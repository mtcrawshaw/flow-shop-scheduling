"""
Unit test cases for flowshop/task.py.
"""

from datetime import datetime

from flowshop.task import Task

def test_get_total_points():
    """
    Test Task.get_total_points() for a small example.
    """

    task = Task(
        "test",
        priority=0.5,
        completed=0.5,
        start_time=datetime(2020, 5, 1, hour=12),
        end_time=datetime(2020, 5, 1, hour=13, minute=30),
    )
    assert task.get_total_points() == 0.75


def test_get_points():
    """
    Test Task.get_points() for a small example.
    """

    task = Task(
        "test",
        priority=0.5,
        completed=0.5,
        start_time=datetime(2020, 5, 1, hour=12),
        end_time=datetime(2020, 5, 1, hour=13, minute=30),
    )
    assert task.get_points() == 0.375


