
# Data Sources & Compatibility Audit

## 1. Overview

AI EcoLens combines public AI inference energy measurements with language model performance benchmarks to explore the trade-offs between model quality and energy consumption.

The V1 analysis uses two sources:

- **AI Energy Score:** GPU inference energy measurements.
- **Open LLM Leaderboard:** Language model performance scores and model metadata.

The validated analytical dataset contains **38 matched models** and **114 model-benchmark observations** across three performance indicators.

This project provides an exploratory cross-source comparison, not a controlled experimental benchmark.

## 2. Data Source Inventory

| Source | Dataset | Local Records | Acquisition | License |
|---|---|---:|---|---|
| AI Energy Score | Question Answering | 18 | Hugging Face Hub | Reuse terms to verify |
| AI Energy Score | Summarization | 11 | Hugging Face Hub | Reuse terms to verify |
| AI Energy Score | Text Generation | 62 | Hugging Face Hub | Reuse terms to verify |
| Open LLM Leaderboard | Model Evaluation Results | 4,576 | Hugging Face Datasets | Reuse terms to verify |

### Source References

**AI Energy Score**

- Project: https://huggingface.github.io/AIEnergyScore/
- Hugging Face Space: https://huggingface.co/spaces/AIEnergyScore/Leaderboard
- Repository ID: `AIEnergyScore/Leaderboard`
- Repository type: `space`
- Source paths: `data/energy/{task}.csv`

**Open LLM Leaderboard**

- Leaderboard: https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard
- Dataset: https://huggingface.co/datasets/open-llm-leaderboard/contents
- Dataset ID: `open-llm-leaderboard/contents`
- Dataset split: `train`

ML.ENERGY and Artificial Analysis were considered during initial research but are not included in the V1 pipeline.

### Dataset Versioning

The source datasets are retrieved without fixed repository revisions.

The fresh-clone validation reproduced the expected analytical counts, but future upstream changes may affect the results.

Dataset snapshot dates, exact revisions, and reuse licenses remain to be documented.

## 3. Raw Dataset Structure

The pipeline stores source data locally in:

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

The downloaded source files contain 91 records across three tasks.

| File | Rows | Available Columns |
|---|---:|---|
| `question_answering.csv` | 18 | `model`, `total_gpu_energy`, `energy_score` |
| `summarization.csv` | 11 | `model`, `total_gpu_energy`, `energy_score` |
| `text_generation.csv` | 62 | `model`, `total_gpu_energy`, `energy_score`, `class`, `test date` |

**Key fields:**

- `model`: Model identifier.
- `total_gpu_energy`: GPU energy measurement reported by the source.
- `energy_score`: Energy-efficiency score reported by the source.
- `class`: Additional model classification for text generation.
- `test date`: Test date for text generation.

The V1 analysis uses only the `text_generation` subset.

The pipeline multiplies `total_gpu_energy` by 1,000 to calculate `energy_wh_per_1k`, following the source leaderboard's reporting convention.

This metric represents GPU inference energy, not total datacenter energy consumption.

The three tasks must not be assumed to have equivalent workloads or inference conditions.

### 3.2 Open LLM Leaderboard

The validated local dataset contains **4,576 records and 34 columns**.

Relevant fields include:

| Column | Description |
|---|---|
| `Model` | Model identifier |
| `fullname` | Full model name |
| `Model sha` | Model revision identifier |
| `#Params (B)` | Number of parameters in billions |
| `Precision` | Evaluation precision |
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

## 4. Data Acquisition and Processing Pipeline

### 4.1 Data Acquisition

AI Energy Score data is downloaded with:

```bash
python -m scripts.download_data
```

The script retrieves three CSV files from the Hugging Face Space `AIEnergyScore/Leaderboard` and saves them under `data/raw/ai_energy_score/`.

Existing local files are reused.

Open LLM Leaderboard data is loaded by `load_quality_data()`.

If `data/raw/open_llm_leaderboard/open_llm_leaderboard.csv` exists, it is reused. Otherwise, the dataset is downloaded from Hugging Face and saved locally.

Both acquisition methods use the latest available source revision unless a local copy already exists.

### 4.2 Processing Stages

1. **Ingestion:** Load the source CSV files using Python and pandas.
2. **Cleaning:** Standardize energy and quality records.
3. **Model Matching:** Join compatible model identifiers across sources.
4. **Storage:** Export the processed dataset and load it into DuckDB.
5. **SQL Analytics:** Compute analytical metrics and Pareto frontiers.
6. **Visualization:** Export model-level and benchmark-level datasets for Tableau.

### 4.3 Model Matching and Submission Selection

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

### 4.4 Generated Outputs

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
| Model identity | Name-based matching; exact revisions require further validation |
| Evaluation tasks | Different protocols across sources |
| Inference hardware | Not fully documented in the local source schema |
| Batch size and precision | Not fully documented across both sources |
| Prompt and output lengths | Not available in the inspected source columns |
| Performance metrics | Analyzed separately by benchmark |
| Energy measurement scope | GPU energy only; experimental boundaries require further documentation |
| Measurement dates | Partially available |
| Controlled experimental comparison | Not established |

**Interpretation:** The merged dataset supports exploratory energy-performance analysis. It does not demonstrate how the same models would perform under identical hardware, prompts, batch sizes, or inference configurations.

## 6. Analytical Metrics

### Energy Consumption

The analytical dashboard uses:

`energy_wh_per_1k`

The pipeline calculates:

`energy_wh_per_1k = total_gpu_energy * 1000`

The metric follows AI Energy Score's GPU energy reporting convention, expressed as Wh per 1,000 queries.

Lower energy values are preferable.

### Model Performance

The analysis uses three performance indicators:

- **MMLU-Pro:** Knowledge and reasoning.
- **IFEval:** Instruction-following.
- **Average Score:** Aggregate leaderboard performance.

Higher performance values are preferable.

### Pareto Optimality

A model is Pareto-optimal when no other evaluated model performs at least as well on both energy and performance, with a strict improvement in at least one objective.

Pareto frontiers are computed separately for each performance indicator.

Models with missing energy or performance values are excluded from Pareto-optimal classification.

## 7. Validated Results

The following results were reproduced from a fresh Git clone.

| Indicator | Result |
|---|---:|
| Matched models | 38 |
| Model-benchmark observations | 114 |
| Performance indicators | 3 |
| SQL transformation scripts | 5 |
| Automated tests passed | 5 |

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
- Git
- Internet connection for the initial dataset downloads
- Dependencies listed in `requirements.txt`

### Run from a Fresh Clone

```bash
git clone https://github.com/EyaWal/ai-ecolens.git
cd ai-ecolens

python3 -m venv .venv
source .venv/bin/activate

python -m pip install -r requirements.txt

python -m scripts.download_data
python -m scripts.run_pipeline
python -m scripts.run_sql

python -m pytest -q
```

### Fresh-Clone Validation

The pipeline was successfully executed from a fresh Git clone.

Validation confirmed:

- Successful source dataset acquisition.
- Successful Python processing and DuckDB database creation.
- Execution of all five SQL transformation scripts.
- Export of both Tableau-ready datasets.
- Reproduction of 38 matched models and 114 model-benchmark observations.
- Reproduction of the expected Pareto-optimal counts.
- Five automated tests passing.

### Remaining Reproducibility Limitations

Raw datasets are excluded from Git and downloaded from public sources.

The current implementation does not pin source dataset revisions or exact dependency versions.

As a result, future downloads may produce different data and analytical results.

Dataset licenses, extraction timestamps, and exact upstream revisions remain to be documented.

## 9. Scientific Limitations

- Energy and performance results originate from different benchmark protocols.
- Model names may refer to different revisions or configurations.
- Hardware and workload differences can influence energy consumption.
- Normalization does not automatically make independent experiments comparable.
- GPU energy consumption is not equivalent to total system energy or lifecycle carbon emissions.
- Pareto optimality depends on the available models and selected metrics.
- The analysis should not be used as a definitive ranking of AI models' environmental impact.

## 10. Future Improvements

- [x] Document source dataset acquisition methods.
- [x] Automate source dataset acquisition.
- [x] Verify the energy normalization implemented in the pipeline.
- [x] Validate pipeline execution from a fresh Git clone.
- [x] Implement automated ingestion tests independent of raw datasets.
- [ ] Pin source dataset revisions and record extraction timestamps.
- [ ] Verify dataset licenses and redistribution conditions.
- [ ] Improve model revision matching.
- [ ] Add automated data-quality checks.
- [ ] Document experimental hardware and workload conditions.
- [ ] Validate energy measurement boundaries and experimental conditions.
- [ ] Investigate inference cost and carbon estimation using explicit assumptions.

---

**Project:** AI EcoLens  
**Status:** V1 — Analytics pipeline reproduced and Tableau dashboard published.
