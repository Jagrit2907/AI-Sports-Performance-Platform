import pandas as pd
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "player_scores.csv"
)

TALENT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "talent_shortlist.csv"
)

RECOMMENDATION_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "recommendations.csv"
)


DIMENSIONS = [
    "attacking_score",
    "passing_score",
    "progression_score",
    "defensive_score",
    "creativity_score",
]


RECOMMENDATIONS = {
    "attacking_score":
        "Focus on shot volume, shot quality and finishing opportunities.",

    "passing_score":
        "Focus on pass completion and consistent ball distribution.",

    "progression_score":
        "Focus on ball carrying, progression and successful dribbling.",

    "defensive_score":
        "Focus on defensive pressure, tackles, interceptions and recoveries.",

    "creativity_score":
        "Focus on chance creation, shot assists, through balls and crosses.",
}


def dimension_name(column):
    return column.replace("_score", "").title()


def main():

    df = pd.read_csv(INPUT_FILE)

    # -----------------------------------------------------
    # Strengths and development areas
    # -----------------------------------------------------

    df["strength_1"] = ""
    df["strength_2"] = ""
    df["development_1"] = ""
    df["development_2"] = ""

    for index, row in df.iterrows():

        scores = row[DIMENSIONS].sort_values(
            ascending=False
        )

        highest = scores.head(2)
        lowest = scores.tail(2).sort_values()

        df.at[index, "strength_1"] = dimension_name(
            highest.index[0]
        )

        df.at[index, "strength_2"] = dimension_name(
            highest.index[1]
        )

        df.at[index, "development_1"] = dimension_name(
            lowest.index[0]
        )

        df.at[index, "development_2"] = dimension_name(
            lowest.index[1]
        )

    # -----------------------------------------------------
    # Talent shortlist
    # -----------------------------------------------------

    talent = (
        df.sort_values(
            ["position_group", "overall_score"],
            ascending=[True, False]
        )
        .groupby(
            "position_group",
            group_keys=False
        )
        .head(10)
    )

    talent_columns = [
        "player_id",
        "player_name",
        "position_group",
        "minutes_played",
        "overall_score",
        "attacking_score",
        "passing_score",
        "progression_score",
        "defensive_score",
        "creativity_score",
    ]

    talent[talent_columns].to_csv(
        TALENT_FILE,
        index=False
    )

    # -----------------------------------------------------
    # Recommendations
    # -----------------------------------------------------

    recommendations = []

    for _, row in df.iterrows():

        lowest = (
            row[DIMENSIONS]
            .sort_values()
            .head(2)
        )

        for dimension in lowest.index:

            recommendations.append(
                {
                    "player_id": row["player_id"],
                    "player_name": row["player_name"],
                    "position_group": row["position_group"],
                    "development_area": dimension_name(
                        dimension
                    ),
                    "recommendation": RECOMMENDATIONS[
                        dimension
                    ],
                }
            )

    recommendation_df = pd.DataFrame(
        recommendations
    )

    recommendation_df.to_csv(
        RECOMMENDATION_FILE,
        index=False
    )

    print("Final analytics created.")

    print(
        "Talent shortlist:",
        TALENT_FILE
    )

    print(
        "Recommendations:",
        RECOMMENDATION_FILE
    )


if __name__ == "__main__":
    main()