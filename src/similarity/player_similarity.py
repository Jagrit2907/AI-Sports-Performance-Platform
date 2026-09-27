import pandas as pd
from pathlib import Path

from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "player_scores.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "similar_players.csv"
)


FEATURES = [
    "goals_per90",
    "xg_per90",
    "shots_per90",

    "passes_per90",
    "completed_passes_per90",
    "pass_completion_pct",

    "carries_per90",
    "carry_distance_per90",
    "completed_dribbles_per90",

    "pressures_per90",
    "tackles_per90",
    "interceptions_per90",
    "clearances_per90",
    "blocks_per90",
    "ball_recoveries_per90",

    "shot_assists_per90",
    "goal_assists_per90",
    "through_balls_per90",
    "crosses_per90",
]


def main():

    df = pd.read_csv(INPUT_FILE)

    results = []

    # Compare players within the same position group.
    for position_group, group in df.groupby(
        "position_group"
    ):

        if len(group) < 2:
            continue

        X = group[FEATURES]

        scaler = StandardScaler()

        X_scaled = scaler.fit_transform(X)

        similarities = cosine_similarity(
            X_scaled
        )

        for i in range(len(group)):

            scores = similarities[i]

            # Sort from most similar to least similar.
            indices = scores.argsort()[::-1]

            added = 0

            for j in indices:

                # Don't compare a player with himself.
                if i == j:
                    continue

                results.append(
                    {
                        "player_id":
                            group.iloc[i]["player_id"],

                        "player_name":
                            group.iloc[i]["player_name"],

                        "position_group":
                            position_group,

                        "similar_player_id":
                            group.iloc[j]["player_id"],

                        "similar_player_name":
                            group.iloc[j]["player_name"],

                        "similarity":
                            round(float(scores[j]), 4),
                    }
                )

                added += 1

                if added == 5:
                    break

    result_df = pd.DataFrame(results)

    result_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("Similarity analysis complete.")
    print("Rows:", len(result_df))
    print("Saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    main()