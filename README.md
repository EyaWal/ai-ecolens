
# AI EcoLens 🌱

**AI Model Performance & Energy Efficiency Analytics**

AI EcoLens is an end-to-end data engineering and analytics project exploring the trade-offs between AI model performance and inference energy consumption.

It combines public benchmark datasets, Python data processing, DuckDB SQL analytics, Pareto frontier analysis, and interactive Tableau visualizations.

**Research question:** How can we identify AI models that deliver competitive performance while minimizing inference energy consumption?

## 📊 Live Dashboard

**[Explore AI EcoLens on Tableau Public](https://public.tableau.com/views/AIEcoLensAIPerformanceEnergyEfficiency/AIEcoLensOverview)**

### Dashboard Preview

![AI EcoLens Interactive Dashboard](assets/dashboard-demo.gif)

The interactive dashboard includes:

- **Energy vs. Performance:** Analyze inference energy consumption against model benchmark scores.
- **Energy vs. Model Size:** Explore relationships between model size and energy consumption.
- **Dynamic Benchmark Selection:** Compare MMLU-Pro, IFEval, and Average Score.
- **Pareto Frontier Analysis:** Identify non-dominated models based on energy and performance.
- **Model Comparison:** Explore individual models through interactive filtering and highlighting.
- **Methodology & Data Sources:** Review the analytical approach, metrics, and limitations.

## 🎯 Project Objectives

1. Integrate public AI model energy and performance datasets.
2. Clean, standardize, and match model records across sources.
3. Build an analytical data pipeline using Python and DuckDB.
4. Evaluate energy-performance trade-offs using Pareto optimization.
5. Export structured analytical datasets for Tableau.
6. Communicate results through an interactive dashboard.

## 🗂️ Data Sources

**[AI Energy Score](https://huggingface.github.io/AIEnergyScore/)**

GPU inference energy measurements retrieved from the Hugging Face Space `AIEnergyScore/Leaderboard`.

**[Open LLM Leaderboard](https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard)**

Language-model performance evaluations retrieved from the Hugging Face dataset `open-llm-leaderboard/contents`.

The current analytical dataset contains **38 matched models** and **114 model-benchmark observations**.

Source CSV files are stored locally under `data/raw/` and excluded from Git version control.

AI Energy Score files are downloaded using `scripts/download_data.py`. Open LLM Leaderboard evaluations are downloaded automatically during pipeline execution when no local CSV is available.

Energy and performance measurements originate from different evaluation protocols. Results are intended for exploratory comparison rather than controlled experimental benchmarking.

For additional details, see [Data Sources & Compatibility Audit](docs/data_sources.md).

## 🏗️ Data Architecture

```text
AI Energy Score        Open LLM Leaderboard
       |                       |
       +-----------+-----------+
                   |
                   v
            Python / pandas
       Ingestion and validation
       Cleaning and model matching
                   |
                   v
           Processed Dataset
    energy_quality_comparison.csv
                   |
                   v
                DuckDB
        Analytical SQL views
       Benchmark-specific Pareto
                   |
                   v
           Tableau CSV Exports
       tableau_model_metrics.csv
     tableau_benchmark_metrics.csv
                   |
                   v
             Tableau Public
        Interactive dashboards
```

### Project Structure

```text
ai-ecolens/
├── assets/
│   └── dashboard-demo.gif
├── data/
│   ├── raw/              # Source datasets (Git-ignored)
│   ├── interim/          # Intermediate data
│   ├── processed/        # Cleaned and merged datasets
│   ├── warehouse/        # Local DuckDB database
│   └── analytics/        # Tableau-ready CSV exports
├── docs/
│   ├── data_sources.md
│   └── methodology.md
├── notebooks/
│   └── 01_energy_data_exploration.ipynb
├── scripts/
│   ├── download_data.py
│   ├── run_pipeline.py
│   ├── run_sql.py
│   └── check_database.py
├── sql/
│   ├── 01_model_analysis.sql
│   ├── 02_pareto_frontier.sql
│   ├── 03_dashboard_dataset.sql
│   ├── 04_benchmark_pareto.sql
│   └── 05_benchmark_dashboard.sql
├── src/ai_ecolens/
│   ├── ingestion/
│   ├── processing/
│   ├── storage/
│   └── analytics/
├── tests/
│   ├── test_ingestion.py
│   └── test_metrics.py
├── requirements.txt
├── pyproject.toml
└── README.md
```

## 📐 Metrics & Methodology

| Metric | Description |
|---|---|
| GPU Energy (Wh/1K queries) | GPU inference energy indicator following AI Energy Score's reporting convention |
| MMLU-Pro | Knowledge and reasoning benchmark |
| IFEval | Instruction-following benchmark |
| Average Score | Aggregate leaderboard performance metric |
| Model Size (B) | Number of parameters in billions |
| Pareto Optimality | Non-dominated energy-performance trade-off |

### Energy Normalization

The pipeline calculates:

`energy_wh_per_1k = total_gpu_energy * 1000`

The metric follows AI Energy Score's GPU energy reporting convention and does not represent total datacenter energy consumption.

### Model Matching

Model identifiers are normalized by trimming whitespace and converting text to lowercase.

The pipeline matches AI Energy Score's `model` field with Open LLM Leaderboard's `fullname` field.

When multiple quality evaluations exist, the pipeline prioritizes:

1. `float16` precision
2. `bfloat16` precision
3. Other or unspecified precisions

Within the same precision priority, the most recent submission is preferred.

Name-based matching does not guarantee identical model revisions or inference configurations across sources.

### Pareto Frontier Analysis

The analysis considers two competing objectives:

- **Minimize** inference GPU energy consumption.
- **Maximize** model performance.

A model is Pareto-optimal when no other model in the comparison set performs at least as well on both objectives and strictly better on at least one.

Pareto analysis is performed separately for MMLU-Pro, IFEval, and Average Score.

## 📈 Key Results

The validated pipeline produced:

| Indicator | Result |
|---|---:|
| Matched AI models | 38 |
| Model-benchmark observations | 114 |
| SQL transformation scripts | 5 |
| Automated tests passed | 5/5 |

### Pareto-Optimal Models by Benchmark

| Benchmark | Pareto-Optimal Models |
|---|---:|
| MMLU-Pro | 10 |
| IFEval | 9 |
| Average Score | 15 |

These results show that the set of non-dominated models changes according to the selected performance benchmark.

Pareto optimality is relative to the evaluated models and metrics; it does not establish that a model is universally more energy-efficient.

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Programming | Python |
| Data Processing | pandas, NumPy |
| Data Acquisition | Hugging Face Hub, Hugging Face Datasets |
| Analytical Database | DuckDB |
| Data Transformations | SQL |
| Data Exploration | Jupyter Notebook |
| Visualization | Tableau Public |
| Testing | pytest |
| Version Control | Git, GitHub |

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Git
- Internet connection for the initial dataset downloads

### 1. Clone the repository

```bash
git clone https://github.com/EyaWal/ai-ecolens.git
cd ai-ecolens
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Download AI Energy Score data

```bash
python -m scripts.download_data
```

This downloads three CSV files into `data/raw/ai_energy_score/`:

- `text_generation.csv`
- `summarization.csv`
- `question_answering.csv`

The Open LLM Leaderboard dataset is downloaded automatically during pipeline execution if no local copy exists.

### 5. Run the pipeline

```bash
python -m scripts.run_pipeline
python -m scripts.run_sql
```

The pipeline creates:

```text
data/processed/energy_quality_comparison.csv
data/warehouse/ai_ecolens.duckdb
data/analytics/tableau_model_metrics.csv
data/analytics/tableau_benchmark_metrics.csv
```

### 6. Run automated tests

```bash
python -m pytest -q
```

The test suite uses temporary sample data and does not require downloading the source datasets.

### Reproducibility Validation

The pipeline was successfully reproduced from a fresh Git clone with the following results:

- 38 matched models
- 114 model-benchmark observations
- 10 Pareto-optimal models for MMLU-Pro
- 9 Pareto-optimal models for IFEval
- 15 Pareto-optimal models for Average Score
- 5 automated tests passed

**Note:** Source dataset revisions and exact dependency versions are not pinned. Future upstream updates may change the results.

## ⚠️ Limitations

- Energy and performance measurements originate from different benchmark protocols.
- Model matching across independent datasets does not guarantee identical model revisions.
- Hardware, workload, precision, and evaluation configurations may differ.
- GPU energy measurements do not represent total environmental or lifecycle impact.
- Pareto results depend on the available models and selected metrics.
- Source dataset revisions are not pinned, limiting exact long-term reproducibility.
- The analysis should not be interpreted as a definitive environmental ranking of AI models.

## 🗺️ Roadmap

- [x] Explore public AI benchmark datasets
- [x] Build Python ingestion and cleaning pipeline
- [x] Match energy and performance datasets
- [x] Implement DuckDB analytical transformations
- [x] Compute benchmark-specific Pareto frontiers
- [x] Export Tableau-ready datasets
- [x] Publish interactive Tableau dashboard
- [x] Automate source dataset acquisition
- [x] Document dataset sources and processing
- [x] Validate the pipeline from a fresh Git clone
- [x] Run automated tests successfully (5/5)
- [ ] Pin dataset revisions for long-term reproducibility
- [ ] Expand automated data-quality checks
- [ ] Improve model revision matching
- [ ] Investigate inference cost and carbon estimation
- [ ] Explore a use-case-based model selection simulator

## 📌 Project Status

**V1 — Interactive Analytics Dashboard Published & Pipeline Reproduced**

AI EcoLens includes a working Python data pipeline, DuckDB SQL analytics, benchmark-specific Pareto analysis, and a published interactive Tableau dashboard.

The complete pipeline has been successfully executed from a fresh Git clone.

Future work will focus on stronger scientific comparability, dataset versioning, and additional decision-support capabilities.
