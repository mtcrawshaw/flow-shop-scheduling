""" Create and save an example session. """

from datetime import datetime

from flowshop.session import Session
from flowshop.task import Task


SAVE_NAME = "example"


if __name__ == "__main__":

    # Construct session with filled tasks.
    session = Session(SAVE_NAME)
    planned_tasks = [
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
    actual_tasks = [
        Task(
            "task1",
            priority=1.0,
            start_time=datetime(2020, 5, 1, hour=12),
            end_time=datetime(2020, 5, 1, hour=13, minute=30),
        ),
        Task(
            "task2",
            priority=1.0,
            start_time=datetime(2020, 5, 1, hour=14),
            end_time=datetime(2020, 5, 1, hour=15),
        ),
        Task(
            "task3",
            priority=2.0,
            start_time=datetime(2020, 5, 2, hour=11),
            end_time=datetime(2020, 5, 2, hour=12, minute=30),
        ),
        Task(
            "task4",
            priority=2.0,
            start_time=datetime(2020, 5, 2, hour=13),
            end_time=datetime(2020, 5, 2, hour=13, minute=30),
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
            start_time=datetime(2020, 6, 3, hour=2, minute=30),
            end_time=datetime(2020, 6, 3, hour=2, minute=59),
        ),
    ]
    for task in planned_tasks:
        session.insert_task(planned=True, task=task)
    for task in actual_tasks:
        session.insert_task(planned=False, task=task)

    # Save session.
    session.save()
