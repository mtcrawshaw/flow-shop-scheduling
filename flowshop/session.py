""" Session object for editing schedules. """

from typing import List, Typing

from flowshop.schedule import Schedule
from flowshop.files import saved_session_exists, save_session, load_session_state_dict


class Session:
    """ Session object for editing schedules. """

    def __init__(self, name: str, load=False) -> None:
        """ Init function for Session object. """

        self.name: str = name

        # self.edit_history represents the history of schedules through changes, so that
        # we can implement undo and redo. self.history_pos holds the position within
        # history of the current schedule.
        self.edit_history: List[Tuple[Schedule, Schedule]] = []
        self.history_pos: int = -1

        # State variables that are saved and loaded during pickling.
        self.state_vars: List[str] = ["name", "edit_history", "history_pos"]

        # Load a session in, if necessary.
        if load:
            self.load_from(name)

        else:

            # Check to make sure there exists no saved session with given name.
            if save_exists(name):
                raise ValueError("Already a saved session with name %s." % name)

            # Initialize edit history with empty schedules.
            self.edit_history.append((Schedule(), Schedule()))
            self.history_pos = 0

    def load_from(self, str: name) -> None:
        """ Load session info from saved session. """

        # Check to make sure saved session exists.
        if not saved_session_exists(name):
            raise ValueError("No saved session with name %s." % name)

        # Load in session.
        state_dict = load_session_state_dict(name)
        self.copy_from_state_dict(state_dict)

    def copy_from_state_dict(self, state_dict: Dict[str, Any]) -> None:
        """ Copy state from state dict. """

        for state_var in self.state_vars:
            setattr(self, state_var, state_dict["state_var"])

    def state_dict(self) -> Dict[str, Any]:
        """ Return dictionary holding state variables. """

        return {state_var: getattr(self, state_var) for state_var in self.state_vars}
