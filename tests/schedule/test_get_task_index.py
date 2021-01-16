"""
Unit test cases for flowshop/task.py.
"""

from datetime import datetime, date

from flowshop import Schedule, Task


def test_get_task_index_valid():
    """
    Test getting task index with valid queries.
    """

    # Construct schedule.
    tasks = [
        Task(
            "task1",
            priority=1.0,
            start_time=datetime(2020, 5, 1, hour=12),
            end_time=datetime(2020, 5, 1, hour=13, minute=30),
        ),
        Task(
            "task2",
            priority=1.0,
            start_time=datetime(2020, 5, 1, hour=13, minute=30),
            end_time=datetime(2020, 5, 1, hour=14, minute=30),
        ),
        Task(
            "task3",
            priority=2.0,
            start_time=datetime(2020, 5, 2, hour=12),
            end_time=datetime(2020, 5, 2, hour=13, minute=30),
        ),
        Task(
            "task4",
            priority=2.0,
            start_time=datetime(2020, 5, 2, hour=23),
            end_time=datetime(2020, 5, 2, hour=23, minute=30),
        ),
        Task(
            "task5",
            priority=1.0,
            start_time=datetime(2020, 5, 3, hour=1, minute=30),
            end_time=datetime(2020, 5, 3, hour=1, minute=59),
        ),
        Task(
            "task6",
            priority=1.0,
            start_time=datetime(2020, 6, 3, hour=1, minute=30),
            end_time=datetime(2020, 6, 3, hour=1, minute=59),
        ),
    ]
    schedule = Schedule("test", tasks)

    # Get task indices for each task.
    task_indices = [
        schedule.get_task_index(date(2020, 5, 1), 0),
        schedule.get_task_index(date(2020, 5, 1), 1),
        schedule.get_task_index(date(2020, 5, 2), 0),
        schedule.get_task_index(date(2020, 5, 2), 1),
        schedule.get_task_index(date(2020, 5, 3), 0),
        schedule.get_task_index(date(2020, 6, 3), 0),
    ]

    # Test task indices.
    assert task_indices == list(range(len(tasks)))


def test_get_task_index_invalid():
    """
    Test getting task index with invalid queries.
    """

    # Construct schedule.
    tasks = [
        Task(
            "task1",
            priority=1.0,
            start_time=datetime(2020, 5, 1, hour=12),
            end_time=datetime(2020, 5, 1, hour=13, minute=30),
        ),
        Task(
            "task2",
            priority=1.0,
            start_time=datetime(2020, 5, 1, hour=13, minute=30),
            end_time=datetime(2020, 5, 1, hour=14, minute=30),
        ),
        Task(
            "task3",
            priority=2.0,
            start_time=datetime(2020, 5, 2, hour=12),
            end_time=datetime(2020, 5, 2, hour=13, minute=30),
        ),
        Task(
            "task4",
            priority=2.0,
            start_time=datetime(2020, 5, 2, hour=23),
            end_time=datetime(2020, 5, 2, hour=23, minute=30),
        ),
        Task(
            "task5",
            priority=1.0,
            start_time=datetime(2020, 5, 3, hour=1, minute=30),
            end_time=datetime(2020, 5, 3, hour=1, minute=59),
        ),
        Task(
            "task6",
            priority=1.0,
            start_time=datetime(2020, 6, 3, hour=1, minute=30),
            end_time=datetime(2020, 6, 3, hour=1, minute=59),
        ),
    ]
    schedule = Schedule("test", tasks)

    # Execute queries and check for errors.
    queries = [
        (date(2020, 5, 1), 2),
        (date(2020, 5, 2), 2),
        (date(2020, 5, 3), 1),
        (date(2020, 6, 3), 1),
        (date(2020, 5, 4), 0),
    ]
    for query in queries:
        failed = False
        try:
            task_index = schedule.get_task_index(query[0], query[1])
        except:
            failed = True

        assert failed
