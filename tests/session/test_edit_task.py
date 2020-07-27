"""
Unit test cases for edit_task() in flowshop/session.py.
"""

from copy import deepcopy
from datetime import timedelta

from flowshop.session import Session


def test_edit_task_name():
    """
    Edit the name of a single task in an existing session.
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

    # Store pre-insert session values.
    pre_history_pos = session.history_pos
    pre_edit_history = list(session.edit_history)
    original_task = session.get_task(planned=planned, day=day, task_index=task_index)
    new_task = deepcopy(original_task)
    new_task.name = new_values["name"]

    # Edit task.
    session.edit_task(
        planned=planned, day=day, task_index=task_index, new_values=new_values,
    )

    # Test session values.
    assert session.history_pos == pre_history_pos + 1
    assert len(session.edit_history) == len(pre_edit_history) + 1
    assert session.edit_history[:-1] == pre_edit_history
    assert pre_edit_history[-1][0].tasks[0] == original_task
    assert session.edit_history[-1][0].tasks[0] == new_task
    assert session.edit_history[-1][1] == pre_edit_history[-1][1]


def test_edit_task_time_valid():
    """
    Edit the time of a single task in a valid way, i.e. it doesn't interfere with other
    tasks.
    """
    raise NotImplementedError


def test_edit_task_time_invalid():
    """
    Edit the time of a single task in an invalid way, i.e. it interferes with other
    tasks.
    """
    raise NotImplementedError


def test_edit_task_time_sorted():
    """
    Edit the time of a single task in a valid way, i.e. it doesn't interfere with other
    tasks, that changes the ordering of tasks.
    """
    raise NotImplementedError
