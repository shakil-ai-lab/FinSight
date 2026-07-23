from __future__ import annotations

from google import genai

from app.config.settings import settings

from time import sleep

from google.genai.errors import ServerError


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

                return response.text or ""

            except ServerError:

                if attempt == max_retries - 1:
                    raise

                wait_time = 5 * (attempt + 1)

                print(
                    f"Gemini unavailable. "
                    f"Retrying in {wait_time} seconds..."
                )

                sleep(wait_time)