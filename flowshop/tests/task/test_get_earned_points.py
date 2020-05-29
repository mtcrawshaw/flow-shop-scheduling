"""
Unit test cases for flowshop/task.py.
"""

from datetime import datetime

from flowshop.task import Task


def test_get_earned_points_small():
    """
    Test Task.get_earned_points() for a small example.
    """

    task = Task(
        "test",
        priority=0.5,
        completed=0.5,
        start_time=datetime(2020, 5, 1, hour=12),
        end_time=datetime(2020, 5, 1, hour=13, minute=30),
    )
    assert task.get_earned_points() == 0.375


def test_get_earned_points_empty():
    """
    Test Task.get_earned_points() for a task not yet started.
    """

    task = Task(
        "test",
        priority=0.5,
        completed=0.0,
        start_time=datetime(2020, 5, 1, hour=12),
        end_time=datetime(2020, 5, 1, hour=13, minute=30),
    )
    assert task.get_earned_points() == 0.0
