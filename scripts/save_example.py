""" Create and save an example session. """

from datetime import datetime, date, timedelta
from copy import deepcopy

from flowshop.session import Session
from flowshop.task import Task
from flowshop.utils import EXAMPLE_TASKS


SAVE_NAME = "example"


def task_base_date(task: Task) -> date:
    """ Get the date of the Monday preceding a given task. """

    task_date = task.start_time.date()
    return task_date - timedelta(days=task_date.weekday())


if __name__ == "__main__":

    # Construct session with filled tasks.
    session = Session(SAVE_NAME)

    # Insert tasks.
    planned_tasks, actual_tasks = EXAMPLE_TASKS
    for task in planned_tasks:
        session.base_date = task_base_date(task)
        session.insert_task(
            day=task.start_time.weekday(),
            planned=True,
            name=task.name,
            priority=task.priority,
            start_time=task.start_time.time(),
            hours=((task.end_time - task.start_time).total_seconds() / 3600),
        )
    for task in actual_tasks:
        session.base_date = task_base_date(task)
        session.insert_task(
            day=task.start_time.weekday(),
            planned=False,
            name=task.name,
            priority=task.priority,
            start_time=task.start_time.time(),
            hours=((task.end_time - task.start_time).total_seconds() / 3600),
        )

    # Find proper base date.
    tasks = planned_tasks + actual_tasks
    earliest_start = min([task.start_time for task in tasks])
    session.base_date = earliest_start - timedelta(days=earliest_start.weekday())

    # Save session.
    session.save()
