"""
Unit test cases for insert_task() in flowshop/session.py.
"""

from datetime import datetime, time, timedelta

from flowshop.session import Session
from flowshop.task import Task
from flowshop.utils import list_exclude


def test_insert_task_empty_actual():
    """
    Insert a task into the actual schedule of an empty session.
    """

    # Construct session.
    session = Session("test")

    # Insert task.
    session.insert_task(
        day=0,
        planned=False,
        name="test",
        priority=1.0,
        start_time=time(hour=12),
        hours=1.5,
    )

    # Test session values.
    assert session.history_pos == 1
    assert len(session.edit_history) == 2
    assert len(session.edit_history[0][0].tasks) == 0
    assert len(session.edit_history[0][1].tasks) == 0
    assert len(session.edit_history[1][0].tasks) == 0
    assert len(session.edit_history[1][1].tasks) == 1
    task = session.edit_history[1][1].tasks[0]
    assert task.name == "test"
    assert task.priority == 1.0
    assert task.start_time == datetime.combine(session.base_date, time(hour=12))
    assert task.end_time == datetime.combine(
        session.base_date, time(hour=13, minute=30)
    )


def test_insert_task_empty_planned():
    """
    Insert a task into the planned schedule of an empty session.
    """

    # Construct session.
    session = Session("test")

    # Insert task.
    session.insert_task(
        day=0,
        planned=True,
        name="test",
        priority=1.0,
        start_time=time(hour=12),
        hours=1.5,
    )

    # Test session values.
    assert session.history_pos == 1
    assert len(session.edit_history) == 2
    assert len(session.edit_history[0][0].tasks) == 0
    assert len(session.edit_history[0][1].tasks) == 0
    assert len(session.edit_history[1][0].tasks) == 1
    assert len(session.edit_history[1][1].tasks) == 0
    task = session.edit_history[1][0].tasks[0]
    assert task.name == "test"
    assert task.priority == 1.0
    assert task.start_time == datetime.combine(session.base_date, time(hour=12))
    assert task.end_time == datetime.combine(
        session.base_date, time(hour=13, minute=30)
    )


def test_insert_task_nonempty_actual():
    """
    Insert a task into the actual schedule of a nonempty session.
    """

    # Construct session.
    session = Session("example", load=True)

    # Store pre-insert session values.
    pre_history_pos = session.history_pos
    pre_edit_history = list(session.edit_history)

    # Insert task.
    session.insert_task(
        day=4,
        planned=False,
        name="test",
        priority=1.0,
        start_time=time(hour=15),
        hours=1,
    )

    # Test session values.
    assert session.history_pos == pre_history_pos + 1
    assert len(session.edit_history) == len(pre_edit_history) + 1
    assert session.edit_history[:-1] == pre_edit_history
    assert session.edit_history[-1][0] == pre_edit_history[-1][0]
    assert (
        list_exclude(session.edit_history[-1][1].tasks, 2)
        == pre_edit_history[-1][1].tasks
    )
    task = session.edit_history[-1][1].tasks[2]
    assert task.name == "test"
    assert task.priority == 1.0
    assert task.start_time == datetime.combine(
        session.base_date, time(hour=15)
    ) + timedelta(days=4)
    assert task.end_time == datetime.combine(
        session.base_date, time(hour=16)
    ) + timedelta(days=4)


def test_insert_task_nonempty_planned():
    """
    Insert a task into the planned schedule of a nonempty session.
    """

    # Construct session.
    session = Session("example", load=True)

    # Store pre-insert session values.
    pre_history_pos = session.history_pos
    pre_edit_history = list(session.edit_history)

    # Insert task.
    task = Task(
        "test",
        priority=1.0,
        start_time=datetime(2020, 5, 1, hour=15),
        end_time=datetime(2020, 5, 1, hour=16),
    )
    session.insert_task(
        day=4,
        planned=True,
        name="test",
        priority=1.0,
        start_time=time(hour=15),
        hours=1,
    )

    # Test session values.
    assert session.history_pos == pre_history_pos + 1
    assert len(session.edit_history) == len(pre_edit_history) + 1
    assert session.edit_history[:-1] == pre_edit_history
    assert session.edit_history[-1][1] == pre_edit_history[-1][1]
    assert (
        list_exclude(session.edit_history[-1][0].tasks, 2)
        == pre_edit_history[-1][0].tasks
    )
    task = session.edit_history[-1][0].tasks[2]
    assert task.name == "test"
    assert task.priority == 1.0
    assert task.start_time == datetime.combine(
        session.base_date, time(hour=15)
    ) + timedelta(days=4)
    assert task.end_time == datetime.combine(
        session.base_date, time(hour=16)
    ) + timedelta(days=4)


def test_insert_task_sorted():
    """
    Insert a task into the actual schedule of a nonempty session, and check that the new
    task gets sorted correctly.
    """

    # Construct session.
    session = Session("example", load=True)

    # Store pre-insert session values.
    pre_history_pos = session.history_pos
    pre_edit_history = list(session.edit_history)

    # Insert task.
    session.insert_task(
        day=5,
        planned=False,
        name="test",
        priority=1.0,
        start_time=time(hour=12, minute=30),
        hours=0.5,
    )

    # Test session values.
    assert session.history_pos == pre_history_pos + 1
    assert len(session.edit_history) == len(pre_edit_history) + 1
    assert session.edit_history[:-1] == pre_edit_history
    assert session.edit_history[-1][0] == pre_edit_history[-1][0]
    assert (
        list_exclude(session.edit_history[-1][1].tasks, 3)
        == pre_edit_history[-1][1].tasks
    )
    task = session.edit_history[-1][1].tasks[3]
    assert task.name == "test"
    assert task.priority == 1.0
    assert task.start_time == datetime.combine(
        session.base_date, time(hour=12, minute=30)
    ) + timedelta(days=5)
    assert task.end_time == datetime.combine(
        session.base_date, time(hour=13)
    ) + timedelta(days=5)


def test_insert_task_overlap():
    """
    Insert an invalid (overlapping) task into the planned schedule of a nonempty
    session, and check that an error gets raised.
    """

    # Construct session.
    session = Session("example", load=True)

    # Store pre-insert session values.
    pre_history_pos = session.history_pos
    pre_edit_history = list(session.edit_history)

    # Insert task.
    error = False
    try:
        session.insert_task(
            day=5,
            planned=True,
            name="test",
            priority=1.0,
            start_time=time(hour=13),
            hours=1,
        )
    except ValueError:
        error = True

    # Ensure error was thrown.
    assert error
