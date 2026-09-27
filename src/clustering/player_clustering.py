import pandas as pd
from pathlib import Path

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score


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
    / "player_clusters.csv"
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

    X = df[FEATURES]

    # Scale features before K-Means.
    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(X)

    # Test several possible numbers of clusters.
    scores = {}

    for k in range(2, 9):

        model = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=10
        )

        labels = model.fit_predict(
            X_scaled
        )

        score = silhouette_score(
            X_scaled,
            labels
        )

        scores[k] = score

        print(
            f"K={k}, "
            f"silhouette={score:.4f}"
        )

    # Select the K with the highest silhouette score.
    best_k = max(
        scores,
        key=scores.get
    )

    print(
        f"\nSelected K: {best_k}"
    )

    # Train final model.
    model = KMeans(
        n_clusters=best_k,
        random_state=42,
        n_init=10
    )

    df["cluster"] = model.fit_predict(
        X_scaled
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(
        "\nClustering complete."
    )

    print(
        "Players:",
        len(df)
    )

    print(
        "Saved to:",
        OUTPUT_FILE
    )

    print(
        "\nPlayers per cluster:"
    )

    print(
        df["cluster"]
        .value_counts()
        .sort_index()
    )


if __name__ == "__main__":
    main()