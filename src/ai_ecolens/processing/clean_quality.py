import pandas as pd


def clean_quality_data(quality_df: pd.DataFrame) -> pd.DataFrame:
    """Prepare model quality evaluations."""

    df = quality_df.copy()

    df["model_key"] = (
        df["fullname"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    df["Submission Date"] = pd.to_datetime(
        df["Submission Date"],
        errors="coerce"
    )

    df["precision_priority"] = (
        df["Precision"]
        .astype(str)
        .str.lower()
        .map({
            "float16": 0,
            "bfloat16": 1
        })
        .fillna(2)
    )

    # Conserver les évaluations pour le moment.
    # La sélection se fera après la jointure.
    return df