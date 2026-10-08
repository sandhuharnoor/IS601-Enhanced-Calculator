"""Input validation for calculator commands."""

import math

from app.exceptions import InvalidInputError


def validate_number(value):
    try:
        number = float(value)
    except (ValueError, TypeError) as exc:
        raise InvalidInputError(
            "Please enter a valid number."
        ) from exc

    if not math.isfinite(number):
        raise InvalidInputError(
            "Numbers must be finite."
        )

    return number


def validate_operation(command):
    valid = {
        "add", "subtract", "multiply",
        "divide", "power", "root",
    }

    if command.lower() not in valid:
        raise InvalidInputError(
            f"Invalid operation: {command}"
        )

    return command.lower()


def validate_arguments(parts):
    if len(parts) != 3:
        raise InvalidInputError(
            "Usage: <operation> <number1> <number2>"
        )

    operation = validate_operation(parts[0])
    a = validate_number(parts[1])
    b = validate_number(parts[2])

    return operation, a, b