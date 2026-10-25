import duckdb

con = duckdb.connect("data/warehouse/ai_ecolens.duckdb")

result = con.execute("""
    SELECT
        COUNT(*) AS total_models,
        COUNT(DISTINCT model_key) AS unique_models,
        ROUND(AVG(energy_wh_per_1k), 2) AS avg_energy,
        ROUND(AVG(mmlu_pro_score), 2) AS avg_mmlu
    FROM model_metrics
""").df()

print(result)

con.close()