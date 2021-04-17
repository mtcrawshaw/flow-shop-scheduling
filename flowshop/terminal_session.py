""" Interface definition for running a Session from the terminal. """

from time import sleep
import curses
from curses import wrapper

from flowshop.session import Session
from flowshop.utils import Direction, DAYS_IN_WEEK


# Constants that determine the size of on-screen boxes.
TASK_HEIGHT = 3
NAME_WIDTH = 25
PRIORITY_WIDTH = 7
TIME_WIDTH = 11
TASK_WIDTH = NAME_WIDTH + PRIORITY_WIDTH + 2 * TIME_WIDTH
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

        # Store number of rows and number of columns.
        self.nrows, self.ncols = stdscr.getmaxyx()

        # Clear screen.
        stdscr.clear()

        # Display the current session and wait for a key press.
        self._display()

        # Wait.
        sleep(10)

    def _display(self) -> None:
        """ Displays the session. Called any time the screen must be refreshed. """

        # Draw boxes for each task.
        for day in range(DAYS_IN_WEEK):
            for planned in [True, False]:
                for task_idx in range(self.session.num_daily_tasks(planned, day)):
                    self._draw_task(planned, day, task_idx)

    def _draw_task(self, planned: bool, day: int, task_idx: int) -> None:
        """ Draw the specified task. """

        # Get task and coordinates of box.
        task = self.session.get_task(planned, day, task_idx)
        planned_x = 0 if planned else TASK_WIDTH
        day_y = day * DAY_HEIGHT
        top = day_y + task_idx * TASK_HEIGHT
        bottom = top + TASK_HEIGHT

        # Draw box for task name.
        name_left = planned_x
        name_right = name_left + NAME_WIDTH
        self._draw_box(top, name_left, bottom, name_right, msg=task.name)

        # Draw box for task priority.
        priority_left = name_right
        priority_right = priority_left + PRIORITY_WIDTH
        self._draw_box(
            top, priority_left, bottom, priority_right, msg=str(task.priority)
        )

        # Draw boxes for start/end time.
        start_left = priority_right
        start_right = start_left + TIME_WIDTH
        end_left = start_right
        end_right = end_left + TIME_WIDTH
        start_time = task.start_time.strftime("%I:%M%p")
        end_time = task.end_time.strftime("%I:%M%p")
        self._draw_box(top, start_left, bottom, start_right, msg=start_time)
        self._draw_box(top, end_left, bottom, end_right, msg=end_time)

    def _draw_box(
        self, top: int, left: int, bottom: int, right: int, msg: str = None,
    ) -> None:
        """
        Draws a box (pad with a border) around the given coordinates `top, left, bottom,
        right`. If `msg` is not None, writes `msg` in the drawn box. If any of the given
        coordinates are out of bounds, the box does not get drawn and we return normally.
        """

        # Check for out of bounds coordinates.
        if top < 0 or bottom >= self.nrows or left < 0 or right >= self.ncols:
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
