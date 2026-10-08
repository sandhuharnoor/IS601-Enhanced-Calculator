
"""Tests for calculator history management."""

from unittest.mock import patch

import pandas as pd
import pytest

from app.calculation import Calculation
from app.exceptions import HistoryError
from app.history import HistoryManager, COLUMNS


@pytest.fixture
def history(tmp_path):
    return HistoryManager(
        filename=tmp_path / "history.csv",
        max_history=100,
    )


@pytest.fixture
def sample_calculation():
    return Calculation.create("add", 10, 5)


def test_history_initialization(history):
    assert history.data.empty
    assert list(history.data.columns) == COLUMNS
    assert history.max_history == 100


def test_add_calculation(history, sample_calculation):
    history.add(sample_calculation)

    assert len(history.data) == 1
    assert history.data.iloc[0]["operation"] == "add"
    assert history.data.iloc[0]["result"] == 15


def test_add_multiple_calculations(history):
    history.add(Calculation.create("add", 10, 5))
    history.add(Calculation.create("multiply", 4, 3))

    assert len(history.data) == 2


def test_max_history_limit(tmp_path):
    history = HistoryManager(
        filename=tmp_path / "history.csv",
        max_history=2,
    )

    history.add(Calculation.create("add", 1, 1))
    history.add(Calculation.create("add", 2, 2))
    history.add(Calculation.create("add", 3, 3))

    assert len(history.data) == 2
    assert history.data.iloc[0]["result"] == 4
    assert history.data.iloc[1]["result"] == 6


def test_clear_history(history, sample_calculation):
    history.add(sample_calculation)
    history.clear()

    assert history.data.empty
    assert list(history.data.columns) == COLUMNS


def test_save_history(history, sample_calculation):
    history.add(sample_calculation)
    history.save()

    assert history.filename.exists()


def test_save_creates_parent_directory(tmp_path):
    filename = tmp_path / "nested" / "folder" / "history.csv"
    history = HistoryManager(filename)

    history.save()

    assert filename.exists()


def test_load_history(history, sample_calculation):
    history.add(sample_calculation)
    history.save()

    restored = HistoryManager(history.filename)

    assert restored.load() is True
    assert len(restored.data) == 1
    assert restored.data.iloc[0]["result"] == 15


def test_load_missing_file(history):
    assert history.load() is False


def test_load_invalid_columns(tmp_path):
    filename = tmp_path / "invalid.csv"
    pd.DataFrame({"wrong": [1]}).to_csv(filename, index=False)

    history = HistoryManager(filename)

    with pytest.raises(HistoryError, match="invalid columns"):
        history.load()


def test_load_respects_max_history(tmp_path):
    filename = tmp_path / "history.csv"
    history = HistoryManager(filename)

    for number in range(5):
        history.add(Calculation.create("add", number, 1))

    history.save()

    limited_history = HistoryManager(filename, max_history=2)

    assert limited_history.load() is True
    assert len(limited_history.data) == 2


def test_get_records(history, sample_calculation):
    history.add(sample_calculation)

    records = history.get_records()

    assert isinstance(records, list)
    assert len(records) == 1
    assert records[0]["operation"] == "add"
    assert records[0]["result"] == 15


def test_restore_history(history, sample_calculation):
    history.add(sample_calculation)
    records = history.get_records()

    history.clear()
    history.restore(records)

    assert len(history.data) == 1
    assert history.data.iloc[0]["result"] == 15


def test_display_empty_history(history):
    assert history.display() == "No calculations in history."


def test_display_history(history, sample_calculation):
    history.add(sample_calculation)

    output = history.display()

    assert "add" in output
    assert "15" in output


def test_save_error(history):
    with patch.object(
        pd.DataFrame,
        "to_csv",
        side_effect=OSError("Disk error"),
    ):
        with pytest.raises(HistoryError, match="Unable to save"):
            history.save()


def test_load_error(tmp_path):
    filename = tmp_path / "history.csv"
    filename.write_text("test", encoding="utf-8")

    history = HistoryManager(filename)

    with patch(
        "app.history.pd.read_csv",
        side_effect=OSError("Read error"),
    ):
        with pytest.raises(HistoryError, match="Unable to load"):
            history.load()


def test_load_parser_error(tmp_path):
    filename = tmp_path / "history.csv"
    filename.write_text("test", encoding="utf-8")

    history = HistoryManager(filename)

    with patch(
        "app.history.pd.read_csv",
        side_effect=pd.errors.ParserError("Invalid CSV"),
    ):
        with pytest.raises(HistoryError, match="Unable to load"):
            history.load()
