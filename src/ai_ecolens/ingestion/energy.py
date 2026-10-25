from pathlib import Path
import pandas as pd


def load_energy_data(data_dir: Path) -> pd.DataFrame:
    """
    Load AI Energy Score datasets.
    """

    tasks = [
        "text_generation",
        "summarization",
        "question_answering"
    ]

    dataframes = []

    for task in tasks:

        file_path = data_dir / f"{task}.csv"

        df = pd.read_csv(file_path)

        df["task"] = task

        dataframes.append(df)

    energy_df = pd.concat(
        dataframes,
        ignore_index=True
    )

    return energy_df