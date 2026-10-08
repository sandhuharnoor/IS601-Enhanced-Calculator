# IS601 Enhanced Calculator

## Overview

This project is an enhanced Python command-line calculator
developed for IS601 Module 5 at NJIT.

The application demonstrates object-oriented programming,
advanced design patterns, persistent calculation history
using pandas, and automated testing.

## Features

- Addition, subtraction, multiplication, and division
- Power and root operations
- Interactive REPL interface
- Factory and Strategy design patterns
- Observer pattern for automatic history saving
- Memento pattern for undo and redo
- Facade pattern for simplified application interaction
- Pandas DataFrame history management
- CSV saving and loading
- Environment-based configuration
- Custom exception handling
- Automated testing with pytest
- GitHub Actions continuous integration

## Installation

Create a virtual environment:

    python -m venv .venv

Activate it and install dependencies:

    pip install -r requirements.txt

## Running the Calculator

    python -m app.calculator_repl

## Example Commands

    add 10 5
    subtract 10 5
    multiply 10 5
    divide 10 5
    power 2 3
    root 16 2
    history
    undo
    redo
    clear
    save
    load
    help
    exit

## Testing

Run the test suite:

    pytest --cov=app --cov-report=term-missing

Enforce 100% test coverage:

    pytest --cov=app --cov-report=term-missing --cov-fail-under=100

## Continuous Integration

GitHub Actions runs the automated tests whenever code
is pushed to the main branch or a pull request is opened.

The workflow fails if test coverage is below 100%.

## Technologies

- Python 3.12
- pandas
- python-dotenv
- pytest
- pytest-cov
- Git and GitHub
- GitHub Actions

## Author

Harnoor Sandhu
NJIT - IS601