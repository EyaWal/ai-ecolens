
from pathlib import Path
import shutil

from huggingface_hub import hf_hub_download


REPO_ID = "AIEnergyScore/Leaderboard"
DATA_DIR = Path("data/raw/ai_energy_score")

TASKS = [
    "text_generation",
    "summarization",
    "question_answering",
]


def download_energy_data():
    """Download AI Energy Score CSV files from Hugging Face."""

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    for task in TASKS:
        destination = DATA_DIR / f"{task}.csv"

        if destination.exists():
            print(f"Already exists: {destination}")
            continue

        source = hf_hub_download(
            repo_id=REPO_ID,
            repo_type="space",
            filename=f"data/energy/{task}.csv",
        )

        shutil.copyfile(source, destination)

        print(f"Downloaded: {destination}")


if __name__ == "__main__":
    download_energy_data()
