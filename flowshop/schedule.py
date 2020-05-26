""" Schedule object which holds a set of tasks. """

from flowshop.task import Task


class Schedule:
    """ Schedule object which holds a set of tasks. """

    def __init__(self, name: str, tasks: List[Task] = None):
        """ Init function for schedule object. """

        # Store given schedule data.
        self.name = name
        if tasks is not None:
            tasks = sorted(tasks, key=lambda task: task.start_time)

            # Verify that there are no overlapping tasks.
            for i in range(len(tasks) - 1):
                current_task = tasks[i]
                next_task = tasks[i + 1]

                if current_task.end_time > next_task.start_time:
                    raise ValueError(
                        "Given list of Tasks contains overlapping tasks %s and %s."
                        % (current_task, next_task)
                    )

        self.tasks = list(tasks)

        # START HERE NEXT TIME
