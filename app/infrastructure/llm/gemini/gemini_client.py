from __future__ import annotations

from google import genai

from app.config.settings import settings

from time import sleep

from google.genai.errors import ServerError

from app.core.logging import get_logger

from app.application.exceptions import (
    LLMGenerationError,
    InvalidLLMResponseError,
)

logger = get_logger(__name__)

class GeminiClient:
    """
    Thin infrastructure client responsible for communicating
    with the Gemini API.
    """

    def __init__(self) -> None:
        self._client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

        self._model = settings.MODEL_NAME

    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Send a prompt to Gemini and return the generated text.

        Retries automatically when Gemini is temporarily unavailable.
        """

        max_retries = 3

        for attempt in range(max_retries):
            try:
                response = self._client.models.generate_content(
                    model=self._model,
                    contents=prompt,
                )

                text = response.text

                if text is None or not text.strip():
                    raise InvalidLLMResponseError(
                        "Gemini returned an empty response."
                    )

                return text

            except ServerError as exc:

                if attempt < max_retries - 1:
                    wait_time = 5 * (attempt + 1)

                    logger.warning(
                        "Gemini unavailable. Retrying in %s seconds...",
                        wait_time,
                    )

                    sleep(wait_time)
                    continue

                raise LLMGenerationError(
                    "Gemini service is temporarily unavailable."
                ) from exc

            except InvalidLLMResponseError:
                raise

            except Exception as exc:
                raise LLMGenerationError(
                    "Failed to generate content using Gemini."
                ) from exc