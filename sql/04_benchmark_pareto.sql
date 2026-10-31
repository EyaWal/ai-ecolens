CREATE OR REPLACE VIEW v_benchmark_pareto AS

WITH benchmark_scores AS (

    SELECT
        model_key,
        energy_wh_per_1k,
        'MMLU-Pro' AS benchmark,
        mmlu_pro_score AS performance_score
    FROM v_model_performance

    UNION ALL

    SELECT
        model_key,
        energy_wh_per_1k,
        'IFEval' AS benchmark,
        ifeval_score AS performance_score
    FROM v_model_performance

    UNION ALL

    SELECT
        model_key,
        energy_wh_per_1k,
        'Average Score' AS benchmark,
        average_score AS performance_score
    FROM v_model_performance
)

SELECT
    a.model_key,
    a.benchmark,
    a.performance_score,

    CASE

        WHEN a.performance_score IS NULL
            OR a.energy_wh_per_1k IS NULL
        THEN NULL

        WHEN NOT EXISTS (
            SELECT 1
            FROM benchmark_scores b

            WHERE b.benchmark = a.benchmark
              AND b.performance_score IS NOT NULL
              AND b.energy_wh_per_1k <= a.energy_wh_per_1k
              AND b.performance_score >= a.performance_score

              AND (
                  b.energy_wh_per_1k < a.energy_wh_per_1k
                  OR b.performance_score > a.performance_score
              )
        )
        THEN TRUE

        ELSE FALSE
    END AS is_pareto_optimal

FROM benchmark_scores a;