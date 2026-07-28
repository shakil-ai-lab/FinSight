from __future__ import annotations

from .base import ApplicationError


class DecisionSupportError(ApplicationError):
    """
    Base exception for the Decision Support capability.
    """


class DecisionSupportResponseParsingError(DecisionSupportError):
    """
    Raised when the LLM returns an invalid Decision Support response.
    """