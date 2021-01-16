"""
Unit test cases for move_week() in flowshop/session.py.
"""

from datetime import date, timedelta
from copy import deepcopy

from flowshop import Session, Task


def test_move_week_forward():
    """
    Test moving the displayed week forward.
    """

    # Construct session. Note that we have to manually set the base date of the session in
    # order to access the task, since it has a hard-coded date.
    session = Session("example", load=True)
    session.base_date = session.current_schedules()[0].tasks[0].start_time.date()
    session.base_date -= timedelta(days=session.base_date.weekday())

    # Move the week forward.
    session.move_week()

    # Test week value.
    assert session.base_date == date(2020, 5, 4)


def test_move_week_backward():
    """
    Test moving the displayed week backward.
    """

    # Construct session. Note that we have to manually set the base date of the session in
    # order to access the task, since it has a hard-coded date.
    session = Session("example", load=True)
    session.base_date = session.current_schedules()[0].tasks[0].start_time.date()
    session.base_date -= timedelta(days=session.base_date.weekday())

    # Move the week forward.
    session.move_week(forward=False)

    # Test week value.
    assert session.base_date == date(2020, 4, 20)
