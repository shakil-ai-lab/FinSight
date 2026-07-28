from __future__ import annotations

from .base import ApplicationError


class KnowledgeAnalysisError(ApplicationError):
    """
    Base exception for all Knowledge Analysis failures.
    """


class PromptGenerationError(KnowledgeAnalysisError):
    """
    Raised when building the analysis prompt fails.
    """


class LLMGenerationError(KnowledgeAnalysisError):
    """
    Raised when the LLM cannot generate an analysis response.
    """


class InvalidLLMResponseError(KnowledgeAnalysisError):
    """
    Raised when the LLM returns an empty or otherwise
    invalid response.
    """


class ResponseParsingError(KnowledgeAnalysisError):
    """
    Raised when the LLM response cannot be parsed.
    """


class MappingError(KnowledgeAnalysisError):
    """
    Raised when parsed analysis data cannot be mapped
    into domain models.
    """