"""
    Connect to that DNS server's API and find some interesting
    sites being requested on your network for further investigation
"""

import sys
import logging
from whispers.gui.startup import startup

_LOGGER = logging.getLogger(__name__)
logging.basicConfig(level="INFO")


def main() -> int:
    """
    Start application
    """

    try:
        startup()
        return 0
    except Exception as error:
        _LOGGER.error("Error encountered!  %s", error)
        return 1


if __name__ == "__main__":
    sys.exit(main())
