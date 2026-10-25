from pathlib import Path

import duckdb
import pandas as pd


def load_to_duckdb(
    df: pd.DataFrame,
    db_path: Path
) -> None:
    """Load the analytical dataset into DuckDB."""

    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    with duckdb.connect(str(db_path)) as con:

        con.register("input_df", df)

        con.execute("""
            CREATE OR REPLACE TABLE model_metrics AS
            SELECT *
            FROM input_df
        """)

        con.unregister("input_df")

    print(f"Data loaded into DuckDB: {db_path}")