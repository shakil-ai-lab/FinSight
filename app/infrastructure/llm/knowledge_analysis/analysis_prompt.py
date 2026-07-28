from __future__ import annotations

from app.application.models import ExtractedKnowledge


class AnalysisPrompt:
    """
    Builds the prompt used for financial reasoning over
    extracted business knowledge.

    Responsibility:
        ExtractedKnowledge -> Prompt (str)

    This class knows nothing about:
        - Gemini
        - JSON parsing
        - AnalysisInsights
        - Pydantic
    """

    def build(
        self,
        knowledge: ExtractedKnowledge,
    ) -> str:

        return f"""
You are a senior equity research analyst.

Analyze the following extracted financial knowledge.

Produce JSON only.

Required JSON schema:

{{
  "consistency_analysis": {{
    "consistency_score": 0,
    "supporting_observations": [
      "..."
    ],
    "inconsistencies": [
      "..."
    ],
    "summary": "..."
  }},

  "communication_analysis": {{
    "communication_quality": "...",
    "confidence_level": "...",
    "transparency_assessment": "...",
    "key_messages": [
      "..."
    ],
    "notable_concerns": [
      "..."
    ],
    "summary": "..."
  }}
}}

Rules:

- Return valid JSON only.
- Do not wrap the JSON inside Markdown code fences.
- Do not include explanations outside the JSON.
- Base every conclusion only on the supplied knowledge.
- Do not invent facts.
- If there is insufficient evidence, return null or an empty array where appropriate.

Knowledge:

{knowledge}
"""