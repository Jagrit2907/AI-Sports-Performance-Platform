# Data Inspection — StatsBomb V1
#
# Run after the frozen raw snapshot has been downloaded with:
# python src/ingestion/download_statsbomb.py
#
# The purpose of this notebook/script is inspection only.
# We do NOT clean or transform the source data here.

from pathlib import Path
import json
from collections import Counter

import pandas as pd

PROJECT_ROOT = Path.cwd()
RAW_ROOT = PROJECT_ROOT / "data" / "raw" / "statsbomb"
MANIFEST_PATH = PROJECT_ROOT / "data" / "dataset_manifest.json"

print("Project root:", PROJECT_ROOT)
print("Raw data root exists:", RAW_ROOT.exists())

with MANIFEST_PATH.open("r", encoding="utf-8") as f:
    manifest = json.load(f)

pd.DataFrame(manifest["scope"]["seasons"])
