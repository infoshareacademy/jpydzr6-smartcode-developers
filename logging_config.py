import logging
import os

def create_log_directory() -> str:
    """
    Creates the log directory if it does not exist and returns the log directory path.

    Returns:
        str: The path to the log directory.
    """
    project_dir = os.path.abspath(os.path.dirname(__file__))
    log_dir = os.path.join(project_dir, "logs")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    return log_dir

def get_logger(debug: bool = False) -> logging.Logger:
    """
    Returns a pre-configured logger.
    Logs messages to a file, and optionally to the console based on `debug`.

    Args:
        debug (bool): If True, logs to the console as well (default is False).

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    if not logger.hasHandlers(): # Prevent adding multiple handlers
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        log_dir = create_log_directory()

        # File handler (logs to a file)
        file_handler = logging.FileHandler(f"{log_dir}/app.log")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Console handler (prints to console if debug is True)
        if debug:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

    return logger