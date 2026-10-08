
"""Tests for the calculator and interactive REPL."""

from unittest.mock import patch

import pytest

from app.calculator_config import CalculatorConfig
from app.calculator_repl import (
    Calculator,
    HistoryObserver,
    repl,
)


@pytest.fixture
def calculator(tmp_path):
    config = CalculatorConfig(
        history_file=str(tmp_path / "history.csv"),
        auto_save=False,
        max_history=100,
    )
    return Calculator(config)


def test_calculator_initialization(calculator):
    assert calculator.history.data.empty
    assert len(calculator.observers) == 1


def test_calculate(calculator):
    result = calculator.calculate("add", 10, 5)

    assert result == 15
    assert len(calculator.history.data) == 1


def test_calculate_multiple_operations(calculator):
    assert calculator.calculate("subtract", 10, 5) == 5
    assert calculator.calculate("multiply", 10, 5) == 50
    assert calculator.calculate("divide", 10, 5) == 2
    assert calculator.calculate("power", 2, 3) == 8
    assert calculator.calculate("root", 16, 2) == 4


def test_clear(calculator):
    calculator.calculate("add", 10, 5)
    calculator.clear()

    assert calculator.history.data.empty


def test_undo(calculator):
    calculator.calculate("add", 10, 5)

    assert calculator.undo() is True
    assert calculator.history.data.empty


def test_undo_empty(calculator):
    assert calculator.undo() is False


def test_redo(calculator):
    calculator.calculate("add", 10, 5)
    calculator.undo()

    assert calculator.redo() is True
    assert len(calculator.history.data) == 1


def test_redo_empty(calculator):
    assert calculator.redo() is False


def test_save_and_load(calculator):
    calculator.calculate("add", 10, 5)
    calculator.save()
    calculator.clear()

    assert calculator.load() is True
    assert len(calculator.history.data) == 1


def test_load_missing_file(calculator):
    assert calculator.load() is False


def test_help(calculator):
    output = calculator.help()

    assert "Available Commands" in output
    assert "add" in output
    assert "undo" in output
    assert "exit" in output


def test_history_observer_disabled(calculator):
    observer = HistoryObserver(calculator.history, enabled=False)

    with patch.object(calculator.history, "save") as mock_save:
        observer.update("calculation")

    mock_save.assert_not_called()


def test_history_observer_enabled(calculator):
    observer = HistoryObserver(calculator.history, enabled=True)

    with patch.object(calculator.history, "save") as mock_save:
        observer.update("calculation")

    mock_save.assert_called_once()


def test_notify(calculator):
    with patch.object(
        calculator.observers[0], "update"
    ) as mock_update:
        calculator.notify("calculation")

    mock_update.assert_called_once_with("calculation")


def test_repl_exit(capsys):
    with patch(
        "app.calculator_repl.input",
        side_effect=["exit"],
    ):
        repl()

    assert "Goodbye!" in capsys.readouterr().out


def test_repl_help(capsys):
    with patch(
        "app.calculator_repl.input",
        side_effect=["help", "exit"],
    ):
        repl()

    assert "Available Commands" in capsys.readouterr().out


def test_repl_calculation(capsys):
    with patch(
        "app.calculator_repl.input",
        side_effect=["add 10 5", "exit"],
    ):
        repl()

    assert "Result: 15" in capsys.readouterr().out


def test_repl_history(capsys):
    with patch(
        "app.calculator_repl.input",
        side_effect=["add 10 5", "history", "exit"],
    ):
        repl()

    assert "add" in capsys.readouterr().out


def test_repl_clear(capsys):
    with patch(
        "app.calculator_repl.input",
        side_effect=["clear", "exit"],
    ):
        repl()

    assert "History cleared." in capsys.readouterr().out


def test_repl_undo_redo(capsys):
    with patch(
        "app.calculator_repl.input",
        side_effect=[
            "add 10 5",
            "undo",
            "redo",
            "exit",
        ],
    ):
        repl()

    output = capsys.readouterr().out

    assert "Undo successful." in output
    assert "Redo successful." in output


def test_repl_undo_redo_empty(capsys):
    with patch(
        "app.calculator_repl.input",
        side_effect=["undo", "redo", "exit"],
    ):
        repl()

    output = capsys.readouterr().out

    assert "Nothing to undo." in output
    assert "Nothing to redo." in output


def test_repl_save_load(capsys):
    with patch(
        "app.calculator_repl.input",
        side_effect=["save", "load", "exit"],
    ):
        repl()

    output = capsys.readouterr().out

    assert "History saved." in output
    assert "History loaded." in output


def test_repl_invalid_input(capsys):
    with patch(
        "app.calculator_repl.input",
        side_effect=["invalid 10 5", "exit"],
    ):
        repl()

    assert "Error:" in capsys.readouterr().out


def test_repl_empty_input(capsys):
    with patch(
        "app.calculator_repl.input",
        side_effect=["", "exit"],
    ):
        repl()

    assert "Goodbye!" in capsys.readouterr().out


def test_repl_keyboard_interrupt(capsys):
    with patch(
        "app.calculator_repl.input",
        side_effect=KeyboardInterrupt,
    ):
        repl()

    assert "Goodbye!" in capsys.readouterr().out


def test_repl_eof(capsys):
    with patch(
        "app.calculator_repl.input",
        side_effect=EOFError,
    ):
        repl()

    assert "Goodbye!" in capsys.readouterr().out

def test_repl_main_entry_point():
    import runpy

    with patch(
        "builtins.input",
        side_effect=["exit"],
    ):
        runpy.run_module(
            "app.calculator_repl",
            run_name="__main__",
        )
