CREATE OR REPLACE VIEW v_dashboard_models AS
SELECT
    m.model,
    m.model_key,
    m.energy_wh_per_1k,
    m.mmlu_pro_score,
    m.ifeval_score,
    m.average_score,
    m.parameters_b,
    m.precision,
    m.performance_rank,
    m.energy_rank,
    CASE
        WHEN p.model_key IS NOT NULL THEN TRUE
        ELSE FALSE
    END AS is_pareto_optimal
FROM v_model_performance m
LEFT JOIN v_pareto_frontier p
    ON m.model_key = p.model_key;