""" Task object definition. Represents a single task in a schedule. """

from datetime import datetime, date


class Task:
    """ Represents a single task in a schedule. """

    def __init__(
        self,
        name: str,
        priority: float = None,
        start_time: datetime = None,
        end_time: datetime = None,
    ) -> None:
        """ Init function for Task object. """

        self.name = name
        self.priority = priority
        self.start_time = start_time
        self.end_time = end_time

        self.state_vars = ["name", "priority", "start_time", "end_time"]

    def __repr__(self) -> str:
        """ Returns string representation of task. """

        state_dict = {var_name: getattr(self, var_name) for var_name in self.state_vars}
        return str(state_dict)

    def __eq__(self, other) -> bool:
        """ Definition of self == other. """

        return all(
            getattr(self, var_name) == getattr(other, var_name)
            for var_name in self.state_vars
        )

    @property
    def date(self) -> date:
        """ Get date of task. Note that this is the date of the start time. """
        return self.start_time.date()

    def points(self) -> float:
        """ Computes points for completing task. """
        hours = (self.end_time - self.start_time).total_seconds() / 3600
        return self.priority * hours
