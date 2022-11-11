"""Log initializer functions for using as decorators."""
import functools
import logging


def _generate_log(path, log_level):
    """Create a logger object with specific attributes.

    Args:
        path (str): File to log
        log_level (logging.level): Level of logging, ERROR/DEBUG

    Returns:
        Logger object: the logger object to log.
    """
    # Create a logger and set the level.
    logger = logging.getLogger("LogError")
    logger.setLevel(log_level)

    # Create file handler, log format and add the format to file handler
    file_handler = logging.FileHandler(path)
    log_format = "%(levelname)s %(asctime)s %(message)s"
    formatter = logging.Formatter(log_format)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return logger


def log(path="./tools/log.error.log", debug=False):
    """Parent function to take arguments.

    Args:
        path (str, optional): Defaults to "./tools/log.error.log".
        debug (bool, optional): Defaults to False.

    Returns:
        degorator: error_log
    """

    def error_log(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                # if debug enabled, log everything on debug.log file.
                if debug:
                    logger = _generate_log(
                        path.replace("error", "debug"), logging.DEBUG
                    )
                    error_msg = (
                        " Debug message originated from / " + func.__name__ + "\n"
                    )
                    logger.debug(error_msg)
                return func(*args, **kwargs)
            except Exception as e:
                # If it throws an error `Exception` will be called.
                logger = _generate_log(path, logging.ERROR)
                error_msg = " Error has occurred at / " + func.__name__ + "\n"
                logger.exception(error_msg)

                return e  # Or whatever message you want.

        return wrapper

    return error_log
