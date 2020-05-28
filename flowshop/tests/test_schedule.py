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
        end_time=datetime(2020, 5, 1, hour=13, minute=30)
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
        end_time=datetime(2020, 5, 1, hour=13, minute=30)
    )
    schedule = Schedule("test", [task1])
    task2 = Task(
        "task2",
        priority=1.0,
        start_time=datetime(2020, 5, 1, hour=13, minute=30),
        end_time=datetime(2020, 5, 1, hour=14, minute=30)
    )


def test_add_task_incompatible():
    """
    Test adding an incompatible task.
    """

    task1 = Task(
        "task1",
        priority=1.0,
        start_time=datetime(2020, 5, 1, hour=12),
        end_time=datetime(2020, 5, 1, hour=13, minute=30)
    )
    schedule = Schedule("test", [task1])
    task2 = Task(
        "task2",
        priority=1.0,
        start_time=datetime(2020, 5, 1, hour=13),
        end_time=datetime(2020, 5, 1, hour=14)
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


def test_check_for_overlap_positive():
    """
    Test for task overlap when overlap is present.
    """

    schedule = Schedule("test", [])
    task1 = Task(
        "task1",
        priority=1.0,
        start_time=datetime(2020, 5, 1, hour=12),
        end_time=datetime(2020, 5, 1, hour=13, minute=30)
    )
    task2 = Task(
        "task2",
        priority=1.0,
        start_time=datetime(2020, 5, 1, hour=13),
        end_time=datetime(2020, 5, 1, hour=14)
    )

    # HARDCODE: Explicity set _tasks in order to test for overlap.
    schedule._tasks = [task1, task2]

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
        end_time=datetime(2020, 5, 1, hour=13, minute=30)
    )
    task2 = Task(
        "task2",
        priority=1.0,
        start_time=datetime(2020, 5, 1, hour=13, minute=30),
        end_time=datetime(2020, 5, 1, hour=14, minute=30)
    )
    schedule = Schedule("test", [task1, task2])

    schedule.check_for_overlap()


def test_sort_tasks():
    """
    Test for correct task sorting.
    """

    tasks = [Task(
        "task_%d" % i,
        start_time=datetime(2020, 5, 1, hour=i),
        end_time=datetime(2020, 5, 1, hour=i+1)
    ) for i in range(10)]
    schedule = Schedule("test", tasks)

    # HARDCODE to directly check schedule._tasks.
    for i in range(len(schedule._tasks) - 1):
        assert schedule._tasks[i].start_time < schedule._tasks[i + 1].start_time
