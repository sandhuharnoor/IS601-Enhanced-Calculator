
"""Tests for the Memento Design Pattern."""

from app.calculator_memento import CalculatorMemento, MementoManager


def test_memento_stores_state():
    original = [{"result": 10}]
    memento = CalculatorMemento(original)

    assert memento.get_state() == original


def test_memento_deep_copy():
    original = [{"result": 10}]
    memento = CalculatorMemento(original)

    original[0]["result"] = 99

    assert memento.get_state() == [{"result": 10}]

    restored = memento.get_state()
    restored[0]["result"] = 50

    assert memento.get_state() == [{"result": 10}]


def test_save_and_undo():
    manager = MementoManager()

    manager.save([])
    previous = manager.undo([{"result": 15}])

    assert previous == []


def test_undo_empty_stack():
    manager = MementoManager()

    assert manager.undo([]) is None


def test_redo():
    manager = MementoManager()

    manager.save([])
    manager.undo([{"result": 15}])

    restored = manager.redo([])

    assert restored == [{"result": 15}]


def test_redo_empty_stack():
    manager = MementoManager()

    assert manager.redo([]) is None


def test_save_clears_redo_stack():
    manager = MementoManager()

    manager.save([])
    manager.undo([{"result": 10}])
    manager.save([{"result": 20}])

    assert manager.redo([]) is None


def test_clear_stacks():
    manager = MementoManager()

    manager.save([])
    manager.undo([{"result": 10}])
    manager.clear()

    assert manager.undo([]) is None
    assert manager.redo([]) is None


def test_multiple_undo_redo():
    manager = MementoManager()

    manager.save([])
    manager.save([{"result": 10}])

    state = manager.undo([{"result": 20}])
    assert state == [{"result": 10}]

    state = manager.undo(state)
    assert state == []

    state = manager.redo(state)
    assert state == [{"result": 10}]

    state = manager.redo(state)
    assert state == [{"result": 20}]
