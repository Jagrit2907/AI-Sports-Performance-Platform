import json
import subprocess
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

MANIFEST_PATH = PROJECT_ROOT / "dataset_manifest.json"
RAW_ROOT = PROJECT_ROOT / "data" / "raw" / "statsbomb"

BASE_URL = "https://raw.githubusercontent.com/hudl/open-data/master/data"


def download_file(url, destination):
    """Download one file using curl."""

    destination.parent.mkdir(parents=True, exist_ok=True)

    # Don't download a file again if it already exists.
    if destination.exists():
        print("Already exists:", destination)
        return

    subprocess.run(
        [
            "curl.exe",
            "-L",
            url,
            "-o",
            str(destination)
        ],
        check=True
    )

    print("Downloaded:", destination)


def main():

    # Read our frozen dataset definition
    with open(MANIFEST_PATH, "r", encoding="utf-8") as file:
        manifest = json.load(file)

    seasons = manifest["scope"]["seasons"]

    # Download competition metadata
    download_file(
        f"{BASE_URL}/competitions.json",
        RAW_ROOT / "competitions.json"
    )

    # Download data for each competition/season
    for season in seasons:

        competition_id = season["competition_id"]
        season_id = season["season_id"]

        competition = season["competition"]
        season_name = season["season"]

        print("\n", competition, season_name)

        # Match list
        matches_path = (
            RAW_ROOT
            / "matches"
            / str(competition_id)
            / f"{season_id}.json"
        )

        download_file(
            f"{BASE_URL}/matches/{competition_id}/{season_id}.json",
            matches_path
        )

        # Read match list
        with open(matches_path, "r", encoding="utf-8") as file:
            matches = json.load(file)

        # Download events and lineups for every match
        for match in matches:

            match_id = match["match_id"]

            download_file(
                f"{BASE_URL}/events/{match_id}.json",
                RAW_ROOT / "events" / f"{match_id}.json"
            )

            download_file(
                f"{BASE_URL}/lineups/{match_id}.json",
                RAW_ROOT / "lineups" / f"{match_id}.json"
            )


if __name__ == "__main__":
    main()