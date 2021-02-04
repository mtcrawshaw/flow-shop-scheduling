""" Interface definition for running a Session from the terminal. """

from time import sleep
import curses
from curses import wrapper

from flowshop.session import Session
from flowshop.utils import Direction


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
        self.display(stdscr)

        # Wait for 5 seconds to see screen.
        sleep(5)

    def display(self, stdscr) -> None:
        """ Displays the session. Called any time the screen must be refreshed. """

        # Draw some test pads.
        x = (curses.COLS - 1) // 6
        y = (curses.LINES - 1) // 6
        x1 = x
        y1 = y
        x2 = 2 * x
        y2 = 2 * y
        x3 = 4 * x
        y3 = 4 * y
        x4 = 5 * x
        y4 = 5 * y
        p1 = curses.newpad(y2 - y1, x2 - x1)
        p2 = curses.newpad(y4 - y3, x4 - x3)
        p1.box()
        p2.box()
        p1.refresh(0, 0, y1, x1, y2, x2)
        p2.refresh(0, 0, y3, x3, y4, x4)

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
