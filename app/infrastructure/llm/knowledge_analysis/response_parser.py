from __future__ import annotations

import json

from app.application.exceptions.knowledge_analysis import (
    ResponseParsingError,
)


class ResponseParser:
    """
    Parses the Gemini analysis response into a Python dictionary.
    """

    def parse(
        self,
        response: str,
    ) -> dict:

        try:

            cleaned = response.strip()

            # Remove opening markdown fence
            if cleaned.startswith("```json"):
                cleaned = cleaned[len("```json"):]

            elif cleaned.startswith("```"):
                cleaned = cleaned[len("```"):]

            # Remove closing markdown fence
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]

            cleaned = cleaned.strip()

            return json.loads(cleaned)

        except json.JSONDecodeError as exc:

            raise ResponseParsingError(
                "Failed to parse analysis response."
            ) from exc