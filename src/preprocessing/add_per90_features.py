import pandas as pd
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "player_match_stats.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "player_match_stats_per90.csv"
)


def main():

    df = pd.read_csv(INPUT_FILE)

    # Statistics for which per-90 values make sense.
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

    for column in stat_columns:

        df[column + "_per90"] = (
            df[column]
            / df["minutes_played"]
            * 90
        )

    # Percentage metrics.
    df["pass_completion_pct"] = (
        df["completed_passes"]
        / df["passes"]
        * 100
    )

    df["dribble_success_pct"] = (
        df["completed_dribbles"]
        / df["dribbles"]
        * 100
    )

    # Where there were zero attempts, percentage is undefined.
    df["pass_completion_pct"] = (
        df["pass_completion_pct"]
        .fillna(0)
    )

    df["dribble_success_pct"] = (
        df["dribble_success_pct"]
        .fillna(0)
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("Per-90 features created.")
    print("Rows:", len(df))
    print("Columns:", len(df.columns))
    print("Saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    main()