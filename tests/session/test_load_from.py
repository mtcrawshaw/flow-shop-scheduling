"""
Unit test cases for load_from() in flowshop/session.py.
"""

from flowshop.session import Session
from flowshop.utils import EXAMPLE_TASKS


def test_load_from_valid():
    """
    Test loading in a saved session when given a valid save name to load. Note that this
    will have to change in the case that scripts/save_example.py changes, as this
    essentially a hard-coded check for the result of the current implementation of that
    script.
    """

    # Load session.
    session = Session("example", load=True)

    # Compare session values.
    planned_tasks, actual_tasks = EXAMPLE_TASKS
    assert session.history_pos == 12
    assert len(session.edit_history) == 13
    assert session.edit_history[0][0].tasks == []
    assert session.edit_history[0][1].tasks == []
    for i in range(len(planned_tasks)):
        assert session.edit_history[i + 1][0].tasks == planned_tasks[: i + 1]
        assert session.edit_history[i + 1][1].tasks == []
    for i in range(len(actual_tasks)):
        n = len(planned_tasks)
        assert session.edit_history[n + i + 1][0].tasks == planned_tasks
        assert session.edit_history[n + i + 1][1].tasks == actual_tasks[: i + 1]


def test_load_from_invalid():
    """
    Test loading in a saved session wehn given an invalid name to load. We just check
    that an error gets raised.
    """

    # Try to load session.
    error = False
    try:
        session = Session("bad_example", load=True)
    except:
        error = True

    # Ensure an error was raised.
    assert error
