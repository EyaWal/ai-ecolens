CREATE OR REPLACE VIEW v_pareto_frontier AS

SELECT
    a.model,
    a.model_key,
    a.energy_wh_per_1k,
    a.mmlu_pro_score,
    a.parameters_b

FROM v_model_performance a

WHERE NOT EXISTS (

    SELECT 1
    FROM v_model_performance b

    WHERE
        b.energy_wh_per_1k <= a.energy_wh_per_1k

        AND b.mmlu_pro_score >= a.mmlu_pro_score

        AND (
            b.energy_wh_per_1k < a.energy_wh_per_1k
            OR b.mmlu_pro_score > a.mmlu_pro_score
        )
);