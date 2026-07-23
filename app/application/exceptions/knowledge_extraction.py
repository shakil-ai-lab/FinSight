from .base import ApplicationError


class KnowledgeExtractionError(ApplicationError):
    """Base exception for knowledge extraction."""


class PromptGenerationError(KnowledgeExtractionError):
    """Prompt generation failed."""


class LLMGenerationError(KnowledgeExtractionError):
    """LLM request failed."""


class InvalidLLMResponseError(KnowledgeExtractionError):
    """LLM returned an invalid response."""


class ResponseParsingError(KnowledgeExtractionError):
    """Failed to parse LLM response."""


class MappingError(KnowledgeExtractionError):
    """Failed to map extracted knowledge."""