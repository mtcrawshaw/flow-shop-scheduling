""" Functions for saving and loading schedule sessions. """

import os
import pickle
from typing import Dict, Any


STORAGE_DIR = "data"


def saved_session_exists(name: str) -> bool:
    """ Return True if there exists a saved session with name ``name``. """

    return os.path.isfile(filename_from_name(name))


def save_session(session: "Session"):
    """ Save session ``session`` to disk. """

    # Get state dictionary and filename.
    state_dict = session.state_dict()
    session_filename = filename_from_name(state_dict["name"])

    # Create directory if it doesn't exist.
    save_dir = os.path.dirname(session_filename)
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)

    # Save state dictionary.
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

    return os.path.join(STORAGE_DIR, "%s.pkl" % name)
