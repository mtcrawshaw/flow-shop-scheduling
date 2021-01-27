""" Main function to run Flowshop. """

import argparse

from flowshop.terminal_session import TerminalSession
from flowshop.files import saved_session_exists


def main(name: str) -> None:
    """ Main function. """

    # Check whether to load session or not.
    load = saved_session_exists(name)

    # Run session.
    session = TerminalSession(name=name, load=load)
    session.run()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Run Flowshop Scheduling.")
    parser.add_argument("name", type=str, help="Name of session to run.")
    args = parser.parse_args()

    main(args.name)
