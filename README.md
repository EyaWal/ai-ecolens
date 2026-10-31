# AI EcoLens 🌱

### Exploring the trade-off between AI model performance and energy consumption

**Can we get high-quality AI results without using more energy than necessary?**

AI EcoLens is an end-to-end data engineering and analytics project that combines public AI inference energy measurements with language-model benchmark results. It helps explore which models offer compelling **performance–energy trade-offs**, rather than assuming that the highest-scoring model is always the best choice.

**[Explore the interactive dashboard on Tableau Public](https://public.tableau.com/views/AIEcoLensAIPerformanceEnergyEfficiency/AIEcoLensOverview)** · [Data sources](docs/data_sources.md) · [Methodology](docs/methodology.md)

![AI EcoLens dashboard preview](assets/dashboard-demo.gif)

> **Project status:** V1 completed — interactive dashboard published, data pipeline reproduced from a fresh clone, and 5 automated tests passing.

## Why I Built This

As AI models become more powerful and widely used, I started questioning whether the additional energy consumed by a more powerful model always translates into a meaningful improvement in results.

I wanted to explore a simple question: **How can we find the best balance between model quality and energy consumption?**

My goal was not to identify only the highest-performing model or the model using the least energy. Instead, I wanted to compare both dimensions and understand the compromises involved in choosing an AI model.

In the longer term, I would like to make this analysis useful for real-world needs—for example, choosing models for studying, writing, or question answering. **V1 is the analytical foundation for that vision:** it compares models using three available performance indicators, rather than making task-specific recommendations.

## What I Built

I developed a reproducible workflow that turns two independent public data sources into an interactive comparison dashboard.

| Stage | What I implemented | Why it matters |
|---|---|---|
| **1. Data acquisition** | Python ingestion scripts to retrieve AI Energy Score CSVs and Open LLM Leaderboard evaluations from Hugging Face | Makes the project runnable without manually collecting source files |
| **2. Cleaning and matching** | pandas transformations, normalized model identifiers, and rules for selecting among multiple benchmark submissions | Makes independently published energy and performance records comparable at the model-name level |
| **3. Analytics** | DuckDB SQL views for model metrics, benchmark-level comparisons, and Pareto-optimality analysis | Makes it possible to explore two competing objectives without inventing a universal combined score |
| **4. Visualization** | Tableau-ready CSV exports and an interactive Tableau Public dashboard | Turns the analytical results into an explorable visual comparison |
| **5. Validation** | pytest tests and an end-to-end run from a fresh Git clone | Checks that the workflow works beyond my local development environment |

### The dashboard answers three questions

- **Performance vs. energy:** Which models offer interesting trade-offs between benchmark scores and GPU inference energy?
- **Model size vs. energy:** How does reported model size relate to measured energy consumption within the available data?
- **Benchmark sensitivity:** How does the set of Pareto-optimal models change when switching between **MMLU-Pro**, **IFEval**, and **Average Score**?

The dashboard supports interactive filtering and model exploration. It **does not yet** recommend models for specific user activities such as studying or writing.

## Engineering Challenges & Decisions

The most important part of the project was not drawing the charts—it was preparing and interpreting data from different sources.

### 1. Matching models across independent datasets

**Challenge:** AI Energy Score and Open LLM Leaderboard do not share a guaranteed common model identifier.

**Approach:** I standardized model names by trimming whitespace and converting text to lowercase, then matched AI Energy Score's `model` field to the leaderboard's `fullname` field.

**Trade-off:** Name-based matching is practical, but it cannot prove that both sources evaluated exactly the same model revision or configuration.

### 2. Handling multiple evaluations of the same model

**Challenge:** A model can appear in several leaderboard submissions.

**Approach:** I defined a deterministic selection rule: prioritize `float16`, then `bfloat16`, then other or unspecified precisions; within the same priority, select the most recent submission.

**Trade-off:** This makes the pipeline consistent, but it is a data-selection rule—not proof that the selected evaluation is experimentally identical to the energy measurement.

### 3. Comparing performance with energy consumption

**Challenge:** Higher benchmark scores are desirable, while lower energy consumption is desirable. A single weighted score would require subjective assumptions about how much one objective matters relative to the other.

**Approach:** I used **Pareto analysis**. A model is Pareto-optimal if no other model in the comparison performs at least as well on both objectives and strictly better on at least one.

**Learning:** There is not necessarily one universally best model; the useful set of candidates can change with the benchmark and the user's priorities.

### 4. Making the pipeline reproducible

**Challenge:** The raw datasets are excluded from Git, so an initial version of the workflow depended on files already present locally.

**Approach:** I added source-data download steps, documented the execution sequence, and updated tests to use temporary sample data rather than local raw CSVs.

**Validation:** I ran the full workflow from a fresh clone and confirmed that all five automated tests passed.

## Results

The validated V1 pipeline produced:

| Indicator | Result |
|---|---:|
| Matched AI models | **38** |
| Model–benchmark observations | **114** |
| Performance indicators | **3** |
| SQL transformation scripts | **5** |
| Automated tests | **5/5 passed** |

### Pareto-optimal models by benchmark

| Benchmark | Pareto-optimal models |
|---|---:|
| MMLU-Pro | **10** |
| IFEval | **9** |
| Average Score | **15** |

**Main takeaway:** The Pareto-optimal set changes depending on which performance indicator is selected. This reinforces the idea that a model's attractiveness depends on how performance is defined—not just on its energy consumption.

These counts describe the **38 matched models in this dataset**, not all AI models available worldwide. They may change if the upstream datasets change.

### Explore the dashboard

**[Open AI EcoLens on Tableau Public](https://public.tableau.com/views/AIEcoLensAIPerformanceEnergyEfficiency/AIEcoLensOverview)**

When reading the energy-versus-performance view, look for models that combine **lower energy** with **higher scores**. Pareto highlighting helps identify candidates for which no other model in the comparison set is better on both objectives.

## What I Learned

AI EcoLens taught me that a model comparison is only as meaningful as the data and assumptions behind it.

- **Data engineering:** Bringing together independent public datasets requires careful cleaning, identity matching, and handling of duplicate evaluations.
- **Analytical thinking:** A Pareto frontier is useful when objectives conflict and there is no defensible universal weighting between them.
- **Data visualization:** A technically correct chart still needs clear labels, context, and explanations to be useful to someone seeing the results for the first time.
- **Reproducibility:** A project is more useful when another person can install it, retrieve its inputs, execute the transformations, and run its tests.
- **Scientific caution:** GPU inference energy is an informative metric, but it is not a complete measure of a model's environmental footprint.

## How It Works

```text
AI Energy Score                  Open LLM Leaderboard
       |                                  |
       +----------------+-----------------+
                        |
                        v
                 Python / pandas
             Download, clean, match
                        |
                        v
                Processed CSV
         energy_quality_comparison.csv
                        |
                        v
                   DuckDB + SQL
           Analytical views + Pareto
                        |
                        v
              Tableau-ready exports
       tableau_model_metrics.csv
       tableau_benchmark_metrics.csv
                        |
                        v
                   Tableau Public
               Interactive dashboard
```

### Tech stack

**Python · pandas · NumPy · Hugging Face Hub / Datasets · DuckDB · SQL · Tableau Public · pytest · Git / GitHub**

### Data sources

**[AI Energy Score](https://huggingface.github.io/AIEnergyScore/)** provides GPU inference energy measurements, retrieved from the Hugging Face Space `AIEnergyScore/Leaderboard` for text generation, summarization, and question answering.

**[Open LLM Leaderboard](https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard)** provides language-model evaluation results, retrieved from the Hugging Face dataset `open-llm-leaderboard/contents`.

For schemas, matching assumptions, and source limitations, see **[Data Sources & Compatibility Audit](docs/data_sources.md)**.

### Metrics

| Metric | Meaning |
|---|---|
| GPU Energy (Wh/1K queries) | GPU inference energy indicator based on AI Energy Score's reporting convention |
| MMLU-Pro | Knowledge and reasoning benchmark |
| IFEval | Instruction-following benchmark |
| Average Score | Aggregate leaderboard performance indicator |
| Model Size (B) | Number of model parameters, in billions |
| Pareto optimality | A model is not dominated by another on both selected objectives |

The pipeline calculates `energy_wh_per_1k = total_gpu_energy * 1000` following the source reporting convention. This is **not** a measurement of total datacenter electricity use or lifecycle environmental impact.

## Run the Project Locally

**Prerequisites:** Python 3.11+, Git, and internet access for the initial data downloads.

### 1. Clone and set up the environment

```bash
git clone https://github.com/EyaWal/ai-ecolens.git
cd ai-ecolens

python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### 2. Download the energy dataset

```bash
python -m scripts.download_data
```

This downloads `text_generation.csv`, `summarization.csv`, and `question_answering.csv` into `data/raw/ai_energy_score/`.

### 3. Run the processing and SQL pipeline

```bash
python -m scripts.run_pipeline
python -m scripts.run_sql
```

If needed, the processing pipeline automatically downloads Open LLM Leaderboard evaluations into `data/raw/open_llm_leaderboard/`.

Generated outputs include:

```text
data/processed/energy_quality_comparison.csv
data/warehouse/ai_ecolens.duckdb
data/analytics/tableau_model_metrics.csv
data/analytics/tableau_benchmark_metrics.csv
```

### 4. Run the tests

```bash
python -m pytest -q
```

The tests use temporary sample data and do not require the full raw datasets.

> **Reproducibility note:** The pipeline was successfully executed from a fresh clone, but upstream dataset revisions and exact dependency versions are not fully pinned. Future downloads may produce different results.

## Project Structure

<details>
<summary>Show repository layout</summary>

```text
ai-ecolens/
├── assets/
│   └── dashboard-demo.gif
├── data/
│   ├── raw/                 # Downloaded source data (Git-ignored)
│   ├── interim/
│   ├── processed/
│   ├── warehouse/
│   └── analytics/
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

</details>

## Limitations

- Energy and quality measurements come from **different evaluation protocols**, potentially using different hardware, precision, workloads, and model revisions.
- Name-based matching does not guarantee exact model or configuration identity.
- GPU inference energy does **not** capture training energy, datacenter overhead, carbon intensity, water use, or full lifecycle environmental impact.
- Pareto optimality is relative to the available models and the selected benchmark; it is **not** a universal environmental ranking.
- Dataset revisions and exact dependency versions are not pinned, so future results may differ.
- The current dashboard compares benchmark indicators; it does **not** directly validate model suitability for individual real-world tasks.

## What's Next

AI EcoLens V1 is a starting point, not a finished model recommendation system.

- [x] Build an ingestion and matching pipeline for two public AI datasets
- [x] Implement DuckDB analytics and benchmark-specific Pareto comparisons
- [x] Publish an interactive Tableau dashboard
- [x] Automate data acquisition and validate a fresh-clone run
- [x] Add automated tests (5 passing)
- [ ] Improve dashboard explanations and storytelling for nontechnical visitors
- [ ] Strengthen model revision matching and data-quality checks
- [ ] Pin source dataset revisions for long-term reproducibility
- [ ] Explore developer-level comparisons with clear dataset coverage limits
- [ ] Investigate carbon estimates where appropriate data and assumptions are available
- [ ] Explore **use-case-based model selection**, supported by task-relevant evaluations

**Long-term vision:** Help people choose AI models that provide the quality they need while avoiding unnecessary inference energy consumption.
