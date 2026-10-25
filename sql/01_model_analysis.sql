CREATE OR REPLACE VIEW v_model_performance AS

SELECT
    model,
    model_key,
    energy_wh_per_1k,
    mmlu_pro_score,
    ifeval_score,
    average_score,
    parameters_b,
    precision,

    RANK() OVER (
        ORDER BY mmlu_pro_score DESC
    ) AS performance_rank,

    RANK() OVER (
        ORDER BY energy_wh_per_1k ASC
    ) AS energy_rank

FROM model_metrics

WHERE
    energy_wh_per_1k > 0
    AND mmlu_pro_score IS NOT NULL;