"""
Unit test cases for daily_points() and daily_score() in flowshop/session.py.
"""

from datetime import datetime, time, timedelta

from flowshop.schedule import Schedule
from flowshop.session import Session
from flowshop.task import Task


DAYS_IN_WEEK = 7


def test_daily_points_score_empty():
    """ Daily points for an empty schedule. """

    # Construct session.
    session = Session("test")

    # Construct expected point/score values.
    p_ind_pts = [0.0] * DAYS_IN_WEEK
    p_cum_pts = [0.0] * DAYS_IN_WEEK
    a_ind_pts = [0.0] * DAYS_IN_WEEK
    a_cum_pts = [0.0] * DAYS_IN_WEEK
    ind_score = [100.0] * DAYS_IN_WEEK
    cum_score = [100.0] * DAYS_IN_WEEK

    # Test point values.
    for day in range(DAYS_IN_WEEK):
        assert (
            session.daily_points(day, planned=False, cumulative=False) == p_ind_pts[day]
        )
        assert (
            session.daily_points(day, planned=False, cumulative=True) == p_cum_pts[day]
        )
        assert (
            session.daily_points(day, planned=True, cumulative=False) == a_ind_pts[day]
        )
        assert (
            session.daily_points(day, planned=True, cumulative=True) == a_cum_pts[day]
        )
        assert session.daily_score(day, cumulative=False) == ind_score[day]
        assert session.daily_score(day, cumulative=True) == cum_score[day]


def test_daily_points_score_current_week():
    """ Daily points for a schedule with tasks only in current week. """

    # Construct session.
    session = Session("test")
    b = session.base_date
    planned_tasks = [
        {
            "day": 1,
            "planned": True,
            "name": "pt1",
            "priority": 1.0,
            "start_time": time(hour=12),
            "hours": 1.5,
        },
        {
            "day": 1,
            "planned": True,
            "name": "pt1",
            "priority": 2.0,
            "start_time": time(hour=13, minute=30),
            "hours": 2.0,
        },
        {
            "day": 3,
            "planned": True,
            "name": "pt3",
            "priority": 1.0,
            "start_time": time(hour=13, minute=30),
            "hours": 2.0,
        },
    ]
    actual_tasks = [
        {
            "day": 1,
            "planned": False,
            "name": "at2",
            "priority": 2.0,
            "start_time": time(hour=14, minute=30),
            "hours": 1.0,
        },
        {
            "day": 3,
            "planned": False,
            "name": "at3",
            "priority": 1.0,
            "start_time": time(hour=19, minute=30),
            "hours": 2.0,
        },
    ]
    for task_kwargs in planned_tasks:
        session.insert_task(**task_kwargs)
    for task_kwargs in actual_tasks:
        session.insert_task(**task_kwargs)

    # Construct expected point/score values.
    p_ind_pts = [0.0, 5.5, 0.0, 2.0, 0.0, 0.0, 0.0]
    p_cum_pts = [0.0, 5.5, 5.5, 7.5, 7.5, 7.5, 7.5]
    a_ind_pts = [0.0, 2.0, 0.0, 2.0, 0.0, 0.0, 0.0]
    a_cum_pts = [0.0, 2.0, 2.0, 4.0, 4.0, 4.0, 4.0]
    ind_score = [100.0, 100.0 * 2.0 / 5.5] + [100.0] * 5
    cum_score = [100.0] + [100.0 * 2.0 / 5.5] * 2 + [100.0 * 4.0 / 7.5] * 4

    # Test point values.
    for day in range(DAYS_IN_WEEK):
        assert (
            session.daily_points(day, planned=True, cumulative=False) == p_ind_pts[day]
        )
        assert (
            session.daily_points(day, planned=True, cumulative=True) == p_cum_pts[day]
        )
        assert (
            session.daily_points(day, planned=False, cumulative=False) == a_ind_pts[day]
        )
        assert (
            session.daily_points(day, planned=False, cumulative=True) == a_cum_pts[day]
        )
        assert session.daily_score(day, cumulative=False) == ind_score[day]
        assert session.daily_score(day, cumulative=True) == cum_score[day]


def test_daily_points_score_full():
    """
    Daily points for a schedule with tasks both in and outside of current week.
    """

    # Construct session.
    session = Session("test")
    b = session.base_date
    planned_tasks = [
        {
            "day": 1,
            "planned": True,
            "name": "pt1",
            "priority": 1.0,
            "start_time": time(hour=12),
            "hours": 1.5,
        },
        {
            "day": 1,
            "planned": True,
            "name": "pt2",
            "priority": 2.0,
            "start_time": time(hour=13, minute=30),
            "hours": 2.0,
        },
        {
            "day": 3,
            "planned": True,
            "name": "pt3",
            "priority": 1.0,
            "start_time": time(hour=13, minute=30),
            "hours": 2.0,
        },
        {
            "day": 10,
            "planned": True,
            "name": "pt4",
            "priority": 1.0,
            "start_time": time(hour=13, minute=30),
            "hours": 2.0,
        },
        {
            "day": -10,
            "planned": True,
            "name": "pt5",
            "priority": 1.0,
            "start_time": time(hour=13, minute=30),
            "hours": 2.0,
        },
    ]
    actual_tasks = [
        {
            "day": 1,
            "planned": False,
            "name": "at2",
            "priority": 2.0,
            "start_time": time(hour=14, minute=30),
            "hours": 1.0,
        },
        {
            "day": 3,
            "planned": False,
            "name": "at3",
            "priority": 1.0,
            "start_time": time(hour=19, minute=30),
            "hours": 2.0,
        },
        {
            "day": 10,
            "planned": False,
            "name": "at4",
            "priority": 1.0,
            "start_time": time(hour=19, minute=30),
            "hours": 2.0,
        },
        {
            "day": -10,
            "planned": False,
            "name": "at5",
            "priority": 1.0,
            "start_time": time(hour=19, minute=30),
            "hours": 2.0,
        },
    ]
    for task_kwargs in planned_tasks:
        session.insert_task(**task_kwargs)
    for task_kwargs in actual_tasks:
        session.insert_task(**task_kwargs)

    # Construct expected point/score values.
    p_ind_pts = [0.0, 5.5, 0.0, 2.0, 0.0, 0.0, 0.0]
    p_cum_pts = [0.0, 5.5, 5.5, 7.5, 7.5, 7.5, 7.5]
    a_ind_pts = [0.0, 2.0, 0.0, 2.0, 0.0, 0.0, 0.0]
    a_cum_pts = [0.0, 2.0, 2.0, 4.0, 4.0, 4.0, 4.0]
    ind_score = [100.0, 100.0 * 2.0 / 5.5] + [100.0] * 5
    cum_score = [100.0] + [100.0 * 2.0 / 5.5] * 2 + [100.0 * 4.0 / 7.5] * 4

    # Test point values.
    for day in range(DAYS_IN_WEEK):
        assert (
            session.daily_points(day, planned=True, cumulative=False) == p_ind_pts[day]
        )
        assert (
            session.daily_points(day, planned=True, cumulative=True) == p_cum_pts[day]
        )
        assert (
            session.daily_points(day, planned=False, cumulative=False) == a_ind_pts[day]
        )
        assert (
            session.daily_points(day, planned=False, cumulative=True) == a_cum_pts[day]
        )
        assert session.daily_score(day, cumulative=False) == ind_score[day]
        assert session.daily_score(day, cumulative=True) == cum_score[day]
