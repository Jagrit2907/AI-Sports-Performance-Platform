import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "player_clusters.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "cluster_summary.csv"
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

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)

    # Plot
    plt.figure(figsize=(9, 6))

    for cluster in sorted(df["cluster"].unique()):

        points = X_pca[df["cluster"] == cluster]

        plt.scatter(
            points[:, 0],
            points[:, 1],
            label=f"Cluster {cluster}"
        )

    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.title("Player Clusters")
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Cluster averages
    summary = (
        df.groupby("cluster")[FEATURES]
        .mean()
        .round(2)
    )

    summary.to_csv(OUTPUT_FILE)

    print("\nCluster summary:")
    print(summary)

    print(
        "\nPCA variance explained:",
        round(pca.explained_variance_ratio_.sum(), 3)
    )

    print(
        "\nSaved:",
        OUTPUT_FILE
    )


if __name__ == "__main__":
    main()