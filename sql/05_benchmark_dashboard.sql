CREATE OR REPLACE VIEW v_benchmark_dashboard AS

SELECT
    m.model,
    m.model_key,
    m.energy_wh_per_1k,
    m.mmlu_pro_score,
    m.ifeval_score,
    m.average_score,
    m.parameters_b,
    m.precision,

    p.benchmark,
    p.performance_score,
    p.is_pareto_optimal

FROM v_model_performance m

JOIN v_benchmark_pareto p
    ON m.model_key = p.model_key;