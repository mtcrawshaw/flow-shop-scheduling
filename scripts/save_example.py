""" Create and save an example session. """

from datetime import datetime

from flowshop.session import Session
from flowshop.task import Task
from flowshop.utils import EXAMPLE_TASKS


SAVE_NAME = "example"


if __name__ == "__main__":

    # Construct session with filled tasks.
    session = Session(SAVE_NAME)
    planned_tasks, actual_tasks = EXAMPLE_TASKS
    for task in planned_tasks:
        session.insert_task(planned=True, task=task)
    for task in actual_tasks:
        session.insert_task(planned=False, task=task)

    # Save session.
    session.save()
