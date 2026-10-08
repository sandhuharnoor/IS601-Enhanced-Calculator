
"""Tests for calculator input validation."""

import pytest

from app.exceptions import InvalidInputError
from app.input_validators import (
    validate_number,
    validate_operation,
    validate_arguments,
)


@pytest.mark.parametrize(
    "value,expected",
    [
        ("10", 10.0),
        ("-5", -5.0),
        ("3.14", 3.14),
        (0, 0.0),
        (2.5, 2.5),
    ],
)
def test_validate_number_valid(value, expected):
    assert validate_number(value) == expected


@pytest.mark.parametrize(
    "value",
    ["abc", "", None, "10abc", [], {}],
)
def test_validate_number_invalid(value):
    with pytest.raises(InvalidInputError):
        validate_number(value)


@pytest.mark.parametrize(
    "value",
    ["nan", "inf", "-inf", float("inf"), float("nan")],
)
def test_validate_number_nonfinite(value):
    with pytest.raises(InvalidInputError, match="finite"):
        validate_number(value)


@pytest.mark.parametrize(
    "operation",
    ["add", "subtract", "multiply", "divide", "power", "root"],
)
def test_validate_operation_valid(operation):
    assert validate_operation(operation) == operation


def test_validate_operation_case_insensitive():
    assert validate_operation("ADD") == "add"
    assert validate_operation("MuLtIpLy") == "multiply"


def test_validate_operation_invalid():
    with pytest.raises(InvalidInputError):
        validate_operation("invalid")


def test_validate_arguments_valid():
    result = validate_arguments(["add", "10", "5"])

    assert result == ("add", 10.0, 5.0)


def test_validate_arguments_uppercase():
    result = validate_arguments(["DIVIDE", "20", "4"])

    assert result == ("divide", 20.0, 4.0)


@pytest.mark.parametrize(
    "parts",
    [
        [],
        ["add"],
        ["add", "10"],
        ["add", "10", "5", "extra"],
    ],
)
def test_validate_arguments_wrong_count(parts):
    with pytest.raises(InvalidInputError, match="Usage"):
        validate_arguments(parts)


def test_validate_arguments_invalid_operation():
    with pytest.raises(InvalidInputError):
        validate_arguments(["unknown", "10", "5"])


def test_validate_arguments_invalid_number():
    with pytest.raises(InvalidInputError):
        validate_arguments(["add", "abc", "5"])
