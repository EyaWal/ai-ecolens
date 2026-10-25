from pathlib import Path

from src.ai_ecolens.ingestion.energy import load_energy_data
from src.ai_ecolens.ingestion.quality import load_quality_data

from src.ai_ecolens.processing.clean_energy import clean_energy_data
from src.ai_ecolens.processing.clean_quality import clean_quality_data
from src.ai_ecolens.processing.merge_datasets import merge_energy_quality
from src.ai_ecolens.storage.duckdb_loader import load_to_duckdb


def main():

    energy_dir = Path("data/raw/ai_energy_score")
    quality_dir = Path("data/raw/open_llm_leaderboard")
    output_dir = Path("data/processed")

    output_dir.mkdir(parents=True, exist_ok=True)

    print("1. Loading energy data...")
    energy_raw = load_energy_data(energy_dir)

    print("2. Loading quality data...")
    quality_raw = load_quality_data(quality_dir)

    print("3. Cleaning energy data...")
    energy_clean = clean_energy_data(energy_raw)

    print("4. Cleaning quality data...")
    quality_clean = clean_quality_data(quality_raw)

    print("5. Merging datasets...")
    final_df = merge_energy_quality(
        energy_clean,
        quality_clean
    )

    print("6. Exporting dataset...")
    output_path = output_dir / "energy_quality_comparison.csv"

    final_df.to_csv(output_path, index=False)
    print("7. Loading data into DuckDB...")

    db_path = Path("data/warehouse/ai_ecolens.duckdb")

    load_to_duckdb(
        df=final_df,
        db_path=db_path
)
    

    print(f"\nPipeline completed!")
    print(f"Models: {len(final_df)}")
    print(f"Output: {output_path}")


if __name__ == "__main__":
    main()