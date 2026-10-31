
from pathlib import Path

import pandas as pd

from src.ai_ecolens.ingestion.energy import load_energy_data
from src.ai_ecolens.ingestion.quality import load_quality_data


def test_load_energy_data(tmp_path: Path):
    """Test energy ingestion using temporary CSV files."""

    data_dir = tmp_path / "ai_energy_score"
    data_dir.mkdir()

    tasks = [
        "text_generation",
        "summarization",
        "question_answering",
    ]

    for task in tasks:
        pd.DataFrame({
            "model": ["test/model-a"],
            "total_gpu_energy": [0.01],
            "energy_score": [5],
        }).to_csv(data_dir / f"{task}.csv", index=False)

    result = load_energy_data(data_dir)

    assert len(result) == 3
    assert set(result["task"]) == set(tasks)
    assert "model" in result.columns
    assert "total_gpu_energy" in result.columns


def test_load_quality_data(tmp_path: Path):
    """Test loading the quality dataset from a local CSV."""

    data_dir = tmp_path / "open_llm_leaderboard"
    data_dir.mkdir()

    pd.DataFrame({
        "fullname": ["test/model-a", "test/model-b"],
        "Average ⬆️": [40.0, 50.0],
        "MMLU-PRO": [35.0, 45.0],
        "IFEval": [60.0, 70.0],
    }).to_csv(
        data_dir / "open_llm_leaderboard.csv",
        index=False,
    )

    result = load_quality_data(data_dir)

    assert len(result) == 2
    assert result["fullname"].nunique() == 2
