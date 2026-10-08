"""Arithmetic operations using the Strategy design pattern."""

from abc import ABC, abstractmethod
import math

from app.exceptions import OperationError


class Operation(ABC):
    """Abstract strategy for calculator operations."""

    @abstractmethod
    def execute(self, a: float, b: float) -> float:
        """Perform an arithmetic operation."""


class Addition(Operation):
    def execute(self, a, b):
        return a + b


class Subtraction(Operation):
    def execute(self, a, b):
        return a - b


class Multiplication(Operation):
    def execute(self, a, b):
        return a * b


class Division(Operation):
    def execute(self, a, b):
        if b == 0:
            raise OperationError("Cannot divide by zero.")
        return a / b


class Power(Operation):
    def execute(self, a, b):
        try:
            result = a ** b
        except (OverflowError, ZeroDivisionError, ValueError) as exc:
            raise OperationError("Invalid power operation.") from exc

        if isinstance(result, complex) or not math.isfinite(result):
            raise OperationError("Power result must be a finite real number.")

        return result


class Root(Operation):
    def execute(self, a, b):
        """Calculate the b-th root of a."""
        if b == 0:
            raise OperationError("Root degree cannot be zero.")

        if a == 0 and b < 0:
            raise OperationError("Cannot take a negative root of zero.")

        if a < 0:
            if not float(b).is_integer() or int(b) % 2 == 0:
                raise OperationError(
                    "Negative numbers require an odd integer root."
                )
            return -((-a) ** (1 / b))

        try:
            result = a ** (1 / b)
        except (OverflowError, ZeroDivisionError, ValueError) as exc:
            raise OperationError("Invalid root operation.") from exc

        if not math.isfinite(result):
            raise OperationError("Root result must be finite.")

        return result


class OperationFactory:
    """Factory pattern for creating arithmetic strategies."""

    _operations = {
        "add": Addition,
        "subtract": Subtraction,
        "multiply": Multiplication,
        "divide": Division,
        "power": Power,
        "root": Root,
    }

    @classmethod
    def create(cls, name: str) -> Operation:
        operation_class = cls._operations.get(name.lower())

        if operation_class is None:
            raise OperationError(f"Unknown operation: {name}")

        return operation_class()