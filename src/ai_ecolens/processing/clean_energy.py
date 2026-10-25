import pandas as pd


def clean_energy_data(energy_df: pd.DataFrame) -> pd.DataFrame:
    """Prepare text-generation energy measurements."""

    df = energy_df.loc[
        energy_df["task"] == "text_generation"
    ].copy()

    df["model_key"] = (
        df["model"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    # Conversion utilisée dans notre notebook exploratoire
    df["energy_wh_per_1k"] = (
        pd.to_numeric(df["total_gpu_energy"], errors="coerce") * 1000
    )

    return df[
        ["model", "model_key", "energy_wh_per_1k"]
    ]