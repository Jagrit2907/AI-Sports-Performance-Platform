import json
import math
from pathlib import Path

import pandas as pd


# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

EVENTS_DIR = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "statsbomb"
    / "events"
)

PLAYER_MATCH_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "player_match.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "player_match_stats.csv"
)


# ---------------------------------------------------------
# Helper function
# ---------------------------------------------------------

def distance(start, end):
    """Calculate distance between two [x, y] coordinates."""

    return math.sqrt(
        (end[0] - start[0]) ** 2
        + (end[1] - start[1]) ** 2
    )


def get_name(value):
    """Get the name from a StatsBomb object."""

    if isinstance(value, dict):
        return value.get("name")

    return value


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    # Load our player-match table
    player_match = pd.read_csv(
        PLAYER_MATCH_FILE
    )

    # Make sure match_id has the same type
    # as the event file IDs.
    player_match["match_id"] = (
        player_match["match_id"]
        .astype(str)
    )

    stats = {}

    # -----------------------------------------------------
    # Read every event file
    # -----------------------------------------------------

    for file in EVENTS_DIR.glob("*.json"):

        match_id = file.stem

        with file.open(
            "r",
            encoding="utf-8"
        ) as f:

            events = json.load(f)

        for event in events:

            player = event.get("player")

            # Some events do not belong to a player.
            if not player:
                continue

            player_id = player["id"]

            key = (
                match_id,
                player_id
            )

            # Create a row the first time we see
            # this player in this match.
            if key not in stats:

                stats[key] = {

                    "match_id": match_id,
                    "player_id": player_id,

                    "passes": 0,
                    "completed_passes": 0,
                    "shot_assists": 0,
                    "goal_assists": 0,
                    "through_balls": 0,
                    "crosses": 0,

                    "shots": 0,
                    "goals": 0,
                    "xg": 0.0,

                    "carries": 0,
                    "carry_distance": 0.0,

                    "dribbles": 0,
                    "completed_dribbles": 0,

                    "pressures": 0,
                    "tackles": 0,
                    "interceptions": 0,
                    "clearances": 0,
                    "blocks": 0,
                    "ball_recoveries": 0,
                }

            row = stats[key]

            event_type = (
                event
                .get("type", {})
                .get("name")
            )

            # -------------------------------------------------
            # PASS
            # -------------------------------------------------

            if event_type == "Pass":

                data = event.get(
                    "pass",
                    {}
                )

                row["passes"] += 1

                # In StatsBomb data, an absent outcome
                # means the pass was completed.
                if data.get("outcome") is None:

                    row["completed_passes"] += 1

                if data.get("shot_assist") is True:
                    row["shot_assists"] += 1

                if data.get("goal_assist") is True:
                    row["goal_assists"] += 1

                if data.get("through_ball") is True:
                    row["through_balls"] += 1

                if data.get("cross") is True:
                    row["crosses"] += 1

            # -------------------------------------------------
            # SHOT
            # -------------------------------------------------

            elif event_type == "Shot":

                data = event.get(
                    "shot",
                    {}
                )

                row["shots"] += 1

                row["xg"] += (
                    data.get(
                        "statsbomb_xg",
                        0
                    )
                    or 0
                )

                outcome = get_name(
                    data.get("outcome")
                )

                if outcome == "Goal":
                    row["goals"] += 1

            # -------------------------------------------------
            # CARRY
            # -------------------------------------------------

            elif event_type == "Carry":

                row["carries"] += 1

                start = event.get(
                    "location"
                )

                end = (
                    event
                    .get("carry", {})
                    .get("end_location")
                )

                if start and end:

                    row["carry_distance"] += (
                        distance(start, end)
                    )

            # -------------------------------------------------
            # DRIBBLE
            # -------------------------------------------------

            elif event_type == "Dribble":

                row["dribbles"] += 1

                outcome = get_name(
                    event
                    .get("dribble", {})
                    .get("outcome")
                )

                if outcome == "Complete":
                    row["completed_dribbles"] += 1

            # -------------------------------------------------
            # DEFENSIVE EVENTS
            # -------------------------------------------------

            elif event_type == "Pressure":

                row["pressures"] += 1

            elif event_type == "Interception":

                row["interceptions"] += 1

            elif event_type == "Clearance":

                row["clearances"] += 1

            elif event_type == "Block":

                row["blocks"] += 1

            elif event_type == "Ball Recovery":

                row["ball_recoveries"] += 1

            elif event_type == "Duel":

                data = event.get(
                    "duel",
                    {}
                )

                duel_type = get_name(
                    data.get("type")
                )

                if duel_type == "Tackle":
                    row["tackles"] += 1

    # -----------------------------------------------------
    # Convert statistics to DataFrame
    # -----------------------------------------------------

    event_stats = pd.DataFrame(
        stats.values()
    )

    # -----------------------------------------------------
    # Add statistics to every player-match row
    # -----------------------------------------------------

    df = player_match.merge(
        event_stats,
        on=[
            "match_id",
            "player_id"
        ],
        how="left"
    )

    # -----------------------------------------------------
    # Players with no relevant events get zero
    # -----------------------------------------------------

    stat_columns = [
        "passes",
        "completed_passes",
        "shot_assists",
        "goal_assists",
        "through_balls",
        "crosses",
        "shots",
        "goals",
        "xg",
        "carries",
        "carry_distance",
        "dribbles",
        "completed_dribbles",
        "pressures",
        "tackles",
        "interceptions",
        "clearances",
        "blocks",
        "ball_recoveries",
    ]

    df[stat_columns] = (
        df[stat_columns]
        .fillna(0)
    )

    # -----------------------------------------------------
    # Save
    # -----------------------------------------------------

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(
        "Player-match statistics created."
    )

    print(
        "Rows:",
        len(df)
    )

    print(
        "Columns:",
        len(df.columns)
    )

    print(
        "Saved to:",
        OUTPUT_FILE
    )


if __name__ == "__main__":
    main()