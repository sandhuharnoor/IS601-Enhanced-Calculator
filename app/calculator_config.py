"""Application configuration using environment variables."""

import os
from dataclasses import dataclass
from dotenv import load_dotenv

from app.exceptions import ConfigurationError


@dataclass
class CalculatorConfig:
    history_file: str = "history.csv"
    auto_save: bool = True
    max_history: int = 1000

    @classmethod
    def from_env(cls):
        load_dotenv()

        history_file = os.getenv("CALCULATOR_HISTORY_FILE", "history.csv")
        auto_save = os.getenv("CALCULATOR_AUTO_SAVE", "true").lower()

        if auto_save not in {"true", "false"}:
            raise ConfigurationError(
                "CALCULATOR_AUTO_SAVE must be true or false."
            )

        try:
            max_history = int(os.getenv("CALCULATOR_MAX_HISTORY", "1000"))
        except ValueError as exc:
            raise ConfigurationError(
                "CALCULATOR_MAX_HISTORY must be an integer."
            ) from exc

        if max_history <= 0:
            raise ConfigurationError(
                "CALCULATOR_MAX_HISTORY must be positive."
            )

        if not history_file.strip():
            raise ConfigurationError("History file cannot be empty.")

        return cls(
            history_file=history_file,
            auto_save=auto_save == "true",
            max_history=max_history,
        )