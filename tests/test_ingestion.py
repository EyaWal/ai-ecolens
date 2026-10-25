from pathlib import Path
from src.ai_ecolens.ingestion.energy import load_energy_data


DATA_DIR = Path("data/raw/ai_energy_score")

energy_df = load_energy_data(DATA_DIR)

print("Dataset shape:", energy_df.shape)

print("\nTasks:")
print(energy_df["task"].value_counts())

print("\nPreview:")
print(energy_df.head())
from pathlib import Path

from src.ai_ecolens.ingestion.quality import load_quality_data


QUALITY_DIR = Path("data/raw/open_llm_leaderboard")

quality_df = load_quality_data(QUALITY_DIR)

print("Dataset shape:", quality_df.shape)
print("Unique models:", quality_df["fullname"].nunique())

print("\nColumns:")
print(quality_df.columns.tolist())