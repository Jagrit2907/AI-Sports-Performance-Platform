# V1 Data Ingestion

## Goal
Download the exact competition-season scope in `data/dataset_manifest.json` into `data/raw/statsbomb/`, without transforming the raw JSON.

## Why raw data is kept untouched
The raw layer is our source of truth. Preprocessing and feature engineering happen later in separate code. This lets us reproduce or audit every derived metric.

## Run locally
From the project root:

```bash
python -m pip install -r requirements.txt
python src/ingestion/download_statsbomb.py
python src/ingestion/inspect_snapshot.py
```

The downloader stops if an expected tournament match count does not match the frozen manifest. It also validates each downloaded JSON file and records SHA-256 checksums in `data/raw/statsbomb/download_snapshot.json`.

## Important
The container used to prepare this project does not have outbound GitHub access, so the actual raw files must be downloaded from your local machine (or another environment with internet access). No dataset content was fabricated or substituted.
