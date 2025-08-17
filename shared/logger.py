# shared/logger.py

import logging
import os
from datetime import datetime

def get_logger(name: str, level: int = logging.INFO, log_to_file: bool = True) -> logging.Logger:
    """
    Creates and configures a logger with stream and optional file handlers.

    Args:
        name (str): The name of the logger (typically __name__).
        level (int): Logging level (e.g., logging.INFO).
        log_to_file (bool): Whether to write logs to a file in runtime/logs.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger  # Already configured

    logger.setLevel(level)

    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler
    if log_to_file:
        log_dir = os.path.join(os.path.dirname(__file__), '..', 'runtime', 'logs')
        os.makedirs(log_dir, exist_ok=True)
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        log_file = os.path.join(log_dir, f'{name.replace(".", "_")}_{timestamp}.log')
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
