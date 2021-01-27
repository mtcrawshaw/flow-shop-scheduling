""" Interface definition for running a Session from the terminal. """

from flowshop.session import Session
from flowshop.utils import Direction


class TerminalSession:
    """ Interface definition for running a Session from the terminal. """

    def __init__(self, name: str, load=False) -> None:
        """ Init function for TerminalSession. """
        self.session = Session(name, load=load)

    def run(self) -> None:
        """ Runs the session. Only needs to be called once at the beginning. """
        pass

    def display(self) -> None:
        """ Displays the session. Called any time a user action is taken. """
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
