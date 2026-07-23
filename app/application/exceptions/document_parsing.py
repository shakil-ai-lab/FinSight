from .base import ApplicationError


class DocumentParsingError(ApplicationError):
    """Raised when document parsing fails."""