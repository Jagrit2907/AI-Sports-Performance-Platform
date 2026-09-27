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
    / "player_scores.csv"
)


DIMENSIONS = {

    "attacking": [
        "goals_per90",
        "xg_per90",
        "shots_per90",
    ],

    "passing": [
        "passes_per90",
        "completed_passes_per90",
        "pass_completion_pct",
    ],

    "progression": [
        "carries_per90",
        "carry_distance_per90",
        "completed_dribbles_per90",
    ],

    "defensive": [
        "pressures_per90",
        "tackles_per90",
        "interceptions_per90",
        "clearances_per90",
        "blocks_per90",
        "ball_recoveries_per90",
    ],

    "creativity": [
        "shot_assists_per90",
        "goal_assists_per90",
        "through_balls_per90",
        "crosses_per90",
    ],
}


def main():

    df = pd.read_csv(INPUT_FILE)

    # Only use players meeting the V1 minimum sample.
    df = df[
        df["eligible_for_analysis"]
    ].copy()

    # -----------------------------------------------------
    # Convert every feature to a percentile within
    # the player's position group.
    # -----------------------------------------------------

    all_features = []

    for features in DIMENSIONS.values():
        all_features.extend(features)

    for feature in all_features:

        df[feature + "_pct"] = (
            df.groupby("position_group")[feature]
            .rank(pct=True) * 100
        )

    # -----------------------------------------------------
    # Dimension scores
    # -----------------------------------------------------

    for dimension, features in DIMENSIONS.items():

        percentile_features = [
            feature + "_pct"
            for feature in features
        ]

        df[dimension + "_score"] = (
            df[percentile_features]
            .mean(axis=1)
        )

    # -----------------------------------------------------
    # Overall score
    # -----------------------------------------------------

    score_columns = [
        "attacking_score",
        "passing_score",
        "progression_score",
        "defensive_score",
        "creativity_score",
    ]

    df["overall_score"] = (
        df[score_columns]
        .mean(axis=1)
    )

    # Round scores for easier reading.
    df[score_columns + ["overall_score"]] = (
        df[score_columns + ["overall_score"]]
        .round(2)
    )

    # -----------------------------------------------------
    # Save
    # -----------------------------------------------------

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("Player scores created.")
    print("Players:", len(df))
    print("Saved to:", OUTPUT_FILE)

    print("\nExample:")
    print(
        df[
            [
                "player_name",
                "position_group",
                "attacking_score",
                "passing_score",
                "progression_score",
                "defensive_score",
                "creativity_score",
                "overall_score",
            ]
        ]
        .sort_values(
            "overall_score",
            ascending=False
        )
        .head(10)
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()