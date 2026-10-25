from pathlib import Path
import duckdb

DB_PATH = Path("data/warehouse/ai_ecolens.duckdb")
SQL_DIR = Path("sql")

with duckdb.connect(str(DB_PATH)) as con:

    for filename in [
        "01_model_analysis.sql",
        "02_pareto_frontier.sql"
    ]:
        sql = (SQL_DIR / filename).read_text(
            encoding="utf-8"
        )

        con.execute(sql)

        print(f"Executed: {filename}")

    pareto_df = con.execute("""
        SELECT *
        FROM v_pareto_frontier
        ORDER BY energy_wh_per_1k
    """).df()

    print("\nPareto frontier:")
    print(pareto_df)

    print("\nNumber of Pareto-optimal models:", len(pareto_df))