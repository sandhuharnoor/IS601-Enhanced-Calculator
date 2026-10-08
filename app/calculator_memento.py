"""Memento pattern for undo and redo functionality."""

from copy import deepcopy


class CalculatorMemento:
    def __init__(self, state):
        self._state = deepcopy(state)

    def get_state(self):
        return deepcopy(self._state)


class MementoManager:
    def __init__(self):
        self._undo_stack = []
        self._redo_stack = []

    def save(self, state):
        self._undo_stack.append(CalculatorMemento(state))
        self._redo_stack.clear()

    def undo(self, current_state):
        if not self._undo_stack:
            return None

        self._redo_stack.append(CalculatorMemento(current_state))
        return self._undo_stack.pop().get_state()

    def redo(self, current_state):
        if not self._redo_stack:
            return None

        self._undo_stack.append(CalculatorMemento(current_state))
        return self._redo_stack.pop().get_state()

    def clear(self):
        self._undo_stack.clear()
        self._redo_stack.clear()