
"""Tests for custom calculator exceptions."""

import pytest

from app.exceptions import (
    CalculatorError,
    InvalidInputError,
    OperationError,
    ConfigurationError,
    HistoryError,
)


def test_calculator_error():
    with pytest.raises(CalculatorError, match="Calculator error"):
        raise CalculatorError("Calculator error")


def test_invalid_input_error():
    with pytest.raises(InvalidInputError, match="Invalid input"):
        raise InvalidInputError("Invalid input")


def test_operation_error():
    with pytest.raises(OperationError, match="Operation failed"):
        raise OperationError("Operation failed")


def test_configuration_error():
    with pytest.raises(ConfigurationError, match="Invalid configuration"):
        raise ConfigurationError("Invalid configuration")


def test_history_error():
    with pytest.raises(HistoryError, match="History failed"):
        raise HistoryError("History failed")


@pytest.mark.parametrize(
    "exception_class",
    [
        InvalidInputError,
        OperationError,
        ConfigurationError,
        HistoryError,
    ],
)
def test_exception_inheritance(exception_class):
    assert issubclass(exception_class, CalculatorError)
    assert issubclass(exception_class, Exception)


@pytest.mark.parametrize(
    "exception_class",
    [
        InvalidInputError,
        OperationError,
        ConfigurationError,
        HistoryError,
    ],
)
def test_custom_exceptions_caught_by_base_class(exception_class):
    with pytest.raises(CalculatorError):
        raise exception_class("Test error")


def test_exception_message():
    error = InvalidInputError("Please enter a valid number.")

    assert str(error) == "Please enter a valid number."


def test_exception_isinstance():
    error = OperationError("Cannot divide by zero.")

    assert isinstance(error, OperationError)
    assert isinstance(error, CalculatorError)
    assert isinstance(error, Exception)
