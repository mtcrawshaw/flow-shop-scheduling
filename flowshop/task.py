""" Task object definition. Represents a single task in a schedule. """

import datetime


class Task:
    """ Represents a single task in a schedule. """

    def __init__(
        self,
        name: str,
        completed: float = 0.0,
        priority: float = None,
        start_time: datetime.datetime = None,
        end_time: datetime.datetime = None,
    ):
        """ Init function for Task object. """

        self.name = name
        self.completed = completed
        self.priority = priority
        self.start_time = start_time
        self.end_time = end_time

    def __repr__(self):
        """ Returns string representation of task. """

        start_str = self.start_time.strftime("%d/%m/%y %H:%M")
        end_str = self.end_time.strftime("%d/%m/%y %H:%M")
        rep = "(%s, %f, %f, %s, %s)" % (self.name, completed, priority, start_str, end_str)
        return rep

    def get_total_points(self):
        """ Computes maximum possible points for completing task. """
        hours = (self.end_time - self.start_time).total_seconds() / 3600
        return self.priority * hours

    def get_points(self):
        """ Computes points earned so far based on task completion. """
        return self.get_total_points() * self.completed
