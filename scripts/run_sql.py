from pathlib import Path
import duckdb

DB_PATH = Path("data/warehouse/ai_ecolens.duckdb")
SQL_DIR = Path("sql")

with duckdb.connect(str(DB_PATH)) as con:

    # 1. Exécuter les fichiers SQL
    for filename in [
        "01_model_analysis.sql",
        "02_pareto_frontier.sql",
        "03_dashboard_dataset.sql",
        "04_benchmark_pareto.sql",
        "05_benchmark_dashboard.sql"
    ]:
        sql = (SQL_DIR / filename).read_text(
            encoding="utf-8"
        )

        con.execute(sql)

        print(f"Executed: {filename}")

    # 2. Analyser la frontière de Pareto
    pareto_df = con.execute("""
        SELECT *
        FROM v_pareto_frontier
        ORDER BY energy_wh_per_1k
    """).df()

    print("\nPareto frontier:")
    print(pareto_df)

    print("\nNumber of Pareto-optimal models:", len(pareto_df))

    # 3. Préparer les données pour Tableau
    dashboard_df = con.execute("""
        SELECT *
        FROM v_dashboard_models
    """).df()

    # Vérifier les données
    assert len(dashboard_df) == 38
    assert dashboard_df["model_key"].is_unique

    print("\nDashboard dataset:")
    print("Models:", len(dashboard_df))
    print(
        "Pareto models:",
        dashboard_df["is_pareto_optimal"].sum()
    )

    # 4. Exporter le CSV pour Tableau
    output_dir = Path("data/analytics")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "tableau_model_metrics.csv"

    dashboard_df.to_csv(
        output_path,
        index=False
    )

    print(f"\nTableau dataset exported: {output_path}")

    # 5. Export des résultats par benchmark
    benchmark_df = con.execute("""
        SELECT *
        FROM v_benchmark_dashboard
    """).df()

    # Contrôles de qualité
    assert len(benchmark_df) == 114

    assert not benchmark_df.duplicated(
        subset=["model_key", "benchmark"]
    ).any()

    print("\nBenchmark dataset:")
    print("Total rows:", len(benchmark_df))
    print("Unique models:", benchmark_df["model_key"].nunique())

    print("\nPareto models by benchmark:")
    print(
        benchmark_df.groupby("benchmark")[
            "is_pareto_optimal"
        ].sum()
    )

    # 6. Export CSV pour Tableau
    output_path = output_dir / "tableau_benchmark_metrics.csv"

    benchmark_df.to_csv(
        output_path,
        index=False
    )

    print(f"\nExported: {output_path}")