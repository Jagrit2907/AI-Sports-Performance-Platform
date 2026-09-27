"""Inspect the downloaded StatsBomb V1 snapshot without transforming it."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_ROOT = PROJECT_ROOT / "data" / "raw" / "statsbomb"
MANIFEST_PATH = PROJECT_ROOT / "data" / "dataset_manifest.json"


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def main() -> None:
    manifest = load_json(MANIFEST_PATH)

    matches_rows = []
    player_rows = []
    event_types = Counter()
    positions = Counter()
    missing_event_player = 0
    event_count = 0

    for season in manifest["scope"]["seasons"]:
        competition_id = season["competition_id"]
        season_id = season["season_id"]
        matches_path = RAW_ROOT / "matches" / str(competition_id) / f"{season_id}.json"
        matches = load_json(matches_path)

        for match in matches:
            match_id = match["match_id"]
            matches_rows.append(
                {
                    "match_id": match_id,
                    "competition": match["competition"]["competition_name"],
                    "season": match["season"]["season_name"],
                    "date": match["match_date"],
                    "home": match["home_team"]["home_team_name"],
                    "away": match["away_team"]["away_team_name"],
                    "home_score": match["home_score"],
                    "away_score": match["away_score"],
                }
            )

            lineup_path = RAW_ROOT / "lineups" / f"{match_id}.json"
            lineup_data = load_json(lineup_path)
            for team in lineup_data:
                team_name = team["team_name"]
                for player in team["lineup"]:
                    # A player can have multiple position intervals because of
                    # tactical shifts. For this first inspection, capture every
                    # position observed in the lineup file.
                    player_positions = [p.get("position") for p in player.get("positions", []) if p.get("position")]
                    player_rows.append(
                        {
                            "match_id": match_id,
                            "team": team_name,
                            "player_id": player["player_id"],
                            "player_name": player["player_name"],
                            "positions": player_positions,
                        }
                    )
                    for position in player_positions:
                        positions[position] += 1

            events_path = RAW_ROOT / "events" / f"{match_id}.json"
            events = load_json(events_path)
            event_count += len(events)
            for event in events:
                event_type = event.get("type", {}).get("name", "UNKNOWN")
                event_types[event_type] += 1
                if event.get("player") is None:
                    missing_event_player += 1

    matches_df = pd.DataFrame(matches_rows)
    players_df = pd.DataFrame(player_rows)

    print("=== DATASET INSPECTION ===")
    print(f"Matches: {len(matches_df):,}")
    print(f"Unique teams: {len(set(matches_df['home']) | set(matches_df['away'])):,}")
    print(f"Unique players in lineups: {players_df['player_id'].nunique():,}")
    print(f"Event records: {event_count:,}")
    print(f"Events without player field: {missing_event_player:,}")

    print("\nMatches by competition/season:")
    print(matches_df.groupby(["competition", "season"]).size().to_string())

    print("\nTop event types:")
    print(pd.Series(event_types).sort_values(ascending=False).head(25).to_string())

    print("\nObserved positions in lineups:")
    print(pd.Series(positions).sort_values(ascending=False).to_string())


if __name__ == "__main__":
    main()
