""" Schedule object which holds a set of tasks. """

from datetime import datetime
from typing import List

from flowshop.task import Task


class Schedule:
    """ Schedule object which holds a set of tasks. """

    def __init__(self, name: str, tasks: List[Task] = None) -> None:
        """ Init function for schedule object. """

        # Store given schedule data.
        self.name = name
        if tasks is not None:
            self.tasks = list(tasks)
            self._sort_tasks()
            self.check_for_overlap()

    def add_task(self, task: Task) -> None:
        """
        Adds a task to self.tasks. Checks to ensure that task isn't overlapping an
        existing task.
        """

        self.tasks += [task]

        # This is a redundant sorting, since self.tasks gets sorted in
        # self.check_for_overlap().
        self._sort_tasks()
        self.check_for_overlap()

    def remove_task(self, task_index: int) -> Task:
        """
        Remove task by its index in self.tasks. Returns removed task.
        """

        return self.tasks.pop(task_index)

    def check_for_overlap(self) -> None:
        """
        Checks whether self.tasks contains any overlapping tasks. Raises an error if so.
        Note that the sort here can be redundant, but we do so to make it easier to check
        for overlapping tasks.
        """

        self._sort_tasks()
        for i in range(len(self.tasks) - 1):
            current_task = self.tasks[i]
            next_task = self.tasks[i + 1]

            if current_task.end_time > next_task.start_time:
                raise ValueError(
                    "Schedule contains overlapping tasks %s and %s."
                    % (current_task, next_task)
                )

    def maximum_points(self) -> float:
        """ Computes maximum possible points for entire schedule. """

        return sum(task.maximum_points() for task in self.tasks)

    def earned_points(self) -> float:
        """ Computes points earned for entire schedule. """

        return sum(task.earned_points() for task in self.tasks)

    def maximum_interval_points(
        self, start_time: datetime, end_time: datetime
    ) -> float:
        """
        Computes maximum possible points for all tasks overlapping a given time
        interval.
        """

        tasks_in_interval = self.tasks_in_interval(start_time, end_time)
        return sum(task.maximum_points() for task in tasks_in_interval)

    def earned_interval_points(
        self, start_time: datetime, end_time: datetime
    ) -> float:
        """ Computes points earned for all tasks overlapping a given time interval.  """

        tasks_in_interval = self.tasks_in_interval(start_time, end_time)
        return sum(task.earned_points() for task in tasks_in_interval)

    def tasks_in_interval(
        self, start_time: datetime, end_time: datetime
    ) -> List[Task]:
        """
        Returns a list of all tasks in the schedule that overlap the interval
        (start_time, end_time).
        """

        tasks_in_interval = []
        for task in self.tasks:
            overlapping_start = (
                task.start_time > start_time and task.start_time < end_time
            )
            overlapping_end = task.end_time > start_time and task.end_time < end_time
            if overlapping_start or overlapping_end:
                tasks_in_interval.append(task)

        print("tasks in interval: %s" % tasks_in_interval)
        return tasks_in_interval

    def _sort_tasks(self):
        """
        Sorts tasks by start time.
        """

        self.tasks = sorted(self.tasks, key=lambda task: task.start_time)
