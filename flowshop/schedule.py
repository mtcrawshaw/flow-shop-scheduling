""" Schedule object which holds a set of tasks. """

from datetime import datetime, date
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
        else:
            self.tasks = []

        self.state_vars = ["name", "tasks"]

    def __eq__(self, other) -> bool:
        """ Definition of self == other. """

        return all(
            getattr(self, var_name) == getattr(other, var_name)
            for var_name in self.state_vars
        )

    def __str__(self) -> str:
        """ String representation of `self`. """

        return str({key: getattr(self, key) for key in self.state_vars})

    def add_task(self, task: Task) -> None:
        """
        Adds a task to self.tasks. Checks to ensure that task isn't overlapping an
        existing task.
        """

        self.tasks += [task]

        # This is a redundant sorting, since self.tasks gets sorted in
        # self.check_for_overlap(). We just do this to be safe, in case
        # self.check_for_overlap() changes later. We take the extra computation time for
        # a safety need.
        self._sort_tasks()
        self.check_for_overlap()

    def remove_task(self, task_index: int) -> Task:
        """
        Remove task by its index in self.tasks. Returns removed task.
        """

        return self.tasks.pop(task_index)

    def get_task_index(self, day: date, daily_index: int) -> int:
        """
        Get index of the ``daily_index``-th task on day ``day``.
        """

        # First, find some task whose date is equal to the day we're looking for.
        task_index = len(self.tasks) // 2
        low = 0
        high = len(self.tasks) - 1
        found = False
        while low <= high:
            if self.tasks[task_index].date == day:
                found = True
                break

            if self.tasks[task_index].date < day:
                low = task_index + 1
            elif self.tasks[task_index].date > day:
                high = task_index - 1
            task_index = int((low + high) / 2)

        # Make sure that such a task exists.
        if not found:
            raise ValueError("No task on day %s" % str(day))

        # Find the first task whose date is equal to ``day``.
        while task_index >= 0 and self.tasks[task_index].date == day:
            task_index -= 1
        task_index += 1

        # Make sure that the final task index has the correct date.
        task_index += daily_index
        if self.tasks[task_index].date != day:
            raise ValueError(
                "Index %d is larger than number of tasks on day %s" % (daily_index, day)
            )

        return task_index

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

    def points(self) -> float:
        """ Computes points earned for entire schedule. """

        return sum(task.points() for task in self.tasks)

    def interval_points(self, start_time: datetime, end_time: datetime) -> float:
        """ Computes points for all tasks within a given time interval. """

        tasks_in_interval = self.tasks_in_interval(start_time, end_time)
        return sum(task.points() for task in tasks_in_interval)

    def tasks_in_interval(self, start_time: datetime, end_time: datetime) -> List[Task]:
        """
        Returns a list of all tasks in the schedule that overlap the interval
        (start_time, end_time).
        """

        tasks_in_interval = []
        for task in self.tasks:
            overlapping_start = (
                task.start_time >= start_time and task.start_time < end_time
            )
            overlapping_end = task.end_time > start_time and task.end_time <= end_time
            surrounding = task.start_time <= start_time and task.end_time >= end_time
            if overlapping_start or overlapping_end or surrounding:
                tasks_in_interval.append(task)

        return tasks_in_interval

    def _sort_tasks(self):
        """
        Sorts tasks by start time.
        """

        self.tasks = sorted(self.tasks, key=lambda task: task.start_time)
