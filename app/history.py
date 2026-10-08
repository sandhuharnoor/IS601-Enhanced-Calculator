"""Persistent calculation history using pandas."""

from pathlib import Path
import pandas as pd

from app.exceptions import HistoryError


COLUMNS = ["operation", "a", "b", "result", "timestamp"]


class HistoryManager:
    def __init__(self, filename="history.csv", max_history=1000):
        self.filename = Path(filename)
        self.max_history = max_history
        self.data = pd.DataFrame(columns=COLUMNS)

    def add(self, calculation):
        row = pd.DataFrame([calculation.to_dict()])
        self.data = pd.concat(
            [self.data, row], ignore_index=True
        ).tail(self.max_history).reset_index(drop=True)

    def clear(self):
        self.data = pd.DataFrame(columns=COLUMNS)

    def save(self):
        try:
            self.filename.parent.mkdir(
                parents=True, exist_ok=True
            )
            self.data.to_csv(self.filename, index=False)
        except (OSError, PermissionError) as exc:
            raise HistoryError(
                f"Unable to save history: {exc}"
            ) from exc

    def load(self):
        if not self.filename.exists():
            return False

        try:
            data = pd.read_csv(self.filename)

            if not set(COLUMNS).issubset(data.columns):
                raise HistoryError(
                    "History file has invalid columns."
                )

            self.data = data[COLUMNS].tail(
                self.max_history
            ).reset_index(drop=True)

            return True
        except (OSError, ValueError, pd.errors.ParserError) as exc:
            raise HistoryError(
                f"Unable to load history: {exc}"
            ) from exc

    def get_records(self):
        return self.data.to_dict(orient="records")

    def restore(self, records):
        self.data = pd.DataFrame(records, columns=COLUMNS)

    def display(self):
        if self.data.empty:
            return "No calculations in history."

        return self.data.to_string(index=False)