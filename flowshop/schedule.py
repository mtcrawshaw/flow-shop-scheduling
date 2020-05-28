""" Schedule object which holds a set of tasks. """

from typing import List

from flowshop.task import Task


class Schedule:
    """ Schedule object which holds a set of tasks. """

    def __init__(self, name: str, tasks: List[Task] = None):
        """ Init function for schedule object. """

        # Store given schedule data.
        self.name = name
        if tasks is not None:
            self._tasks = list(tasks)
            self.sort_tasks()
            self.check_for_overlap()

    def add_task(self, task: Task):
        """
        Adds a task to self._tasks. Checks to ensure that task isn't overlapping an
        existing task.
        """

        self._tasks += [task]

        # This is a redundant sorting, since self._tasks gets sorted in
        # self.check_for_overlap().
        self.sort_tasks()
        self.check_for_overlap()

    def check_for_overlap(self):
        """
        Checks whether self._tasks contains any overlapping tasks. Raises an error if so.
        Note that the sort here can be redundant, but we do so to make it easier to check
        for overlapping tasks.
        """
 
        self.sort_tasks()
        for i in range(len(self._tasks) - 1):
            current_task = self._tasks[i]
            next_task = self._tasks[i + 1]
 
            if current_task.end_time > next_task.start_time:
                raise ValueError(
                    "Schedule contains overlapping tasks %s and %s."
                    % (current_task, next_task)
                )

    def sort_tasks(self):
        """
        Sorts tasks by start time.
        """
        self._tasks = sorted(self._tasks, key=lambda task: task.start_time)
