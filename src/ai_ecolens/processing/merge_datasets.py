import pandas as pd


def merge_energy_quality(
    energy_df: pd.DataFrame,
    quality_df: pd.DataFrame
) -> pd.DataFrame:
    """Merge energy and quality data into one analytical dataset."""

    matched_df = energy_df.merge(
        quality_df,
        on="model_key",
        how="inner",
        validate="one_to_many"
    )

    # Priorité à float16, puis à la soumission la plus récente
    matched_df = matched_df.sort_values(
        by=[
            "model_key",
            "precision_priority",
            "Submission Date"
        ],
        ascending=[True, True, False]
    )

    matched_df = matched_df.drop_duplicates(
        subset="model_key",
        keep="first"
    )

    columns = {
        "Average ⬆️": "average_score",
        "MMLU-PRO": "mmlu_pro_score",
        "IFEval": "ifeval_score",
        "#Params (B)": "parameters_b",
        "Precision": "precision",
        "Model sha": "model_sha",
        "Submission Date": "submission_date"
    }

    final_df = matched_df[
        [
            "model",
            "model_key",
            "energy_wh_per_1k",
            *columns.keys()
        ]
    ].rename(columns=columns).copy()

    numeric_columns = [
        "energy_wh_per_1k",
        "average_score",
        "mmlu_pro_score",
        "ifeval_score",
        "parameters_b"
    ]

    for col in numeric_columns:
        final_df[col] = pd.to_numeric(
            final_df[col],
            errors="coerce"
        )

    final_df.loc[
        final_df["parameters_b"] <= 0,
        "parameters_b"
    ] = float("nan")

    return final_df