from app.exceptions import OperationError
"""Unit tests for the Calculation model."""

from datetime import datetime

import pytest

from app.calculation import Calculation


@pytest.mark.parametrize(
    "operation,a,b,expected",
    [
        ("add", 10, 5, 15),
        ("subtract", 10, 5, 5),
        ("multiply", 10, 5, 50),
        ("divide", 10, 5, 2),
        ("power", 2, 3, 8),
        ("root", 16, 2, 4),
    ],
)
def test_create_calculation(operation, a, b, expected):
    calculation = Calculation.create(operation, a, b)

    assert calculation.operation == operation
    assert calculation.a == float(a)
    assert calculation.b == float(b)
    assert calculation.result == pytest.approx(expected)
    assert datetime.fromisoformat(calculation.timestamp)


def test_calculation_to_dict():
    calculation = Calculation.create("add", 10, 5)

    data = calculation.to_dict()

    assert data == {
        "operation": "add",
        "a": 10.0,
        "b": 5.0,
        "result": 15.0,
        "timestamp": calculation.timestamp,
    }



def test_calculation_invalid_operation():
    with pytest.raises(OperationError):
        Calculation.create("invalid", 10, 5)


def test_calculation_division_by_zero():
    with pytest.raises(OperationError):
        Calculation.create("divide", 10, 0)

