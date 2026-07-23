from __future__ import annotations

import logging
import sys


def configure_logging(
    level: int = logging.INFO,
) -> None:
    """
    Configure application-wide logging.

    This function should be called once during application startup.
    """

    logging.basicConfig(
        level=level,
        format=(
            "%(asctime)s | "
            "%(levelname)-8s | "
            "%(name)s | "
            "%(message)s"
        ),
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
        force=True,
    )


def get_logger(
    name: str,
) -> logging.Logger:
    """
    Return a logger for the specified module.
    """
    return logging.getLogger(name)