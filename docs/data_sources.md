# Data Sources & Compatibility Audit

## 1. Overview

AI EcoLens combines public AI inference energy measurements with language model performance benchmarks to explore the trade-offs between model quality and energy consumption.

The V1 analysis uses two data sources:

- **AI Energy Score:** GPU inference energy measurements.
- **Open LLM Leaderboard:** Language model performance scores and model metadata.

The validated analytical dataset contains **38 matched models** and **114 model-benchmark observations** across three performance indicators.

This project provides an exploratory cross-source comparison, not a controlled experimental benchmark.

## 2. Data Source Inventory

| Source | Dataset | Local Records | Access Method | License |
|---|---|---:|---|---|
| AI Energy Score | Question Answering | 18 | Public benchmark CSV | Dataset reuse terms to verify |
| AI Energy Score | Summarization | 11 | Public benchmark CSV | Dataset reuse terms to verify |
| AI Energy Score | Text Generation | 62 | Public benchmark CSV | Dataset reuse terms to verify |
| Open LLM Leaderboard | Model Evaluation Results | 4,576 | Public leaderboard CSV | Dataset reuse terms to verify |

**Source references:**

- [AI Energy Score](https://huggingface.github.io/AIEnergyScore/)
- [Open LLM Leaderboard](https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard)

ML.ENERGY and Artificial Analysis were considered during initial research but are not included in the V1 pipeline.

## 3. Raw Dataset Structure

The project expects the following local files:

```text
data/raw/
├── ai_energy_score/
│   ├── question_answering.csv
│   ├── summarization.csv
│   └── text_generation.csv
└── open_llm_leaderboard/
    └── open_llm_leaderboard.csv
```

Raw datasets are excluded from Git version control.

### 3.1 AI Energy Score

The source files contain 91 records across three tasks.

| File | Rows | Available Columns |
|---|---:|---|
| `question_answering.csv` | 18 | `model`, `total_gpu_energy`, `energy_score` |
| `summarization.csv` | 11 | `model`, `total_gpu_energy`, `energy_score` |
| `text_generation.csv` | 62 | `model`, `total_gpu_energy`, `energy_score`, `class`, `test date` |

**Key fields:**

- `model`: Model identifier.
- `total_gpu_energy`: GPU energy measurement reported by the source.
- `energy_score`: Energy-efficiency score reported by the source.
- `class`: Additional model classification, available for text generation.
- `test date`: Test date, available for text generation.

The V1 pipeline uses the `total_gpu_energy` field from the AI Energy Score text-generation dataset. It multiplies the source value by 1,000 to produce the analytical metric `energy_wh_per_1k`.

This metric is labeled GPU Energy (Wh per 1,000 queries), following the source leaderboard's reporting convention. It represents GPU inference energy rather than total datacenter energy consumption.

The three tasks must not be assumed to have equivalent workloads or inference conditions.

### 3.2 Open LLM Leaderboard

The local dataset contains **4,576 records and 34 columns**.

Relevant fields include:

| Column | Description |
|---|---|
| `Model` | Model identifier |
| `fullname` | Full model name |
| `Model sha` | Model revision identifier |
| `#Params (B)` | Number of parameters in billions |
| `Average ⬆️` | Aggregate benchmark score |
| `IFEval` | Instruction-following evaluation score |
| `MMLU-PRO` | Knowledge and reasoning evaluation score |
| `BBH` | Reasoning benchmark score |
| `MATH Lvl 5` | Mathematical reasoning benchmark score |
| `GPQA` | Graduate-level question-answering benchmark score |
| `MUSR` | Multi-step reasoning benchmark score |
| `Hub License` | Model repository license metadata |
| `Submission Date` | Leaderboard submission date |
| `Upload To Hub Date` | Model upload date |
| `CO₂ cost (kg)` | Source-provided CO₂ cost field |

The V1 dashboard uses MMLU-Pro, IFEval, and Average Score.

The `Hub License` field describes model licensing metadata and does not establish the reuse license of the complete leaderboard dataset.

The source-provided `CO₂ cost (kg)` field is not treated as equivalent to AI Energy Score GPU energy measurements.

## 4. Data Processing Pipeline

The data pipeline follows these stages:

1. **Ingestion:** Load the four source CSV files using Python and pandas.
2. **Cleaning:** Standardize and validate energy and quality records.
3. **Model Matching:** Combine compatible model identifiers across sources.
4. **Storage:** Export the processed dataset and load it into DuckDB.
5. **SQL Analytics:** Compute analytical metrics and Pareto frontiers.
6. **Visualization:** Export model-level and benchmark-level datasets for Tableau.
### Model Matching and Submission Selection

Only the `text_generation` subset of AI Energy Score is retained for the V1 analytical dataset.

Model identifiers are normalized by trimming leading and trailing whitespace and converting text to lowercase.

An inner join is performed between AI Energy Score's `model` column and Open LLM Leaderboard's `fullname` column using the normalized `model_key`.

When multiple leaderboard submissions exist for the same model, the pipeline selects one using the following priority:

1. `float16` precision
2. `bfloat16` precision
3. Other or unspecified precisions

Within each precision category, the most recent submission is preferred.

The final dataset retains the selected model SHA, precision, and submission date.

**Limitation:** Matching model names does not guarantee that the energy and quality measurements correspond to identical model revisions or inference configurations.
### Generated Outputs

| File | Purpose |
|---|---|
| `data/processed/energy_quality_comparison.csv` | Merged energy and quality dataset |
| `data/warehouse/ai_ecolens.duckdb` | Local analytical database |
| `data/analytics/tableau_model_metrics.csv` | Model-level analytical metrics |
| `data/analytics/tableau_benchmark_metrics.csv` | Benchmark-level metrics and Pareto indicators |

The validated pipeline produces 38 model-level records and 114 model-benchmark observations.

## 5. Data Compatibility Assessment

Combining measurements from different benchmark sources introduces important limitations.

| Criterion | V1 Assessment |
|---|---|
| Model identity | Matching implemented; model revisions require further validation |
| Evaluation tasks | Different protocols across sources |
| Inference hardware | Not fully documented in the local source schema |
| Batch size and precision | Not fully documented |
| Prompt and output lengths | Not available in the inspected source columns |
| Performance metrics | Analyzed separately by benchmark |
| Energy measurement scope | Requires source-methodology verification |
| Measurement dates | Partially available |
| Controlled experimental comparison | Not established |

**Interpretation:** The merged dataset supports exploratory energy-performance analysis. It does not demonstrate how the same models would perform under identical hardware, prompts, batch sizes, or inference configurations.

## 6. Analytical Metrics

### Energy Consumption

The analytical dashboard uses an energy indicator labeled:

`energy_wh_per_1k`

This represents the pipeline's normalized energy metric, expressed as Wh per 1,000 queries.

The pipeline calculates this metric as:

`energy_wh_per_1k = total_gpu_energy * 1000`

The metric follows the GPU energy reporting convention of AI Energy Score. Lower values are preferable.

Lower energy values are treated as preferable.

### Model Performance

The analysis uses three performance indicators:

- **MMLU-Pro:** Knowledge and reasoning.
- **IFEval:** Instruction-following.
- **Average Score:** Aggregate leaderboard performance.

Higher performance values are treated as preferable.

### Pareto Optimality

A model is Pareto-optimal when no other evaluated model performs at least as well on both energy and performance, with a strict improvement in at least one objective.

Pareto frontiers are computed separately for each performance indicator.

## 7. Validated Results

| Indicator | Result |
|---|---:|
| Matched models | 38 |
| Model-benchmark observations | 114 |
| Performance indicators | 3 |
| SQL transformation scripts | 5 |
| Automated tests passed | 3 |

### Pareto-Optimal Models

| Benchmark | Pareto-Optimal Models |
|---|---:|
| MMLU-Pro | 10 |
| IFEval | 9 |
| Average Score | 15 |

These results are specific to the evaluated dataset and should not be generalized to all available AI models.

## 8. Reproducibility

### Requirements

- Python 3.11+
- Dependencies listed in `requirements.txt`
- Four source CSV files placed in their expected directories

### Run the Pipeline

From the project root:

```bash
python -m pip install -r requirements.txt
python -m scripts.run_pipeline
python -m scripts.run_sql
python -m pytest -q
```

The current pipeline has been successfully executed and tested in the development environment.

### Current Reproducibility Limitations

The raw datasets are not committed to Git.

The following information must still be documented to enable full reproduction from a fresh clone:

- Exact download locations for the four CSV files
- Dataset snapshot or extraction dates
- Dataset licenses and redistribution conditions
- Any manual preparation performed before ingestion
- Verification of energy measurement units and normalization

## 9. Scientific Limitations

- Energy and performance results originate from different benchmark protocols.
- Model names may refer to different revisions or configurations.
- Hardware and workload differences can influence energy consumption.
- Normalization does not automatically make independent experiments comparable.
- GPU energy consumption is not equivalent to total system energy or lifecycle carbon emissions.
- Pareto optimality depends on the available models and selected metrics.
- The analysis should not be used as a definitive ranking of AI models' environmental impact.

## 10. Future Improvements

- [ ] Document exact dataset acquisition and snapshot information.
- [ ] Verify dataset licenses.
- [x] Verify the energy normalization implemented in the pipeline.
- [ ] Validate energy measurement boundaries and experimental conditions.
- [ ] Improve model revision matching.
- [ ] Add automated data-quality checks.
- [ ] Document experimental hardware and workload conditions.
- [ ] Automate dataset acquisition where permitted.
- [ ] Investigate inference cost and carbon estimation using explicit assumptions.

---

**Project:** AI EcoLens  
**Status:** V1 — Analytics pipeline and Tableau dashboard published.