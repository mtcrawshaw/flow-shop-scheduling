"""
Unit test cases for redo() in flowshop/session.py.
"""

from datetime import datetime, timedelta

from flowshop.session import Session
from flowshop.task import Task


def test_redo_empty_planned():
    """
    Test redoing the addition of a task to an empty session.
    """

    # Construct session.
    session = Session("test")

    # Insert task.
    task = Task(
        "test",
        priority=1.0,
        start_time=datetime(2020, 5, 1, hour=12),
        end_time=datetime(2020, 5, 1, hour=13, minute=30),
    )
    session.insert_task(
        planned=True, task=task,
    )

    # Store session values.
    old_planned, old_actual = session.current_schedules()

    # Undo, then redo insertion.
    session.undo()
    session.redo()

    # Test session values.
    new_planned, new_actual = session.current_schedules()
    assert session.history_pos == 1
    assert len(session.edit_history) == 2
    assert new_planned == old_planned
    assert new_actual == old_actual
    assert len(session.edit_history[0][0].tasks) == 0
    assert len(session.edit_history[0][1].tasks) == 0
    assert len(session.edit_history[1][0].tasks) == 1
    assert len(session.edit_history[1][1].tasks) == 0
    assert session.edit_history[1][0].tasks[0] == task


def test_redo_empty_actual():
    """
    Test redoing the addition of a task to an empty session.
    """

    # Construct session.
    session = Session("test")

    # Insert task.
    task = Task(
        "test",
        priority=1.0,
        start_time=datetime(2020, 5, 1, hour=12),
        end_time=datetime(2020, 5, 1, hour=13, minute=30),
    )
    session.insert_task(
        planned=False, task=task,
    )

    # Store session values.
    old_planned, old_actual = session.current_schedules()

    # Undo, then redo insertion.
    session.undo()
    session.redo()

    # Test session values.
    new_planned, new_actual = session.current_schedules()
    assert session.history_pos == 1
    assert len(session.edit_history) == 2
    assert new_planned == old_planned
    assert new_actual == old_actual
    assert len(session.edit_history[0][0].tasks) == 0
    assert len(session.edit_history[0][1].tasks) == 0
    assert len(session.edit_history[1][0].tasks) == 0
    assert len(session.edit_history[1][1].tasks) == 1
    assert session.edit_history[1][1].tasks[0] == task


def test_redo_edge():
    """
    Test redoing when there is nothing to redo.
    """

    # Construct session.
    session = Session("test")

    # Undo.
    session.redo()

    # Test session values.
    assert session.history_pos == 0
    assert len(session.edit_history) == 1
    assert len(session.edit_history[0][0].tasks) == 0
    assert len(session.edit_history[0][1].tasks) == 0


def test_redo_filled():
    """
    Test redoing an action on a filled out planned schedule.
    """

    # Set up case. Note that we have to manually set the base date of the session in
    # order to access the task, since it has a hard-coded date.
    session = Session("example", load=True)
    session.base_date = session.current_schedules()[0].tasks[0].start_time.date()
    session.base_date -= timedelta(days=session.base_date.weekday())

    # Store pre-edit values.
    old_history_pos = session.history_pos
    old_history_len = len(session.edit_history)
    old_planned, old_actual = session.current_schedules()

    # Undo then redo last action.
    session.undo()
    session.redo()

    # Test session values.
    new_planned, new_actual = session.current_schedules()
    assert session.history_pos == old_history_pos
    assert old_planned == new_planned
    assert old_actual == new_actual
    assert len(session.edit_history) == old_history_len
