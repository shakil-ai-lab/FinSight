from __future__ import annotations

from google import genai

from app.config.settings import settings


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
        """

        response = self._client.models.generate_content(
            model=self._model,
            contents=prompt,
        )

        return response.text