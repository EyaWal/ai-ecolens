from pathlib import Path

import pandas as pd
from datasets import load_dataset


def load_quality_data(
    output_dir: Path,
    refresh: bool = False
) -> pd.DataFrame:
    """
    Load Open LLM Leaderboard evaluations.

    Reuse a local CSV when available.
    Download from Hugging Face otherwise.
    """

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "open_llm_leaderboard.csv"

    if output_path.exists() and not refresh:
        print("Loading local quality dataset...")
        return pd.read_csv(output_path)

    print("Downloading quality dataset from Hugging Face...")

    dataset = load_dataset(
        "open-llm-leaderboard/contents",
        split="train"
    )

    quality_df = dataset.to_pandas()

    quality_df.to_csv(output_path, index=False)

    print(f"Saved to: {output_path}")

    return quality_df