"""
Unit test cases for delete_task() in flowshop/session.py.
"""

from datetime import datetime, timedelta, date, time

from flowshop import Session, Task
from flowshop.utils import list_exclude


def test_delete_task_single_planned():
    """
    Test deleting task from a schedule with only one task in planned.
    """

    # Construct session. Note that we have to manually set the base date of the session
    # in order to access the task, since it has a hard-coded date.
    session = Session("test")
    session.insert_task(
        day=4,
        planned=True,
        name="test",
        priority=1.0,
        start_time=time(hour=12),
        hours=1.5,
    )
    session.base_date = session.current_schedules()[0].tasks[0].start_time.date()
    session.base_date -= timedelta(days=session.base_date.weekday())

    # Delete the task.
    session.delete_task(planned=True, day=4, task_index=0)

    # Test session values.
    assert session.history_pos == 2
    assert len(session.edit_history) == 3
    assert len(session.edit_history[0][0].tasks) == 0
    assert len(session.edit_history[0][1].tasks) == 0
    assert len(session.edit_history[1][0].tasks) == 1
    assert len(session.edit_history[1][1].tasks) == 0
    assert len(session.edit_history[2][0].tasks) == 0
    assert len(session.edit_history[2][1].tasks) == 0


def test_delete_task_single_actual():
    """
    Test deleting task from a schedule with only one task in actual.
    """

    # Construct session. Note that we have to manually set the base date of the session
    # in order to access the task, since it has a hard-coded date.
    session = Session("test")
    session.insert_task(
        day=4,
        planned=False,
        name="test",
        priority=1.0,
        start_time=time(hour=12),
        hours=1.5,
    )
    session.base_date = session.current_schedules()[1].tasks[0].start_time.date()
    session.base_date -= timedelta(days=session.base_date.weekday())

    # Delete the task.
    session.delete_task(planned=False, day=4, task_index=0)

    # Test session values.
    assert session.history_pos == 2
    assert len(session.edit_history) == 3
    assert len(session.edit_history[0][0].tasks) == 0
    assert len(session.edit_history[0][1].tasks) == 0
    assert len(session.edit_history[1][0].tasks) == 0
    assert len(session.edit_history[1][1].tasks) == 1
    assert len(session.edit_history[2][0].tasks) == 0
    assert len(session.edit_history[2][1].tasks) == 0


def test_delete_task_full():
    """
    Test deleting task from a full schedule.
    """

    # Construct session. Note that we have to manually set the base date of the session in
    # order to access the task, since it has a hard-coded date.
    session = Session("example", load=True)
    session.base_date = session.current_schedules()[0].tasks[0].start_time.date()
    session.base_date -= timedelta(days=session.base_date.weekday())
    planned = True
    day = 5
    task_index = 0

    # Store pre-delete session values.
    pre_history_pos = session.history_pos
    pre_edit_history = list(session.edit_history)
    original_task = session.get_task(planned=planned, day=day, task_index=task_index)

    # Delete task.
    session.delete_task(planned=planned, day=day, task_index=task_index)

    # Test session values.
    assert session.history_pos == pre_history_pos + 1
    assert len(session.edit_history) == len(pre_edit_history) + 1
    assert session.edit_history[:-1] == pre_edit_history
    assert pre_edit_history[-1][0].tasks[2] == original_task
    assert session.edit_history[-1][0].tasks == list_exclude(
        pre_edit_history[-1][0].tasks, 2
    )
    assert session.edit_history[-1][1] == pre_edit_history[-1][1]


def test_delete_task_invalid():
    """
    Test deleting a nonexistent task from a full schedule.
    """

    # Construct session. Note that we have to manually set the base date of the session in
    # order to access the task, since it has a hard-coded date.
    session = Session("example", load=True)
    session.base_date = session.current_schedules()[0].tasks[0].start_time.date()
    session.base_date -= timedelta(days=session.base_date.weekday())
    planned = True
    day = 6
    task_index = 1

    # Delete nonexistent task.
    error = False
    try:
        session.delete_task(planned=planned, day=day, task_index=task_index)
    except:
        error = True

    # Ensure that error was thrown.
    assert error
