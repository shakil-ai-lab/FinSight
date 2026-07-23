from app.core import (
    configure_logging,
    get_logger,
)

configure_logging()

logger = get_logger(__name__)

logger.debug("Debug message")

logger.info("Info message")

logger.warning("Warning message")

logger.error("Error message")