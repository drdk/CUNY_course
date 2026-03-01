import logging
from typing import Optional, Annotated
from logging import Logger, LogRecord, Filter


Int0to50 = Annotated[int, "range[0, 51]"]


class EndpointFilter(Filter):
    """
    A logging filter that excludes log records containing a specific endpoint.

    This filter is used to exclude log messages that contain the "/status/" endpoint,
    preventing them from being logged.

    Args:
        endpoints (list): A list of endpoint strings to be filtered out.

    Methods:
        filter(record: LogRecord) -> bool: Determines if the log record should
            be logged.
    """

    def __init__(self, endpoints: list):
        self.endpoints = endpoints

    def filter(self, record: LogRecord) -> bool:
        """
        Determine if the log record should be logged.

        Args:
            record (LogRecord): The log record to be checked.

        Returns:
            bool: True if the log record does not contain the "/status/" endpoint,
                  False otherwise.
        """
        message = record.getMessage()
        return all(message.find(endpoint) == -1 for endpoint in self.endpoints)


def getlogger(
    target: object, format: Optional[str] = None, level: Int0to50 = 0
) -> Logger:
    """Returns a logger with the specified name and logging level.

    Args:
        target (object): Instantiated class to be targeted with logger
        format (str, optional): Format for logging output. Defaults to level - message.
        level (Int0to50, optional): Logging level. Choose between following levels.\n
            0 (NOTSET): When set on a logger, indicates that ancestor loggers
                are to be consulted to determine the effective level. If that still
                resolves to NOTSET, then all events are logged. When set on a handler,
                all events are handled.\n
            10 (DEBUG): Detailed information, typically only of interest to a
                developer trying to diagnose a problem.\n
            20 (INFO): Confirmation that things are working as expected.\n
            30 (WARNING): An indication that something unexpected happened, or
                that a problem might occur in the near future (e.g. ‘disk space low’).
                The software is still working as expected.\n
            40 (ERROR): Due to a more serious problem, the software has not been
                able to perform some function.\n
            50 (CRITICAL): A serious error, indicating that the program itself
                may be unable to continue running.\n Defaults to 0/NOTSET.

    Returns:
        Logger: A logger with the specified name and level.

    Raises:
        ValueError: If the `level` is outside the range [0, 50].
    """
    if format is None:
        logging.basicConfig(
            # format="%(asctime)s %(levelname)-8s %(message)s",
            format="%(levelname)-9s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    else:
        logging.basicConfig(
            format=format,
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    if not 0 <= level <= 50:
        raise ValueError("level must be between 0 and 50, inclusive.")
    logger = logging.getLogger(name=target.__class__.__name__)
    logger.setLevel(level=level)
    return logger
