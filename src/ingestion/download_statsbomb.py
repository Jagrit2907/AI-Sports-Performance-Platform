"""Download the frozen V1 StatsBomb Open Data snapshot.

This script downloads only the competition/season scope declared in
``data/dataset_manifest.json``. It is intentionally separate from
preprocessing so raw source data remains untouched.
"""

from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = PROJECT_ROOT / "data" / "dataset_manifest.json"
RAW_ROOT = PROJECT_ROOT / "data" / "raw" / "statsbomb"

USER_AGENT = "AI-Sports-Platform/1.0"
MAX_RETRIES = 4
RETRY_SECONDS = 2


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download_json(url: str, destination: Path) -> None:
    """Download one JSON resource with retries and atomic replacement."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(destination.suffix + ".part")

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            request = Request(url, headers={"User-Agent": USER_AGENT})
            with urlopen(request, timeout=60) as response:
                body = response.read()

            # Validate before replacing the existing file.
            json.loads(body.decode("utf-8"))
            temporary.write_bytes(body)
            temporary.replace(destination)
            return
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
            if attempt == MAX_RETRIES:
                raise RuntimeError(f"Failed to download {url}: {exc}") from exc
            print(f"  Retry {attempt}/{MAX_RETRIES - 1}: {exc}")
            time.sleep(RETRY_SECONDS * attempt)


def load_manifest() -> dict:
    with MANIFEST_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def main() -> int:
    manifest = load_manifest()
    source = manifest["source"]
    base_url = source["raw_base"].rstrip("/")

    # Step 1: competition metadata.
    competitions_path = RAW_ROOT / "competitions.json"
    print("Downloading competition metadata...")
    download_json(f"{base_url}/competitions.json", competitions_path)

    download_record = {
        "source": source["repository"],
        "raw_base": base_url,
        "files": [],
        "scope": manifest["scope"]["seasons"],
    }

    record_file = competitions_path
    download_record["files"].append(
        {
            "path": str(record_file.relative_to(PROJECT_ROOT)),
            "sha256": sha256_file(record_file),
        }
    )

    # Step 2: matches + lineups + events for the frozen competition/season set.
    total_matches = 0
    for season in manifest["scope"]["seasons"]:
        competition_id = season["competition_id"]
        season_id = season["season_id"]
        competition = season["competition"]
        season_name = season["season"]

        print(f"\n[{competition} {season_name}]")
        matches_url = f"{base_url}/matches/{competition_id}/{season_id}.json"
        matches_path = RAW_ROOT / "matches" / str(competition_id) / f"{season_id}.json"
        download_json(matches_url, matches_path)
        download_record["files"].append(
            {
                "path": str(matches_path.relative_to(PROJECT_ROOT)),
                "sha256": sha256_file(matches_path),
            }
        )

        matches = json.loads(matches_path.read_text(encoding="utf-8"))
        if len(matches) != season["expected_matches"]:
            raise RuntimeError(
                f"Expected {season['expected_matches']} matches for {competition} {season_name}, "
                f"but source returned {len(matches)}. Stop rather than silently accepting a changed dataset."
            )

        print(f"  matches: {len(matches)}")
        total_matches += len(matches)

        for index, match in enumerate(matches, start=1):
            match_id = match["match_id"]
            print(f"  [{index:>2}/{len(matches)}] match {match_id}", end="\r")

            for kind in ("events", "lineups"):
                path = RAW_ROOT / kind / f"{match_id}.json"
                url = f"{base_url}/{kind}/{match_id}.json"
                if not path.exists():
                    download_json(url, path)
                download_record["files"].append(
                    {
                        "path": str(path.relative_to(PROJECT_ROOT)),
                        "sha256": sha256_file(path),
                    }
                )

        print(f"  downloaded match-level files for {len(matches)} matches")

    snapshot_path = RAW_ROOT / "download_snapshot.json"
    download_record["total_matches"] = total_matches
    snapshot_path.write_text(json.dumps(download_record, indent=2), encoding="utf-8")

    print(f"\nDone. Total matches in frozen V1 scope: {total_matches}")
    print(f"Snapshot manifest: {snapshot_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
