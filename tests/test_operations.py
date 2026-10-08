
"""Tests for arithmetic operations and design patterns."""

from unittest.mock import patch

import pytest

from app.exceptions import OperationError
from app.operations import (
    Operation,
    Addition,
    Subtraction,
    Multiplication,
    Division,
    Power,
    Root,
    OperationFactory,
)


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (10, 5, 15),
        (-10, 5, -5),
        (0, 0, 0),
        (2.5, 3.5, 6),
    ],
)
def test_addition(a, b, expected):
    assert Addition().execute(a, b) == pytest.approx(expected)


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (10, 5, 5),
        (5, 10, -5),
        (0, 0, 0),
    ],
)
def test_subtraction(a, b, expected):
    assert Subtraction().execute(a, b) == pytest.approx(expected)


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (10, 5, 50),
        (-4, 3, -12),
        (0, 100, 0),
    ],
)
def test_multiplication(a, b, expected):
    assert Multiplication().execute(a, b) == pytest.approx(expected)


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (10, 5, 2),
        (5, 2, 2.5),
        (-10, 2, -5),
    ],
)
def test_division(a, b, expected):
    assert Division().execute(a, b) == pytest.approx(expected)


def test_division_by_zero():
    with pytest.raises(OperationError, match="divide by zero"):
        Division().execute(10, 0)


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (2, 3, 8),
        (5, 0, 1),
        (4, -1, 0.25),
        (9, 0.5, 3),
    ],
)
def test_power(a, b, expected):
    assert Power().execute(a, b) == pytest.approx(expected)


def test_power_complex_result():
    with pytest.raises(OperationError, match="finite real"):
        Power().execute(-4, 0.5)


def test_power_infinite_result():
    with pytest.raises(OperationError, match="Invalid power"):
        Power().execute(1e200, 2)


def test_power_zero_negative_exponent():
    with pytest.raises(OperationError, match="Invalid power"):
        Power().execute(0, -1)


def test_power_overflow_exception():
    class OverflowNumber:
        def __pow__(self, exponent):
            raise OverflowError("Overflow")

    with pytest.raises(OperationError, match="Invalid power"):
        Power().execute(OverflowNumber(), 2)


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (16, 2, 4),
        (27, 3, 3),
        (81, 4, 3),
        (0, 2, 0),
        (16, -2, 0.25),
    ],
)
def test_root(a, b, expected):
    assert Root().execute(a, b) == pytest.approx(expected)


def test_root_zero_degree():
    with pytest.raises(OperationError, match="degree cannot be zero"):
        Root().execute(16, 0)


def test_root_negative_degree_of_zero():
    with pytest.raises(OperationError, match="negative root of zero"):
        Root().execute(0, -2)


@pytest.mark.parametrize(
    "a,b",
    [
        (-16, 2),
        (-16, 2.5),
    ],
)
def test_root_invalid_negative_number(a, b):
    with pytest.raises(OperationError, match="odd integer root"):
        Root().execute(a, b)


def test_root_negative_odd_integer():
    assert Root().execute(-27, 3) == pytest.approx(-3)


def test_root_negative_odd_degree():
    assert Root().execute(-8, -3) == pytest.approx(-0.5)


def test_root_infinite_result():
    with patch("app.operations.math.isfinite", return_value=False):
        with pytest.raises(OperationError, match="must be finite"):
            Root().execute(16, 2)


def test_root_overflow_exception():
    class OverflowNumber:
        def __eq__(self, other):
            return False

        def __lt__(self, other):
            return False

        def __pow__(self, exponent):
            raise OverflowError("Overflow")

    with pytest.raises(OperationError, match="Invalid root"):
        Root().execute(OverflowNumber(), 2)


@pytest.mark.parametrize(
    "name,expected_class",
    [
        ("add", Addition),
        ("subtract", Subtraction),
        ("multiply", Multiplication),
        ("divide", Division),
        ("power", Power),
        ("root", Root),
    ],
)
def test_operation_factory(name, expected_class):
    operation = OperationFactory.create(name)

    assert isinstance(operation, expected_class)
    assert isinstance(operation, Operation)


def test_operation_factory_case_insensitive():
    assert isinstance(OperationFactory.create("ADD"), Addition)
    assert isinstance(
        OperationFactory.create("MuLtIpLy"),
        Multiplication,
    )


def test_operation_factory_invalid():
    with pytest.raises(OperationError, match="Unknown operation"):
        OperationFactory.create("invalid")


def test_strategy_pattern():
    operation = OperationFactory.create("multiply")

    assert operation.execute(6, 7) == 42


def test_abstract_operation_cannot_instantiate():
    with pytest.raises(TypeError):
        Operation()


def test_root_value_error_exception():
    class InvalidNumber:
        def __eq__(self, other):
            return False

        def __lt__(self, other):
            return False

        def __pow__(self, exponent):
            raise ValueError("Invalid root")

    with pytest.raises(OperationError, match="Invalid root"):
        Root().execute(InvalidNumber(), 2)
