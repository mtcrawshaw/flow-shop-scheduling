"""
Unit test cases for flowshop/task.py.
"""

from datetime import datetime
from typing import List


from flowshop.schedule import Schedule
from flowshop.task import Task


def test_add_task_empty():
    """
    Test add task which to empty schedule.
    """

    schedule = Schedule("test", [])
    task1 = Task(
        "task1",
        priority=1.0,
        start_time=datetime(2020, 5, 1, hour=12),
        end_time=datetime(2020, 5, 1, hour=13, minute=30),
    )
    schedule.add_task(task1)


def test_add_task_one():
    """
    Test add task which to schedule with one task.
    """

    task1 = Task(
        "task1",
        priority=1.0,
        start_time=datetime(2020, 5, 1, hour=12),
        end_time=datetime(2020, 5, 1, hour=13, minute=30),
    )
    schedule = Schedule("test", [task1])
    task2 = Task(
        "task2",
        priority=1.0,
        start_time=datetime(2020, 5, 1, hour=13, minute=30),
        end_time=datetime(2020, 5, 1, hour=14, minute=30),
    )


def test_add_task_incompatible():
    """
    Test adding an incompatible task.
    """

    task1 = Task(
        "task1",
        priority=1.0,
        start_time=datetime(2020, 5, 1, hour=12),
        end_time=datetime(2020, 5, 1, hour=13, minute=30),
    )
    schedule = Schedule("test", [task1])
    task2 = Task(
        "task2",
        priority=1.0,
        start_time=datetime(2020, 5, 1, hour=13),
        end_time=datetime(2020, 5, 1, hour=14),
    )

    # Check that add_task throws ValueError.
    try:
        schedule.add_task(task2)
        # If we made it here, no error was thrown.
        assert False
    except ValueError:
        # We're good in this case!
        pass
    except:
        # Something else went wrong.
        assert False
