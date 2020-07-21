"""
Unit test cases for flowshop/task.py.
"""

from datetime import datetime


from flowshop.schedule import Schedule
from flowshop.task import Task


def test_check_for_overlap_positive():
    """
    Test for task overlap when overlap is present.
    """

    schedule = Schedule("test", [])
    task1 = Task(
        "task1",
        priority=1.0,
        start_time=datetime(2020, 5, 1, hour=12),
        end_time=datetime(2020, 5, 1, hour=13, minute=30),
    )
    task2 = Task(
        "task2",
        priority=1.0,
        start_time=datetime(2020, 5, 1, hour=13),
        end_time=datetime(2020, 5, 1, hour=14),
    )

    schedule.tasks = [task1, task2]

    try:
        schedule.check_for_overlap()
        # If we made it here, no error was thrown.
        assert False
    except ValueError:
        # We're good in this case!
        pass
    except:
        # Something else went wrong.
        assert False


def test_check_for_overlap_negative():
    """
    Test for task overlap when overlap is not present.
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

    schedule.check_for_overlap()
