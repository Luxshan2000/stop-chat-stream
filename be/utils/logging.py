import logging


def get_logger(name):
    """
    Create and configure a logger.

    Args:
        name (str): The name of the logger.

    Returns:
        logging.Logger: A configured logger instance.
    """
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logging.getLogger("sqlalchemy").setLevel(logging.CRITICAL)

    logger = logging.getLogger(name)
    return logger
