"""
Unit test cases for flowshop/task.py.
"""

from datetime import datetime

from flowshop import Schedule, Task


def test_tasks_in_interval_small():
    """
    Test Schedule.tasks_in_interval() for a small example.
    """

    task1 = Task(
        "task1",
        priority=1.5,
        start_time=datetime(2020, 5, 1, hour=12),
        end_time=datetime(2020, 5, 1, hour=13, minute=30),
    )
    task2 = Task(
        "task2",
        priority=2.0,
        start_time=datetime(2020, 5, 1, hour=13, minute=30),
        end_time=datetime(2020, 5, 1, hour=14, minute=30),
    )
    task3 = Task(
        "task3",
        priority=2.0,
        start_time=datetime(2020, 5, 8, hour=13, minute=30),
        end_time=datetime(2020, 5, 8, hour=14, minute=30),
    )
    schedule = Schedule("test", [task1, task2, task3])

    start_time = datetime(2020, 5, 1)
    end_time = datetime(2020, 5, 8)
    assert schedule.tasks_in_interval(start_time, end_time) == [task1, task2]


def test_tasks_in_interval_empty():
    """
    Test Schedule.tasks_in_interval() for an empty example.
    """

    task1 = Task(
        "task1",
        priority=1.5,
        start_time=datetime(2020, 5, 1, hour=12),
        end_time=datetime(2020, 5, 1, hour=13, minute=30),
    )
    task2 = Task(
        "task2",
        priority=2.0,
        start_time=datetime(2020, 5, 1, hour=13, minute=30),
        end_time=datetime(2020, 5, 1, hour=14, minute=30),
    )
    task3 = Task(
        "task3",
        priority=2.0,
        start_time=datetime(2020, 5, 8, hour=13, minute=30),
        end_time=datetime(2020, 5, 8, hour=14, minute=30),
    )
    schedule = Schedule("test", [task1, task2, task3])

    start_time = datetime(2020, 4, 1)
    end_time = datetime(2020, 4, 8)
    assert schedule.tasks_in_interval(start_time, end_time) == []


def test_tasks_in_interval_start_overlap():
    """
    Test Schedule.tasks_in_interval() when a target task is overlapping the interval
    start time.
    """

    task1 = Task(
        "task1",
        priority=1.5,
        start_time=datetime(2020, 5, 1, hour=12),
        end_time=datetime(2020, 5, 1, hour=13, minute=30),
    )
    task2 = Task(
        "task2",
        priority=2.0,
        start_time=datetime(2020, 5, 1, hour=13, minute=30),
        end_time=datetime(2020, 5, 1, hour=14, minute=30),
    )
    schedule = Schedule("test", [task1, task2])

    start_time = datetime(2020, 5, 1, hour=13)
    end_time = datetime(2020, 5, 1, hour=13, minute=30)
    assert schedule.tasks_in_interval(start_time, end_time) == [task1]


def test_tasks_in_interval_end_overlap():
    """
    Test Schedule.tasks_in_interval() when a target task is overlapping the interval end
    time.
    """

    task1 = Task(
        "task1",
        priority=1.5,
        start_time=datetime(2020, 5, 1, hour=12),
        end_time=datetime(2020, 5, 1, hour=13, minute=30),
    )
    task2 = Task(
        "task2",
        priority=2.0,
        start_time=datetime(2020, 5, 1, hour=13, minute=30),
        end_time=datetime(2020, 5, 1, hour=14, minute=30),
    )
    schedule = Schedule("test", [task1, task2])

    start_time = datetime(2020, 5, 1, hour=11)
    end_time = datetime(2020, 5, 1, hour=12, minute=30)
    assert schedule.tasks_in_interval(start_time, end_time) == [task1]


def test_tasks_in_interval_surround():
    """
    Test Schedule.tasks_in_interval() when a target task is surrounding the interval.
    """

    task1 = Task(
        "task1",
        priority=1.5,
        start_time=datetime(2020, 5, 1, hour=12),
        end_time=datetime(2020, 5, 1, hour=13, minute=30),
    )
    task2 = Task(
        "task2",
        priority=2.0,
        start_time=datetime(2020, 5, 1, hour=13, minute=30),
        end_time=datetime(2020, 5, 1, hour=14, minute=30),
    )
    schedule = Schedule("test", [task1, task2])

    start_time = datetime(2020, 5, 1, hour=12)
    end_time = datetime(2020, 5, 1, hour=14)
    assert schedule.tasks_in_interval(start_time, end_time) == [task1, task2]
