"""
Unit test cases for flowshop/task.py.
"""

from datetime import datetime


from flowshop.schedule import Schedule
from flowshop.task import Task


def test_earned_points_small():
    """
    Test Schedule.earned_points() for a small example.
    """

    task1 = Task(
        "task1",
        priority=1.5,
        completed=0.5,
        start_time=datetime(2020, 5, 1, hour=12),
        end_time=datetime(2020, 5, 1, hour=13, minute=30),
    )
    task2 = Task(
        "task2",
        priority=2.0,
        completed=1.0,
        start_time=datetime(2020, 5, 1, hour=13, minute=30),
        end_time=datetime(2020, 5, 1, hour=14, minute=30),
    )
    schedule = Schedule("test", [task1, task2])

    assert schedule.earned_points() == 3.125


def test_earned_points_empty():
    """
    Test Schedule.earned_points() for an empty schedule.
    """

    schedule = Schedule("test", [])
    assert schedule.earned_points() == 0.0
