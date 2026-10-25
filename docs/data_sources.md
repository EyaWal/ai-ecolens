# Data source audit

Complete this table **before** joining benchmark results.

| Source | Dataset / URL | License | Access method | Models | Tasks | Metric + unit | Hardware | Prompt/output length | Date | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| AI Energy Score | https://huggingface.github.io/AIEnergyScore/ | To verify | To verify | TBD | TBD | TBD | TBD | TBD | TBD | |
| ML.ENERGY | https://ml.energy/ | To verify | To verify | TBD | TBD | TBD | TBD | TBD | TBD | |
| Artificial Analysis | https://artificialanalysis.ai/ | To verify | To verify | TBD | TBD | TBD | TBD | TBD | TBD | |

## Compatibility rules
1. Same task definition and comparable quality metric.
2. Similar input/output token lengths, or clearly documented normalization.
3. Known inference hardware, precision and batch/concurrency conditions.
4. Separate measured GPU energy from estimated total service energy.
5. Include source and measurement timestamp in every final record.
6. Treat API pricing separately from self-hosted compute costs.

## First task
Identify one downloadable dataset with at least five models evaluated under a shared protocol. Record its license and schema. Do not merge sources until the compatibility check is complete.
