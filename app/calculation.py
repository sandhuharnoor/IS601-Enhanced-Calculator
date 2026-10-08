"""Calculation model and Strategy pattern integration."""

from dataclasses import dataclass
from datetime import datetime

from app.operations import OperationFactory


@dataclass
class Calculation:
    operation: str
    a: float
    b: float
    result: float
    timestamp: str

    @classmethod
    def create(cls, operation, a, b):
        strategy = OperationFactory.create(operation)
        result = strategy.execute(a, b)
        return cls(
            operation=operation,
            a=float(a),
            b=float(b),
            result=float(result),
            timestamp=datetime.now().isoformat(),
        )

    def to_dict(self):
        return {
            "operation": self.operation,
            "a": self.a,
            "b": self.b,
            "result": self.result,
            "timestamp": self.timestamp,
        }