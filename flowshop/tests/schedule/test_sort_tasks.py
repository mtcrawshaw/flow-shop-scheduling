"""
Unit test cases for flowshop/task.py.
"""

from datetime import datetime


from flowshop.schedule import Schedule
from flowshop.task import Task


def test_sort_tasks():
    """
    Test for correct task sorting.
    """

    tasks = [
        Task(
            "task_%d" % i,
            start_time=datetime(2020, 5, 1, hour=i),
            end_time=datetime(2020, 5, 1, hour=i + 1),
        )
        for i in range(10)
    ]
    schedule = Schedule("test", tasks)

    for i in range(len(schedule.tasks) - 1):
        assert schedule.tasks[i].start_time < schedule.tasks[i + 1].start_time
