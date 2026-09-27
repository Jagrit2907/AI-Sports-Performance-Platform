AI Sports Performance, Talent & Coaching Platform

A football analytics project that uses real match event data to analyze player performance and create simple player insights.

What this project does

The current V1 can:

Calculate player statistics from football events

Convert statistics to per-90 metrics

Group players by position

Create a position-aware performance score

Find similar players

Group players using K-Means clustering

Identify strengths and development areas

Create a statistical talent shortlist

Generate simple development recommendations

Show results in a Streamlit dashboard

Dataset

The project uses StatsBomb Open Data.

V1 contains data from these tournaments:

FIFA World Cup 2018

FIFA World Cup 2022

UEFA Euro 2020

UEFA Euro 2024

Copa América 2024

Africa Cup of Nations 2023

The frozen V1 snapshot contains 314 matches.

The raw data is stored locally under:

 data/raw/statsbomb/

Raw data is kept separate from the processed data used by the analysis pipeline.

Main workflow

StatsBomb Data
      ↓
Data Ingestion
      ↓
Player-Match Statistics
      ↓
Per-90 Features
      ↓
Player Profiles
      ↓
Performance Score
      ↓
Similarity + Clustering
      ↓
Talent Shortlist + Recommendations
      ↓
Streamlit Dashboard

Project structure

AI_SPORTS_PROJECT/
├── app/              # Streamlit dashboard
├── data/             # Raw and processed data
├── docs/             # Project documentation
├── models/           # Saved models / model files
├── notebooks/        # Data analysis and exploration
├── src/              # Main Python code
└── tests/            # Tests

Running the dashboard

Install the required packages:

pip install -r requirements.txt

Start the dashboard:

streamlit run app/dashboard.py

Important notes

This is a V1 football analytics prototype, not a complete football scouting system.

The performance score is an analytical index based on the available event data. The talent shortlist identifies players with strong observed statistics; it does not predict future success.

The current dataset does not provide full physical tracking data, and clustering results are exploratory.

Data source

StatsBomb Open Data:
https://github.com/hudl/open-data

Please follow StatsBomb's attribution requirements when using or sharing analysis based on the data.