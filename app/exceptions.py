"""Custom exceptions for the enhanced calculator."""


class CalculatorError(Exception):
    """Base exception for calculator errors."""


class InvalidInputError(CalculatorError):
    """Raised when a user enters invalid input."""


class OperationError(CalculatorError):
    """Raised when a calculation cannot be completed."""


class ConfigurationError(CalculatorError):
    """Raised when application configuration is invalid."""


class HistoryError(CalculatorError):
    """Raised when calculation history cannot be saved or loaded."""