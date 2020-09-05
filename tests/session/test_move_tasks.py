"""
Unit test cases for move_tasks() in flowshop/session.py.
"""

from datetime import datetime, timedelta
from copy import deepcopy

from flowshop.session import Session
from flowshop.task import Task


def test_move_tasks_single_planned():
    """
    Test moving a single task from a planned schedule with only a single task.
    """

    # Construct session. Note that we have to manually set the base date of the session
    # in order to access the task, since it has a hard-coded date.
    session = Session("test")
    task = Task(
        "test",
        priority=1.0,
        start_time=datetime(2020, 5, 1, hour=12),
        end_time=datetime(2020, 5, 1, hour=13, minute=30),
    )
    session.insert_task(
        planned=True, task=task,
    )
    session.base_date = session.current_schedules()[0].tasks[0].start_time.date()
    session.base_date -= timedelta(days=session.base_date.weekday())

    # Move the task.
    session.move_tasks(
        planned=True,
        day=4,
        start_task_index=0,
        end_task_index=1,
        time_delta=timedelta(hours=2),
    )

    # Test session values.
    edited_task = deepcopy(task)
    edited_task.start_time = datetime(2020, 5, 1, hour=14)
    edited_task.end_time = datetime(2020, 5, 1, hour=15, minute=30)
    assert session.history_pos == 2
    assert len(session.edit_history) == 3
    assert len(session.edit_history[0][0].tasks) == 0
    assert len(session.edit_history[0][1].tasks) == 0
    assert len(session.edit_history[1][0].tasks) == 1
    assert len(session.edit_history[1][1].tasks) == 0
    assert len(session.edit_history[2][0].tasks) == 1
    assert len(session.edit_history[2][1].tasks) == 0
    assert session.edit_history[2][0].tasks[0] == edited_task


def test_move_tasks_single_actual():
    """
    Test moving a single task from an actual schedule with only a single task.
    """

    # Construct session. Note that we have to manually set the base date of the session
    # in order to access the task, since it has a hard-coded date.
    session = Session("test")
    task = Task(
        "test",
        priority=1.0,
        start_time=datetime(2020, 5, 1, hour=12),
        end_time=datetime(2020, 5, 1, hour=13, minute=30),
    )
    session.insert_task(
        planned=False, task=task,
    )
    session.base_date = session.current_schedules()[1].tasks[0].start_time.date()
    session.base_date -= timedelta(days=session.base_date.weekday())

    # Move the task.
    session.move_tasks(
        planned=False,
        day=4,
        start_task_index=0,
        end_task_index=1,
        time_delta=timedelta(hours=2),
    )

    # Test session values.
    edited_task = deepcopy(task)
    edited_task.start_time = datetime(2020, 5, 1, hour=14)
    edited_task.end_time = datetime(2020, 5, 1, hour=15, minute=30)
    assert session.history_pos == 2
    assert len(session.edit_history) == 3
    assert len(session.edit_history[0][0].tasks) == 0
    assert len(session.edit_history[0][1].tasks) == 0
    assert len(session.edit_history[1][0].tasks) == 0
    assert len(session.edit_history[1][1].tasks) == 1
    assert len(session.edit_history[2][0].tasks) == 0
    assert len(session.edit_history[2][1].tasks) == 1
    assert session.edit_history[2][1].tasks[0] == edited_task


def test_move_tasks_full():
    """
    Test moving multiple tasks in a full schedule.
    """

    # Construct session. Note that we have to manually set the base date of the session in
    # order to access the task, since it has a hard-coded date.
    session = Session("example", load=True)
    session.base_date = session.current_schedules()[0].tasks[0].start_time.date()
    session.base_date -= timedelta(days=session.base_date.weekday())
    planned = True
    day = 4
    start_task_index = 0
    end_task_index = 2

    # Store pre-move session values.
    pre_history_pos = session.history_pos
    pre_edit_history = list(session.edit_history)
    original_tasks = [
        session.get_task(planned=planned, day=day, task_index=i)
        for i in range(start_task_index, end_task_index)
    ]

    # Move tasks.
    session.move_tasks(
        planned=planned,
        day=day,
        start_task_index=start_task_index,
        end_task_index=end_task_index,
        time_delta=timedelta(hours=2),
    )

    # Test session values.
    edited_tasks = [deepcopy(task) for task in original_tasks]
    edited_tasks[0].start_time = datetime(2020, 5, 1, hour=14)
    edited_tasks[0].end_time = datetime(2020, 5, 1, hour=15, minute=30)
    edited_tasks[1].start_time = datetime(2020, 5, 1, hour=15, minute=30)
    edited_tasks[1].end_time = datetime(2020, 5, 1, hour=16, minute=30)
    assert session.history_pos == pre_history_pos + 1
    assert len(session.edit_history) == len(pre_edit_history) + 1
    assert session.edit_history[:-1] == pre_edit_history
    assert pre_edit_history[-1][0].tasks[0:2] == original_tasks
    assert session.edit_history[-1][0].tasks[0:2] == edited_tasks
    assert session.edit_history[-1][0].tasks[2:] == pre_edit_history[-1][0].tasks[2:]
    assert session.edit_history[-1][1] == pre_edit_history[-1][1]


def test_move_tasks_invalid():
    """
    Test moving tasks in an invalid way.
    """

    # Construct session. Note that we have to manually set the base date of the session in
    # order to access the task, since it has a hard-coded date.
    session = Session("example", load=True)
    session.base_date = session.current_schedules()[0].tasks[0].start_time.date()
    session.base_date -= timedelta(days=session.base_date.weekday())
    planned = True
    day = 4
    start_task_index = 0
    end_task_index = 1

    # Move task into invalid time slot.
    error = False
    try:
        session.move_tasks(
            planned=planned,
            day=day,
            start_task_index=start_task_index,
            end_task_index=end_task_index,
            time_delta=timedelta(hours=2),
        )
    except:
        error = True

    # Ensure that error was thrown.
    assert error
