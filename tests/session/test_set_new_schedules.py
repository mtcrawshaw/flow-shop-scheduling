"""
Unit test cases for set_new_schedules() in flowshop/session.py.
"""

from datetime import datetime

from flowshop import Schedule, Session, Task


def test_set_new_schedules_1():
    """
    Call `set_new_schedules()` in the first case of edit history (cases listed in
    docstring of `set_new_schedules()`).
    """

    # Construct session.
    session = Session("test")

    # Construct planned and new schedules.
    planned_task = Task(
        "planned_task",
        priority=1.0,
        start_time=datetime(2020, 5, 1, hour=12),
        end_time=datetime(2020, 5, 1, hour=13, minute=30),
    )
    actual_task = Task(
        "actual_task",
        priority=1.0,
        start_time=datetime(2020, 5, 1, hour=13),
        end_time=datetime(2020, 5, 1, hour=14, minute=30),
    )
    planned = Schedule("planned", [planned_task])
    actual = Schedule("actual", [actual_task])

    # Set new schedules in session.
    session.set_new_schedules(planned, actual)

    # Test session values.
    assert session.history_pos == 1
    assert len(session.edit_history) == 2
    assert len(session.edit_history[0][0].tasks) == 0
    assert len(session.edit_history[0][1].tasks) == 0
    assert len(session.edit_history[1][0].tasks) == 1
    assert len(session.edit_history[1][1].tasks) == 1
    assert session.edit_history[1][0].tasks[0] == planned_task
    assert session.edit_history[1][1].tasks[0] == actual_task


def test_set_new_schedules_2():
    """
    Call `set_new_schedules()` in the second case of edit history (cases listed in
    docstring of `set_new_schedules()`).
    """

    # Construct session.
    session = Session("test")

    # Construct planned and new schedules.
    planned_tasks = [
        Task(
            "planned_task_1",
            priority=1.0,
            start_time=datetime(2020, 5, 1, hour=12),
            end_time=datetime(2020, 5, 1, hour=13, minute=30),
        ),
        Task(
            "planned_task_2",
            priority=1.0,
            start_time=datetime(2020, 5, 1, hour=12, minute=30),
            end_time=datetime(2020, 5, 1, hour=14),
        ),
    ]
    actual_tasks = [
        Task(
            "actual_task_1",
            priority=1.0,
            start_time=datetime(2020, 5, 1, hour=13),
            end_time=datetime(2020, 5, 1, hour=14, minute=30),
        ),
        Task(
            "actual_task_2",
            priority=1.0,
            start_time=datetime(2020, 5, 1, hour=13, minute=30),
            end_time=datetime(2020, 5, 1, hour=15),
        ),
    ]

    planned = [
        Schedule("planned_1", [planned_tasks[0]]),
        Schedule("planned_2", [planned_tasks[1]]),
    ]
    actual = [
        Schedule("actual_1", [actual_tasks[0]]),
        Schedule("actual_2", [actual_tasks[1]]),
    ]

    # Set new schedules in session, undo, then redo with new versions.
    session.set_new_schedules(planned[0], actual[0])
    session.undo()
    session.set_new_schedules(planned[1], actual[1])

    # Test session values.
    assert session.history_pos == 1
    assert len(session.edit_history) == 2
    assert len(session.edit_history[0][0].tasks) == 0
    assert len(session.edit_history[0][1].tasks) == 0
    assert len(session.edit_history[1][0].tasks) == 1
    assert len(session.edit_history[1][1].tasks) == 1
    assert session.edit_history[1][0].tasks[0] == planned_tasks[1]
    assert session.edit_history[1][1].tasks[0] == actual_tasks[1]


def test_set_new_schedules_3():
    """
    Call `set_new_schedules()` in the third case of edit history (cases listed in
    docstring of `set_new_schedules()`).
    """

    # Construct session.
    session = Session("test")

    # Construct planned and new schedules.
    planned_tasks = [
        Task(
            "planned_task",
            priority=1.0,
            start_time=datetime(2020, 5, 1, hour=12),
            end_time=datetime(2020, 5, 1, hour=13, minute=30),
        ),
        Task(
            "planned_task",
            priority=1.0,
            start_time=datetime(2020, 5, 1, hour=12),
            end_time=datetime(2020, 5, 1, hour=13, minute=30),
        ),
        Task(
            "planned_dummy",
            priority=1.0,
            start_time=datetime(2020, 5, 2, hour=12),
            end_time=datetime(2020, 5, 2, hour=13, minute=30),
        ),
    ]
    actual_tasks = [
        Task(
            "actual_task",
            priority=1.0,
            start_time=datetime(2020, 5, 1, hour=13),
            end_time=datetime(2020, 5, 1, hour=14, minute=30),
        ),
        Task(
            "actual_task",
            priority=1.0,
            start_time=datetime(2020, 5, 1, hour=13),
            end_time=datetime(2020, 5, 1, hour=14, minute=30),
        ),
        Task(
            "actual_dummy",
            priority=1.0,
            start_time=datetime(2020, 5, 2, hour=13),
            end_time=datetime(2020, 5, 1, hour=14, minute=30),
        ),
    ]

    planned = [
        Schedule("planned", [planned_tasks[0]]),
        Schedule("planned_dummy", [planned_tasks[0], planned_tasks[2]]),
        Schedule("planned", [planned_tasks[1]]),
    ]
    actual = [
        Schedule("actual", [actual_tasks[0]]),
        Schedule("actual_dummy", [actual_tasks[0], actual_tasks[2]]),
        Schedule("actual", [actual_tasks[1]]),
    ]

    # Set new schedules in session, undo, then redo with new versions.
    session.set_new_schedules(planned[0], actual[0])
    session.set_new_schedules(planned[1], actual[1])
    session.undo()
    session.undo()
    session.set_new_schedules(planned[2], actual[2])

    # Test session values.
    assert session.history_pos == 1
    assert len(session.edit_history) == 3
    assert len(session.edit_history[0][0].tasks) == 0
    assert len(session.edit_history[0][1].tasks) == 0
    assert len(session.edit_history[1][0].tasks) == 1
    assert len(session.edit_history[1][1].tasks) == 1
    assert len(session.edit_history[2][0].tasks) == 2
    assert len(session.edit_history[2][1].tasks) == 2
    assert session.edit_history[1][0].tasks == [planned_tasks[1]]
    assert session.edit_history[1][1].tasks == [actual_tasks[1]]
    assert session.edit_history[2][0].tasks == [planned_tasks[0], planned_tasks[2]]
    assert session.edit_history[2][1].tasks == [actual_tasks[0], actual_tasks[2]]
