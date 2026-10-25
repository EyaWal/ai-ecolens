# AI EcoLens 🌱

**AI Model Performance, Cost & Environmental Impact Analytics**

AI EcoLens is a data engineering and Tableau analytics project exploring trade-offs between AI model quality, inference energy consumption, cost, and estimated carbon emissions.

## Research question
How can organizations select AI models for specific use cases while balancing quality, cost, energy use and environmental impact?

## Scope (V1)
- Audit public benchmark datasets and their licenses.
- Compare only measurements with compatible workloads and experimental conditions.
- Build reproducible ingestion, validation and analytics in Python + DuckDB.
- Create Tableau dashboards: Model Explorer and Use Case Simulator.
- Clearly label measured versus estimated values.

## Data sources to evaluate
- [AI Energy Score](https://huggingface.github.io/AIEnergyScore/)
- [ML.ENERGY](https://ml.energy/)
- [Artificial Analysis](https://artificialanalysis.ai/)

> Data coverage, access conditions and licenses must be verified before ingestion.

## Setup
Requires Python 3.11+.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
```

## Structure
- `docs/`: source audit and methodology
- `data/`: raw, interim and processed datasets (data files ignored by Git)
- `src/ai_ecolens/`: ingestion, processing and analytics code
- `sql/`: SQL transformations
- `tests/`: automated checks
- `tableau/`: workbook files and dashboard documentation

## Scientific guardrails
- Keep source, model revision, hardware, task, batch size, input/output lengths and measurement boundaries where available.
- Do not assume benchmark scores from different datasets are interchangeable.
- Carbon estimates depend on electricity carbon intensity and measurement scope; they are not full lifecycle footprints.
- Do not impute missing energy measurements as zero.

## Roadmap
1. Source discovery and compatibility matrix
2. Ingestion and validation
3. SQL marts and initial Tableau dashboard
4. Model Explorer
5. Use Case Simulator
6. Testing, documentation and publishing

## Status
🚧 Week 1 — Data discovery.
