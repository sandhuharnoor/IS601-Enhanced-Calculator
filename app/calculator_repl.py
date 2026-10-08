"""Enhanced calculator REPL with advanced design patterns."""

from app.calculation import Calculation
from app.calculator_config import CalculatorConfig
from app.calculator_memento import MementoManager
from app.exceptions import CalculatorError
from app.history import HistoryManager
from app.input_validators import validate_arguments


class HistoryObserver:
    """Observer that automatically saves calculation history."""

    def __init__(self, history, enabled=True):
        self.history = history
        self.enabled = enabled

    def update(self, event):
        if self.enabled:
            self.history.save()


class Calculator:
    """Facade providing a simplified calculator interface."""

    def __init__(self, config=None):
        self.config = config or CalculatorConfig.from_env()

        self.history = HistoryManager(
            self.config.history_file,
            self.config.max_history,
        )

        self.mementos = MementoManager()
        self.observers = [
            HistoryObserver(
                self.history,
                self.config.auto_save,
            )
        ]

        self.history.load()

    def notify(self, event):
        for observer in self.observers:
            observer.update(event)

    def calculate(self, operation, a, b):
        calculation = Calculation.create(
            operation, a, b
        )

        self.mementos.save(
            self.history.get_records()
        )

        self.history.add(calculation)
        self.notify("calculation")

        return calculation.result

    def clear(self):
        self.mementos.save(
            self.history.get_records()
        )

        self.history.clear()
        self.notify("clear")

    def undo(self):
        previous = self.mementos.undo(
            self.history.get_records()
        )

        if previous is None:
            return False

        self.history.restore(previous)
        self.notify("undo")
        return True

    def redo(self):
        next_state = self.mementos.redo(
            self.history.get_records()
        )

        if next_state is None:
            return False

        self.history.restore(next_state)
        self.notify("redo")
        return True

    def save(self):
        self.history.save()

    def load(self):
        self.mementos.save(
            self.history.get_records()
        )
        return self.history.load()

    def help(self):
        return """
Available Commands:
  add <a> <b>       Addition
  subtract <a> <b>  Subtraction
  multiply <a> <b>  Multiplication
  divide <a> <b>    Division
  power <a> <b>     Exponentiation
  root <a> <b>      Calculate the b-th root of a

  history           Display calculation history
  clear             Clear calculation history
  undo              Undo last history change
  redo              Redo last undone change
  save              Save history to CSV
  load              Load history from CSV
  help              Display available commands
  exit              Exit the calculator
"""


def repl():
    calculator = Calculator()

    print("Enhanced Professional Calculator")
    print("Type 'help' for available commands.")

    while True:
        try:
            user_input = input("\n>>> ").strip()

            if not user_input:
                continue

            parts = user_input.split()
            command = parts[0].lower()

            if command == "exit":
                print("Goodbye!")
                break

            if command == "help":
                print(calculator.help())
                continue

            if command == "history":
                print(calculator.history.display())
                continue

            if command == "clear":
                calculator.clear()
                print("History cleared.")
                continue

            if command == "undo":
                print(
                    "Undo successful."
                    if calculator.undo()
                    else "Nothing to undo."
                )
                continue

            if command == "redo":
                print(
                    "Redo successful."
                    if calculator.redo()
                    else "Nothing to redo."
                )
                continue

            if command == "save":
                calculator.save()
                print("History saved.")
                continue

            if command == "load":
                loaded = calculator.load()
                print(
                    "History loaded."
                    if loaded
                    else "No history file found."
                )
                continue

            operation, a, b = validate_arguments(parts)
            result = calculator.calculate(operation, a, b)

            print(f"Result: {result}")

        except CalculatorError as exc:
            print(f"Error: {exc}")

        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    repl()