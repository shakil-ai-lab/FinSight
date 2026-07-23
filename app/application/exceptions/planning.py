from .base import ApplicationError


class PlanningError(ApplicationError):
    """Raised when analysis planning fails."""