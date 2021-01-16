""" Create and save an example session. """

from datetime import datetime, timedelta
from copy import deepcopy

from flowshop.session import Session
from flowshop.task import Task
from flowshop.utils import EXAMPLE_TASKS


SAVE_NAME = "example"


if __name__ == "__main__":

    # Construct session with filled tasks.
    session = Session(SAVE_NAME)

    # Find proper base date.
    planned_tasks, actual_tasks = EXAMPLE_TASKS
    tasks = planned_tasks + actual_tasks
    earliest_start = min([task.start_time for task in tasks])
    session.base_date = earliest_start - timedelta(days=earliest_start.weekday())

    # Insert tasks.
    planned, actual = session.current_schedules()
    planned = deepcopy(planned)
    actual = deepcopy(actual)
    planned.tasks = EXAMPLE_TASKS[0]
    actual.tasks = EXAMPLE_TASKS[1]
    session.set_new_schedules(planned, actual)

    # Save session.
    session.save()
