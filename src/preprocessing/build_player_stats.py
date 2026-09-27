import pandas as pd
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "player_match_stats_per90.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "player_stats.csv"
)


STAT_COLUMNS = [
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


def main():

    df = pd.read_csv(INPUT_FILE)

    # -----------------------------------------------------
    # Player totals
    # -----------------------------------------------------

    player_stats = (
        df.groupby("player_id", as_index=False)
        [["minutes_played"] + STAT_COLUMNS]
        .sum()
    )

    # -----------------------------------------------------
    # Keep one player name for each player ID
    # -----------------------------------------------------

    names = (
        df.groupby("player_id")["player_name"]
        .first()
        .reset_index()
    )

    player_stats = player_stats.merge(
        names,
        on="player_id",
        how="left"
    )

    # -----------------------------------------------------
    # Per-90 metrics
    # -----------------------------------------------------

    for column in STAT_COLUMNS:

        player_stats[column + "_per90"] = (
            player_stats[column]
            / player_stats["minutes_played"]
            * 90
        )

    # -----------------------------------------------------
    # Percentage metrics
    # -----------------------------------------------------

    player_stats["pass_completion_pct"] = (
        player_stats["completed_passes"]
        / player_stats["passes"]
        * 100
    )

    player_stats["dribble_success_pct"] = (
        player_stats["completed_dribbles"]
        / player_stats["dribbles"]
        * 100
    )

    player_stats[
        [
            "pass_completion_pct",
            "dribble_success_pct"
        ]
    ] = (
        player_stats[
            [
                "pass_completion_pct",
                "dribble_success_pct"
            ]
        ]
        .fillna(0)
    )

    # -----------------------------------------------------
    # Primary position
    # -----------------------------------------------------

    position_minutes = (
        df.groupby(
            ["player_id", "position"]
        )["minutes_played"]
        .sum()
        .reset_index()
    )

    primary_positions = (
        position_minutes
        .sort_values(
            "minutes_played",
            ascending=False
        )
        .drop_duplicates("player_id")
        [["player_id", "position"]]
        .rename(
            columns={
                "position": "primary_position"
            }
        )
    )

    player_stats = player_stats.merge(
        primary_positions,
        on="player_id",
        how="left"
    )

    # -----------------------------------------------------
    # Save
    # -----------------------------------------------------

    player_stats.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("Player-level statistics created.")
    print("Players:", len(player_stats))
    print("Columns:", len(player_stats.columns))
    print("Duplicate player IDs:",
          player_stats["player_id"].duplicated().sum())
    print("Saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    main()