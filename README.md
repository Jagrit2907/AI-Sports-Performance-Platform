# AI Sports Performance, Talent & Coaching Platform

Version 1 is a football analytics prototype built from **StatsBomb Open Data**.

## V1 dataset status

**FROZEN SCOPE** — the V1 analytical/training population is the fixed competition-season set recorded in `data/dataset_manifest.json`.

The source data is event- and lineup-based JSON. V1 will derive player-level statistics from actual football actions rather than game ratings.

## V1 roadmap

1. Data ingestion and inspection
2. Preprocessing and validation
3. Player-match feature engineering
4. Position-aware player profiles
5. Transparent performance scoring
6. Strength/weakness analysis
7. Player similarity
8. Player clustering
9. Statistical talent shortlist
10. Rule-based development recommendations
11. Python-friendly dashboard

## Guardrails

- No fabricated data, metrics, counts, model accuracy, or trends.
- No future-success claims without a valid supervised target.
- Core features will not depend on optional 360 data.
- Any change to the frozen V1 population creates a new dataset version.

## Source

StatsBomb Open Data: https://github.com/hudl/open-data

When publishing or sharing analysis based on this data, follow StatsBomb's attribution and logo requirements.


## Immediate next step

Run `python src/ingestion/download_statsbomb.py` once the project is on your machine. Then run `python src/ingestion/inspect_snapshot.py` and open `notebooks/01_data_inspection.ipynb`. We will use the inspection output to finalize feature definitions before preprocessing.
