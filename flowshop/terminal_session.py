""" Interface definition for running a Session from the terminal. """

from time import sleep
import curses
from curses import wrapper

from flowshop.session import Session
from flowshop.utils import Direction, DAYS_IN_WEEK


TASK_HEIGHT = 3
TASK_WIDTH = 50
TASKS_PER_DAY = 3
DAY_HEIGHT = TASK_HEIGHT * TASKS_PER_DAY
DAY_WIDTH = TASK_WIDTH * 2
TEXT_OFFSET = 2


class TerminalSession:
    """ Interface definition for running a Session from the terminal. """

    def __init__(self, name: str, load=False) -> None:
        """ Init function for TerminalSession. """
        self.session = Session(name, load=load)

    def run(self) -> None:
        """ Exposed wrapper around `self._run()` that uses curses wrapper. """

        wrapper(self._run)

    def _run(self, stdscr) -> None:
        """ Runs the session. Only needs to be called once at beginning of session. """

        # Clear screen.
        stdscr.clear()

        # Display the current session and wait for a key press.
        self._display(stdscr)

        # Wait for 5 seconds to see screen.
        sleep(5)

    def _display(self, stdscr) -> None:
        """ Displays the session. Called any time the screen must be refreshed. """

        planned, actual = self.session.current_schedules()
        nrows, ncols = stdscr.getmaxyx()

        # Create pads for each task indexed by day, version, and task index.
        for day in range(DAYS_IN_WEEK):
            day_versions = []
            day_y = day * DAY_HEIGHT

            for planned in [True, False]:
                version_tasks = []
                planned_x = 0 if planned else TASK_WIDTH

                for task in range(self.session.num_daily_tasks(planned, day)):

                    # Create single pad for task.
                    top = day_y + task * TASK_HEIGHT
                    left = planned_x
                    bottom = top + TASK_HEIGHT
                    right = left + TASK_WIDTH
                    msg = self.session.get_task(planned, day, task).name
                    draw_box(nrows, ncols, top, left, bottom, right, msg=msg)

                    # START HERE. Instead of drawing a single box for each task, we want
                    # to draw multiple boxes: one for name, one for priority, a couple
                    # for start/end time.
                    pass

    def navigate(self, direction: Direction, big=False) -> None:
        """
        Moves the cursor one unit in a direction specified by `direction`. If `big` is
        true, moves by day instead of by task.
        """
        pass

    def edit(self) -> None:
        """ Enters edit mode, allowing user to edit a task/block. """
        pass

    def insert(self, before=True) -> None:
        """ Inserts new time block, then enters insert mode, shifting nearby tasks. """
        pass

    def delete(self, fill=False) -> None:
        """
        Deletes a task and (if `fill` is True) move subsequent tasks backward to fill
        space.
        """
        pass

    def move(self) -> None:
        """
        Enters move mode, allowing user to move a contiguous set of tasks in time.
        """
        pass

    def quit(self) -> None:
        """ End session. """
        pass

    def load(self) -> None:
        """ Load a previously saved session. """
        pass

    def new(self) -> None:
        """ Start a new, blank session. """
        pass


def draw_box(
    nrows: int,
    ncols: int,
    top: int,
    left: int,
    bottom: int,
    right: int,
    msg: str = None,
) -> None:
    """
    Draws a box (pad with a border) around the given coordinates `top, left, bottom,
    right`. If `msg` is not None, writes `msg` in the drawn box. If any of the given
    coordinates are out of bounds, the box does not get drawn and we return normally.
    """

    # Check for out of bounds coordinates.
    if top < 0 or bottom >= nrows or left < 0 or right >= ncols:
        return

    # Get width and height.
    height = bottom - top
    width = right - left

    # Draw box and (potentially) add string.
    pad = curses.newpad(height, width)
    pad.box()
    if msg is not None:
        center_y = (bottom - top) // 2
        pad.addstr(center_y, TEXT_OFFSET, msg)
    pad.refresh(0, 0, top, left, bottom, right)
