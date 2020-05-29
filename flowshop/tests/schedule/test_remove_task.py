"""
Unit test cases for flowshop/task.py.
"""

from datetime import datetime
from typing import List


from flowshop.schedule import Schedule
from flowshop.task import Task


def test_remove_task():
    """
    Test Schedule.remove_task() for a small case.
    """
    task1 = Task(
        "task1",
        priority=1.0,
        start_time=datetime(2020, 5, 1, hour=12),
        end_time=datetime(2020, 5, 1, hour=13, minute=30),
    )
    task2 = Task(
        "task2",
        priority=1.0,
        start_time=datetime(2020, 5, 1, hour=13, minute=30),
        end_time=datetime(2020, 5, 1, hour=14, minute=30),
    )
    schedule = Schedule("test", [task1, task2])

    removed_task = schedule.remove_task(1)

    assert removed_task == task2
    assert schedule.tasks == [task1]
