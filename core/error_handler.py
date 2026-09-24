from core.logger import logger
from core.utils import print_error


def handle_error(error, context="Application"):
    """
    Handle an unexpected application error.

    The detailed error is logged for debugging,
    while the user receives a simple message.
    """
    logger.exception("%s error: %s", context, error)

    print_error(
        f"{context} failed. Check logs for more information."
    )


def safe_run(function, context="Application"):
    """
    Execute a function safely and handle unexpected errors.
    """
    try:
        return function()

    except KeyboardInterrupt:
        print_error("Operation cancelled by user.")
        logger.info("%s cancelled by user.", context)

    except Exception as error:
        handle_error(error, context)
