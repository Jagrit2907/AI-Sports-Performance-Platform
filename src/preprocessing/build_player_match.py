import json
from collections import Counter
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

LINEUPS_DIR = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "statsbomb"
    / "lineups"
)

EVENTS_DIR = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "statsbomb"
    / "events"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
)


def event_time(event):
    """Return event time in seconds."""

    return (
        event["minute"] * 60
        + event["second"]
    )


def main():

    rows = []

    for lineup_file in LINEUPS_DIR.glob("*.json"):

        match_id = lineup_file.stem

        event_file = EVENTS_DIR / f"{match_id}.json"

        with lineup_file.open(
            "r",
            encoding="utf-8"
        ) as file:
            lineups = json.load(file)

        with event_file.open(
            "r",
            encoding="utf-8"
        ) as file:
            events = json.load(file)

        # -------------------------------------------------
        # Player information from lineup
        # -------------------------------------------------

        players = {}

        for team in lineups:

            for player in team["lineup"]:

                players[player["player_id"]] = {
                    "player_name": player["player_name"],
                    "team_id": team["team_id"],
                    "team_name": team["team_name"],
                }

        # -------------------------------------------------
        # Match end
        # -------------------------------------------------

        match_end = max(
            event_time(event)
            for event in events
            if "minute" in event and "second" in event
        )

        # -------------------------------------------------
        # Find starting players
        # -------------------------------------------------

        starters = set()

        for event in events:

            event_type = (
                event
                .get("type", {})
                .get("name")
            )

            if event_type == "Starting XI":

                lineup = (
                    event
                    .get("tactics", {})
                    .get("lineup", [])
                )

                for player in lineup:

                    player_id = player["player"]["id"]

                    starters.add(player_id)

        # -------------------------------------------------
        # Player participation
        # -------------------------------------------------

        start_times = {}

        end_times = {}

        for player_id in starters:
            start_times[player_id] = 0

        # -------------------------------------------------
        # Substitutions
        # -------------------------------------------------

        for event in events:

            event_type = (
                event
                .get("type", {})
                .get("name")
            )

            if event_type != "Substitution":
                continue

            time = event_time(event)

            outgoing = event.get("player")

            substitution = event.get(
                "substitution",
                {}
            )

            replacement = substitution.get(
                "replacement"
            )

            if outgoing:

                player_id = outgoing["id"]

                end_times[player_id] = time

            if replacement:

                player_id = replacement["id"]

                start_times[player_id] = time

        # -------------------------------------------------
        # Find each player's most common event position
        # -------------------------------------------------

        position_counts = {}

        for event in events:

            player = event.get("player")
            position = event.get("position")

            if not player or not position:
                continue

            player_id = player["id"]

            position_name = position.get("name")

            if position_name is None:
                continue

            if player_id not in position_counts:

                position_counts[player_id] = Counter()

            position_counts[player_id][position_name] += 1

        # -------------------------------------------------
        # Build rows
        # -------------------------------------------------

        participant_ids = set(start_times)

        for player_id in participant_ids:

            if player_id not in players:
                continue

            start = start_times[player_id]

            end = end_times.get(
                player_id,
                match_end
            )

            minutes = max(
                0,
                end - start
            ) / 60

            positions = position_counts.get(
                player_id,
                Counter()
            )

            if positions:

                primary_position = (
                    positions.most_common(1)[0][0]
                )

            else:

                primary_position = "Unknown"

            rows.append(
                {
                    "match_id": match_id,
                    "player_id": player_id,
                    "player_name": players[player_id]["player_name"],
                    "team_id": players[player_id]["team_id"],
                    "team_name": players[player_id]["team_name"],
                    "position": primary_position,
                    "minutes_played": round(
                        minutes,
                        2
                    ),
                    "started": player_id in starters,
                }
            )

    # -----------------------------------------------------
    # Create DataFrame
    # -----------------------------------------------------

    df = pd.DataFrame(rows)

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = (
        OUTPUT_DIR
        / "player_match.csv"
    )

    df.to_csv(
        output_file,
        index=False
    )

    print(
        "Player-match table created."
    )

    print(
        "Rows:",
        len(df)
    )

    print(
        "Saved to:",
        output_file
    )


if __name__ == "__main__":
    main()