import json


class ResponseParser:
    """
    Parses the raw response returned by Gemini into a Python dictionary.

    Responsibility:
        Raw LLM response -> dict
    """

    def parse(self, response: str) -> dict:
        """
        Convert the JSON response from Gemini into a Python dictionary.

        Args:
            response: Raw JSON string returned by Gemini.

        Returns:
            Parsed dictionary.

        Raises:
            ValueError:
                If the response is not valid JSON.
        """
        try:
            return json.loads(response)

        except json.JSONDecodeError as exc:
            raise ValueError("Gemini returned invalid JSON.") from exc