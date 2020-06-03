""" Functions for saving and loading schedule sessions. """

import os

from flowshop.session import Session


STORAGE_DIR = "storage"


def saved_session_exists(name: str) -> bool:
    """ Return True if there exists a saved session with name ``name``. """

    return os.path.isfile(filename_from_name(name))


def save_session(session: Session):
    """ Save session ``session`` to disk. """

    state_dict = session.state_dict()
    session_filename = filename_from_name(state_dict["name"])
    with open(session_filename, "wb") as session_file:
        pickle.dump(state_dict, session_file)


def load_session_state_dict(name: str) -> Dict[str, Any]:
    """ Load a session state dict with name ``name`` from disk. """

    # Check to make sure saved session exists.
    if not saved_session_exists(name):
        raise ValueError("No saved session with name %s." % name)

    session_filename = filename_from_name(name)
    with open(session_filename, "rb") as session_file:
        state_dict = pickle.load(session_file)

    return state_dict


def filename_from_name(name: str) -> str:
    """ Return filename from session name. """

    return os.path.join(STORAGE_DIR, "%d.pkl" % name)
