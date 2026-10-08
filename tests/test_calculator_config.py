
"""Tests for calculator configuration."""

import pytest

from app.calculator_config import CalculatorConfig
from app.exceptions import ConfigurationError


def test_default_configuration(monkeypatch):
    monkeypatch.setattr(
        "app.calculator_config.load_dotenv",
        lambda: None
    )

    monkeypatch.delenv("CALCULATOR_HISTORY_FILE", raising=False)
    monkeypatch.delenv("CALCULATOR_AUTO_SAVE", raising=False)
    monkeypatch.delenv("CALCULATOR_MAX_HISTORY", raising=False)

    config = CalculatorConfig.from_env()

    assert config.history_file == "history.csv"
    assert config.auto_save is True
    assert config.max_history == 1000


def test_custom_configuration(monkeypatch):
    monkeypatch.setattr(
        "app.calculator_config.load_dotenv",
        lambda: None
    )

    monkeypatch.setenv("CALCULATOR_HISTORY_FILE", "custom.csv")
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "false")
    monkeypatch.setenv("CALCULATOR_MAX_HISTORY", "500")

    config = CalculatorConfig.from_env()

    assert config.history_file == "custom.csv"
    assert config.auto_save is False
    assert config.max_history == 500


def test_invalid_auto_save(monkeypatch):
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "invalid")

    with pytest.raises(
        ConfigurationError,
        match="CALCULATOR_AUTO_SAVE"
    ):
        CalculatorConfig.from_env()


def test_invalid_max_history_string(monkeypatch):
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "true")
    monkeypatch.setenv("CALCULATOR_MAX_HISTORY", "abc")

    with pytest.raises(
        ConfigurationError,
        match="must be an integer"
    ):
        CalculatorConfig.from_env()


@pytest.mark.parametrize("value", ["0", "-1", "-100"])
def test_invalid_max_history_value(monkeypatch, value):
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "true")
    monkeypatch.setenv("CALCULATOR_MAX_HISTORY", value)

    with pytest.raises(
        ConfigurationError,
        match="must be positive"
    ):
        CalculatorConfig.from_env()


def test_empty_history_file(monkeypatch):
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "true")
    monkeypatch.setenv("CALCULATOR_MAX_HISTORY", "100")
    monkeypatch.setenv("CALCULATOR_HISTORY_FILE", "   ")

    with pytest.raises(
        ConfigurationError,
        match="History file cannot be empty"
    ):
        CalculatorConfig.from_env()


def test_direct_configuration():
    config = CalculatorConfig(
        history_file="test.csv",
        auto_save=False,
        max_history=50
    )

    assert config.history_file == "test.csv"
    assert config.auto_save is False
    assert config.max_history == 50
