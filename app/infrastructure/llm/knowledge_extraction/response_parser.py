import json

from app.core.logging import get_logger


from app.application.exceptions import ResponseParsingError

logger = get_logger(__name__)

class ResponseParser:
    """
    Parses the raw response returned by Gemini into a Python dictionary.

    Responsibility:
        Raw LLM response -> dict
    """

    # def parse(self, response: str) -> dict:
    #     """
    #     Convert the JSON response from Gemini into a Python dictionary.

    #     Args:
    #         response: Raw JSON string returned by Gemini.

    #     Returns:
    #         Parsed dictionary.

    #     Raises:
    #         ResponseParsingError:
    #             If the response is not valid JSON.
    #     """
    #     try:

    #         logger.info("Parsing LLM JSON response.")
    #         return json.loads(response)

    #     except json.JSONDecodeError as exc:
    #         raise ResponseParsingError(
    #             "Gemini returned invalid JSON."
    #         ) from exc

        
    def parse(self, response: str) -> dict:
        try:
            logger.info("Parsing LLM JSON response.")

            response = response.strip()

            if response.startswith("```json"):
                response = response.removeprefix("```json").strip()

            if response.startswith("```"):
                response = response.removeprefix("```").strip()

            if response.endswith("```"):
                response = response.removesuffix("```").strip()

            data = json.loads(response)

            return data

        except json.JSONDecodeError as exc:
            raise ResponseParsingError(
                "Gemini returned invalid JSON."
            ) from exc