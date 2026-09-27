AI Sports Performance, Talent & Coaching Platform

A football analytics platform built with real match event data to analyze player performance, compare player profiles, explore player archetypes, and generate simple development insights.

Current Version: V1 — Football Analytics

⚽ What This Project Does

The V1 pipeline turns raw football match events into player-level analytics.

Core Features

📊 Player Statistics — Calculates performance statistics from match events

⏱️ Per-90 Metrics — Normalizes statistics based on playing time

🧩 Position Groups — Groups players into broad football positions

📈 Performance Score — Creates a position-aware analytical performance score

🔎 Player Similarity — Finds players with similar statistical profiles

🧠 K-Means Clustering — Groups players into statistical profiles

💪 Strengths & Development Areas — Highlights strong and weaker dimensions

🌟 Talent Shortlist — Identifies players with strong observed statistics

💡 Recommendations — Generates simple development suggestions

🖥️ Streamlit Dashboard — Provides an interactive interface for exploring results

🗂️ Dataset

The project uses StatsBomb Open Data.

V1 Tournament Coverage

Competition

Year

FIFA World Cup

2018

FIFA World Cup

2022

UEFA European Championship

2020

UEFA European Championship

2024

Copa América

2024

Africa Cup of Nations

2023

Frozen V1 dataset: 314 matches

The raw dataset is stored locally in:

data/raw/statsbomb/

Raw data is kept separate from the processed datasets used by the analysis pipeline.

🔄 Main Workflow

                StatsBomb Open Data
                        │
                        ▼
                Data Ingestion
                        │
                        ▼
             Player-Match Statistics
                        │
                        ▼
                  Per-90 Metrics
                        │
                        ▼
                 Player Profiles
                        │
                        ▼
                Performance Score
                   /         \
                  ▼           ▼
             Similarity    Clustering
                  \           /
                   ▼         ▼
              Talent Shortlist
                      +
                Recommendations
                        │
                        ▼
             Streamlit Dashboard

📁 Project Structure

AI_SPORTS_PROJECT/
│
├── app/
│   └── dashboard.py              # Streamlit dashboard
│
├── data/
│   ├── raw/                      # Original StatsBomb data
│   └── processed/                # Generated analysis datasets
│
├── docs/                         # Project documentation
├── models/                       # Saved model files
├── notebooks/                    # Analysis and experimentation
│
├── src/
│   ├── clustering/
│   ├── features/
│   ├── ingestion/
│   ├── preprocessing/
│   ├── recommendations/
│   ├── scoring/
│   ├── similarity/
│   ├── talent/
│   └── visualization/
│
├── tests/                        # Tests
│
├── dataset_manifest.json         # V1 dataset definition
├── requirements.txt              # Python dependencies
├── .gitignore
└── README.md

🚀 Running the Dashboard

1. Install dependencies

pip install -r requirements.txt

2. Start the dashboard

streamlit run app/dashboard.py

The dashboard allows you to explore individual player profiles, performance dimensions, similar players, recommendations, and the statistical talent shortlist.

📌 Important Notes

This is a V1 football analytics prototype, not a complete professional scouting system.

The performance score is an analytical index based on the available event data.

The talent shortlist identifies players with strong observed statistics; it does not predict future success.

The dataset does not contain complete physical tracking information.

K-Means clustering is exploratory and should not be interpreted as definitive player archetypes.

Player comparisons can be affected by differences between competitions and playing contexts.

The current analysis focuses on observed event data rather than long-term player development forecasting.

🛠️ Tech Stack

Python • Pandas • NumPy • Scikit-learn • Matplotlib • Streamlit • Git/GitHub

📚 Data Source

StatsBomb Open Data

https://github.com/hudl/open-data

Please follow StatsBomb's attribution requirements when using or sharing analysis based on the data.

🔮 Future Development

Planned future versions can extend the platform with:

Computer Vision for visual football analysis

Deep Learning models

Advanced player recommendation systems

Natural Language / LLM-based coaching insights

Database and backend services

AWS cloud deployment

MLOps and production pipelines

📄 Project Status

V1 Complete ✅

The current version focuses on building a clean end-to-end football analytics pipeline from raw event data to an interactive dashboard.