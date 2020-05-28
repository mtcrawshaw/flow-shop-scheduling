""" Task object definition. Represents a single task in a schedule. """

from datetime import datetime


class Task:
    """ Represents a single task in a schedule. """

    def __init__(
        self,
        name: str,
        completed: float = 0.0,
        priority: float = None,
        start_time: datetime = None,
        end_time: datetime = None,
    ) -> None:
        """ Init function for Task object. """

        self.name = name
        self.completed = completed
        self.priority = priority
        self.start_time = start_time
        self.end_time = end_time

    def __repr__(self) -> str:
        """ Returns string representation of task. """

        state = {
            "name": self.name,
            "completed": self.completed,
            "priority": self.priority,
            "start_time": self.start_time.strftime("%d/%m/%y %H:%M"),
            "end_time": self.end_time.strftime("%d/%m/%y %H:%M"),
        }
        return str(state)

    def get_total_points(self) -> float:
        """ Computes maximum possible points for completing task. """
        hours = (self.end_time - self.start_time).total_seconds() / 3600
        return self.priority * hours

    def get_points(self) -> float:
        """ Computes points earned so far based on task completion. """
        return self.get_total_points() * self.completed
