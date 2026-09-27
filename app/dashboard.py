import pandas as pd
import streamlit as st
from pathlib import Path


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data" / "processed"


# ---------------------------------------------------------
# Load data
# ---------------------------------------------------------

players = pd.read_csv(
    DATA_DIR / "player_scores.csv"
)

similar = pd.read_csv(
    DATA_DIR / "similar_players.csv"
)

recommendations = pd.read_csv(
    DATA_DIR / "recommendations.csv"
)

talent = pd.read_csv(
    DATA_DIR / "talent_shortlist.csv"
)


# ---------------------------------------------------------
# Page settings
# ---------------------------------------------------------

st.set_page_config(
    page_title="AI Sports Performance",
    page_icon="⚽",
    layout="wide"
)

st.title("⚽ AI Sports Performance Platform")
st.caption(
    "Explainable football performance analytics"
)


# ---------------------------------------------------------
# Tabs
# ---------------------------------------------------------

profile_tab, talent_tab = st.tabs(
    ["Player Profile", "Talent Shortlist"]
)


# =========================================================
# PLAYER PROFILE
# =========================================================

with profile_tab:

    player_name = st.selectbox(
        "Select a player",
        sorted(players["player_name"].unique())
    )

    player = players[
        players["player_name"] == player_name
    ].iloc[0]

    st.subheader(player_name)

    # -----------------------------------------------------
    # Basic information
    # -----------------------------------------------------

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Position",
        player["position_group"]
    )

    col2.metric(
        "Minutes",
        f"{player['minutes_played']:.0f}"
    )

    col3.metric(
        "Overall Score",
        f"{player['overall_score']:.1f}"
    )

    # -----------------------------------------------------
    # Performance profile
    # -----------------------------------------------------

    st.subheader("Performance Profile")

    scores = pd.DataFrame(
        {
            "Dimension": [
                "Attacking",
                "Passing",
                "Progression",
                "Defensive",
                "Creativity"
            ],
            "Score": [
                player["attacking_score"],
                player["passing_score"],
                player["progression_score"],
                player["defensive_score"],
                player["creativity_score"]
            ]
        }
    )

    st.bar_chart(
        scores.set_index("Dimension")
    )

    # -----------------------------------------------------
    # Strengths and development areas
    # -----------------------------------------------------

    score_columns = {
        "Attacking": player["attacking_score"],
        "Passing": player["passing_score"],
        "Progression": player["progression_score"],
        "Defensive": player["defensive_score"],
        "Creativity": player["creativity_score"]
    }

    sorted_scores = sorted(
        score_columns.items(),
        key=lambda x: x[1],
        reverse=True
    )

    strengths = [
        sorted_scores[0][0],
        sorted_scores[1][0]
    ]

    development = [
        sorted_scores[-1][0],
        sorted_scores[-2][0]
    ]

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Strengths")

        for item in strengths:
            st.write("✓", item)

    with col2:

        st.subheader("Development Areas")

        for item in development:
            st.write("•", item)

    # -----------------------------------------------------
    # Similar players
    # -----------------------------------------------------

    st.subheader("Similar Players")

    similar_players = similar[
        similar["player_id"] == player["player_id"]
    ][
        [
            "similar_player_name",
            "similarity"
        ]
    ].head(5)

    similar_players = similar_players.rename(
        columns={
            "similar_player_name": "Player",
            "similarity": "Similarity"
        }
    )

    st.dataframe(
        similar_players,
        hide_index=True,
        width="stretch"
    )

    # -----------------------------------------------------
    # Recommendations
    # -----------------------------------------------------

    st.subheader("Development Recommendations")

    player_recommendations = recommendations[
        recommendations["player_id"] == player["player_id"]
    ]

    for _, row in player_recommendations.iterrows():

        st.info(
            f"**{row['development_area']}** — "
            f"{row['recommendation']}"
        )


# =========================================================
# TALENT SHORTLIST
# =========================================================

with talent_tab:

    st.subheader("Statistical Talent Shortlist")

    st.caption(
        "Players with strong observed statistical profiles "
        "within their position groups."
    )

    selected_position = st.selectbox(
        "Position group",
        sorted(
            talent["position_group"].unique()
        )
    )

    shortlist = talent[
        talent["position_group"] == selected_position
    ][
        [
            "player_name",
            "position_group",
            "minutes_played",
            "overall_score"
        ]
    ]

    shortlist = shortlist.rename(
        columns={
            "player_name": "Player",
            "position_group": "Position",
            "minutes_played": "Minutes",
            "overall_score": "Overall Score"
        }
    )

    st.dataframe(
        shortlist,
        hide_index=True,
        width="stretch"
    )

    st.caption(
        "Statistical shortlist only; it does not predict "
        "future professional success."
    )


# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------

st.divider()

st.caption(
    "V1 • StatsBomb Open Data • Position-aware analysis"
)