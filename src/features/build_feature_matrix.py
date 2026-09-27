import pandas as pd
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "player_analysis.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "player_features.csv"
)


FEATURES = [
    # Attacking
    "goals_per90",
    "xg_per90",
    "shots_per90",

    # Passing
    "passes_per90",
    "completed_passes_per90",
    "pass_completion_pct",

    # Progression
    "carries_per90",
    "carry_distance_per90",
    "completed_dribbles_per90",

    # Defensive
    "pressures_per90",
    "tackles_per90",
    "interceptions_per90",
    "clearances_per90",
    "blocks_per90",
    "ball_recoveries_per90",

    # Creativity
    "shot_assists_per90",
    "goal_assists_per90",
    "through_balls_per90",
    "crosses_per90",
]


def main():

    df = pd.read_csv(INPUT_FILE)

    # Keep only players meeting our minimum
    # playing-time requirement.
    df = df[
        df["eligible_for_analysis"]
    ].copy()

    # Keep the information needed to identify
    # and interpret each player.
    columns = [
        "player_id",
        "player_name",
        "minutes_played",
        "primary_position",
        "position_group",
        "eligible_for_analysis",
    ] + FEATURES

    features = df[columns].copy()

    # Check for missing feature values.
    missing = features[FEATURES].isna().sum()

    print("Missing feature values:")
    print(missing[missing > 0])

    # Save.
    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    features.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\nFeature matrix created.")
    print("Players:", len(features))
    print("Features:", len(FEATURES))
    print("Saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    main()