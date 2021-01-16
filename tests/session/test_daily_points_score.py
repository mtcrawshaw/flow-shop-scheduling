"""
Unit test cases for daily_points() and daily_score() in flowshop/session.py.
"""

from datetime import datetime, timedelta

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
        Task(
            "pt1",
            priority=1.0,
            start_time=(datetime(b.year, b.month, b.day, hour=12) + timedelta(days=1)),
            end_time=(
                datetime(b.year, b.month, b.day, hour=13, minute=30) + timedelta(days=1)
            ),
        ),
        Task(
            "pt2",
            priority=2.0,
            start_time=(
                datetime(b.year, b.month, b.day, hour=13, minute=30) + timedelta(days=1)
            ),
            end_time=(
                datetime(b.year, b.month, b.day, hour=15, minute=30) + timedelta(days=1)
            ),
        ),
        Task(
            "pt3",
            priority=1.0,
            start_time=(
                datetime(b.year, b.month, b.day, hour=13, minute=30) + timedelta(days=3)
            ),
            end_time=(
                datetime(b.year, b.month, b.day, hour=15, minute=30) + timedelta(days=3)
            ),
        ),
    ]
    actual_tasks = [
        Task(
            "at2",
            priority=2.0,
            start_time=(
                datetime(b.year, b.month, b.day, hour=14, minute=30) + timedelta(days=1)
            ),
            end_time=(
                datetime(b.year, b.month, b.day, hour=15, minute=30) + timedelta(days=1)
            ),
        ),
        Task(
            "at3",
            priority=1.0,
            start_time=(
                datetime(b.year, b.month, b.day, hour=19, minute=30) + timedelta(days=3)
            ),
            end_time=(
                datetime(b.year, b.month, b.day, hour=21, minute=30) + timedelta(days=3)
            ),
        ),
    ]
    for task in planned_tasks:
        session.insert_task(task=task, planned=True)
    for task in actual_tasks:
        session.insert_task(task=task, planned=False)

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
        Task(
            "pt1",
            priority=1.0,
            start_time=(datetime(b.year, b.month, b.day, hour=12) + timedelta(days=1)),
            end_time=(
                datetime(b.year, b.month, b.day, hour=13, minute=30) + timedelta(days=1)
            ),
        ),
        Task(
            "pt2",
            priority=2.0,
            start_time=(
                datetime(b.year, b.month, b.day, hour=13, minute=30) + timedelta(days=1)
            ),
            end_time=(
                datetime(b.year, b.month, b.day, hour=15, minute=30) + timedelta(days=1)
            ),
        ),
        Task(
            "pt3",
            priority=1.0,
            start_time=(
                datetime(b.year, b.month, b.day, hour=13, minute=30) + timedelta(days=3)
            ),
            end_time=(
                datetime(b.year, b.month, b.day, hour=15, minute=30) + timedelta(days=3)
            ),
        ),
        Task(
            "pt4",
            priority=1.0,
            start_time=(
                datetime(b.year, b.month, b.day, hour=13, minute=30)
                + timedelta(days=10)
            ),
            end_time=(
                datetime(b.year, b.month, b.day, hour=15, minute=30)
                + timedelta(days=10)
            ),
        ),
        Task(
            "pt5",
            priority=1.0,
            start_time=(
                datetime(b.year, b.month, b.day, hour=13, minute=30)
                + timedelta(days=-10)
            ),
            end_time=(
                datetime(b.year, b.month, b.day, hour=15, minute=30)
                + timedelta(days=-10)
            ),
        ),
    ]
    actual_tasks = [
        Task(
            "at2",
            priority=2.0,
            start_time=(
                datetime(b.year, b.month, b.day, hour=14, minute=30) + timedelta(days=1)
            ),
            end_time=(
                datetime(b.year, b.month, b.day, hour=15, minute=30) + timedelta(days=1)
            ),
        ),
        Task(
            "at3",
            priority=1.0,
            start_time=(
                datetime(b.year, b.month, b.day, hour=19, minute=30) + timedelta(days=3)
            ),
            end_time=(
                datetime(b.year, b.month, b.day, hour=21, minute=30) + timedelta(days=3)
            ),
        ),
        Task(
            "at4",
            priority=1.0,
            start_time=(
                datetime(b.year, b.month, b.day, hour=19, minute=30)
                + timedelta(days=10)
            ),
            end_time=(
                datetime(b.year, b.month, b.day, hour=21, minute=30)
                + timedelta(days=10)
            ),
        ),
        Task(
            "at5",
            priority=1.0,
            start_time=(
                datetime(b.year, b.month, b.day, hour=19, minute=30)
                + timedelta(days=-10)
            ),
            end_time=(
                datetime(b.year, b.month, b.day, hour=21, minute=30)
                + timedelta(days=-10)
            ),
        ),
    ]
    for task in planned_tasks:
        session.insert_task(task=task, planned=True)
    for task in actual_tasks:
        session.insert_task(task=task, planned=False)

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
