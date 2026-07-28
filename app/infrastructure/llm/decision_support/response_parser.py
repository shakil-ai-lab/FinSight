from __future__ import annotations

import json

from app.application.exceptions.decision_support import (
    DecisionSupportResponseParsingError,
)


class ResponseParser:
    """
    Parses the raw LLM response produced by the Decision Support capability.

    Responsibilities
    ----------------
    - Remove Markdown code fences.
    - Parse JSON.
    - Validate that the response is a JSON object.
    """

    def parse(self, response: str) -> dict:
        """
        Parse the LLM response into a dictionary.

        Parameters
        ----------
        response:
            Raw text returned by the LLM.

        Returns
        -------
        dict
            Parsed JSON response.

        Raises
        ------
        DecisionSupportResponseParsingError
            If the response cannot be parsed.
        """

        cleaned = self._remove_markdown(response)

        try:
            parsed = json.loads(cleaned)
        except json.JSONDecodeError as exc:
            raise DecisionSupportResponseParsingError(
                "Decision Support returned invalid JSON."
            ) from exc

        if not isinstance(parsed, dict):
            raise DecisionSupportResponseParsingError(
                "Decision Support response must be a JSON object."
            )

        return parsed

    @staticmethod
    def _remove_markdown(text: str) -> str:
        """
        Remove Markdown code fences that Gemini occasionally returns.
        """

        text = text.strip()

        if text.startswith("```json"):
            text = text[7:]

        elif text.startswith("```"):
            text = text[3:]

        if text.endswith("```"):
            text = text[:-3]

        return text.strip()