"""
Unit test cases for flowshop/task.py.
"""

from datetime import datetime

from flowshop.task import Task


def test_points_small():
    """ Test Task.points() for a small example. """

    task = Task(
        "test",
        priority=0.5,
        start_time=datetime(2020, 5, 1, hour=12),
        end_time=datetime(2020, 5, 1, hour=13, minute=30),
    )
    assert task.points() == 0.75


def test_points_empty():
    """ Test Task.points() for an empty example. """

    task = Task(
        "test",
        priority=0.0,
        start_time=datetime(2020, 5, 1, hour=12),
        end_time=datetime(2020, 5, 1, hour=13, minute=30),
    )
    assert task.points() == 0.0
