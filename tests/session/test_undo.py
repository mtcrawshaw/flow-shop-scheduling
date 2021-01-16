"""
Unit test cases for undo() in flowshop/session.py.
"""

from datetime import datetime, timedelta, time

from flowshop import Session, Task


def test_undo_empty_planned():
    """
    Test undoing the addition of a task to an empty session.
    """

    # Construct session.
    session = Session("test")

    # Insert task and undo insertion.
    session.insert_task(
        day=4,
        planned=True,
        name="test",
        priority=1.0,
        start_time=time(hour=12),
        hours=1.5,
    )
    session.undo()

    # Test session values.
    assert session.history_pos == 0
    assert len(session.edit_history) == 2
    assert len(session.edit_history[0][0].tasks) == 0
    assert len(session.edit_history[0][1].tasks) == 0
    assert len(session.edit_history[1][0].tasks) == 1
    assert len(session.edit_history[1][1].tasks) == 0
    task = session.edit_history[1][0].tasks[0]
    assert task.name == "test"
    assert task.priority == 1.0
    assert task.start_time.date() == session.base_date + timedelta(days=4)
    assert task.start_time.time() == time(hour=12)
    assert task.end_time.date() == session.base_date + timedelta(days=4)
    assert task.end_time.time() == time(hour=13, minute=30)


def test_undo_empty_actual():
    """
    Test undoing the addition of a task to an empty session.
    """

    # Construct session.
    session = Session("test")

    # Insert task and undo insertion.
    session.insert_task(
        day=4,
        planned=False,
        name="test",
        priority=1.0,
        start_time=time(hour=12),
        hours=1.5,
    )
    session.undo()

    # Test session values.
    assert session.history_pos == 0
    assert len(session.edit_history) == 2
    assert len(session.edit_history[0][0].tasks) == 0
    assert len(session.edit_history[0][1].tasks) == 0
    assert len(session.edit_history[1][0].tasks) == 0
    assert len(session.edit_history[1][1].tasks) == 1
    task = session.edit_history[1][1].tasks[0]
    assert task.name == "test"
    assert task.priority == 1.0
    assert task.start_time.date() == session.base_date + timedelta(days=4)
    assert task.start_time.time() == time(hour=12)
    assert task.end_time.date() == session.base_date + timedelta(days=4)
    assert task.end_time.time() == time(hour=13, minute=30)


def test_undo_edge():
    """
    Test undoing when there is nothing to undo.
    """

    # Construct session.
    session = Session("test")

    # Undo.
    session.undo()

    # Test session values.
    assert session.history_pos == 0
    assert len(session.edit_history) == 1
    assert len(session.edit_history[0][0].tasks) == 0
    assert len(session.edit_history[0][1].tasks) == 0


def test_undo_filled_planned():
    """
    Test undoing an edit task action on a filled out planned schedule.
    """

    # Set up case. Note that we have to manually set the base date of the session in
    # order to access the task, since it has a hard-coded date.
    session = Session("example", load=True)
    session.base_date = session.current_schedules()[0].tasks[0].start_time.date()
    session.base_date -= timedelta(days=session.base_date.weekday())
    planned = True
    day = 4
    task_index = 0
    new_values = {"name": "new_name"}

    # Store pre-edit values.
    old_history_pos = session.history_pos
    old_planned, old_actual = session.current_schedules()

    # Edit task, then undo.
    session.edit_task(
        planned=planned, day=day, task_index=task_index, new_values=new_values,
    )
    session.undo()

    # Test session values.
    new_planned, new_actual = session.current_schedules()
    assert session.history_pos == old_history_pos
    assert old_planned == new_planned
    assert old_actual == new_actual


def test_undo_filled_actual():
    """
    Test undoing an edit task action on a filled out actual schedule.
    """

    # Set up case. Note that we have to manually set the base date of the session in
    # order to access the task, since it has a hard-coded date.
    session = Session("example", load=True)
    session.base_date = session.current_schedules()[0].tasks[0].start_time.date()
    session.base_date -= timedelta(days=session.base_date.weekday())
    planned = False
    day = 4
    task_index = 0
    new_values = {"name": "new_name"}

    # Store pre-edit values.
    old_history_pos = session.history_pos
    old_planned, old_actual = session.current_schedules()

    # Edit task, then undo.
    session.edit_task(
        planned=planned, day=day, task_index=task_index, new_values=new_values,
    )
    session.undo()

    # Test session values.
    new_planned, new_actual = session.current_schedules()
    assert session.history_pos == old_history_pos
    assert old_planned == new_planned
    assert old_actual == new_actual
