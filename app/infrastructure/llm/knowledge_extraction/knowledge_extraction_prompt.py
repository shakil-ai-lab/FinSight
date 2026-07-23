from __future__ import annotations

from app.application.models.parsed_document import ParsedDocument


class KnowledgeExtractionPrompt:
    """
    Builds the prompt used for extracting structured financial knowledge
    from a parsed SEC filing.

    Responsibility:
        ParsedDocument -> Prompt (str)

    This class knows nothing about:
        - Gemini
        - JSON parsing
        - ExtractedKnowledge
        - Mapping
        - Domain objects

    It is only responsible for constructing the prompt sent to the LLM.
    """

    def build(
        self,
        document: ParsedDocument,
    ) -> str:
        """
        Build the complete prompt for the language model.
        """

        return "\n\n".join(
    [
        self._instructions(),
        self._output_rules(),
        "Return JSON using EXACTLY the following schema.",
        self._json_schema(),
        "SEC FILING",
        document.text,
    ]
)

    # ---------------------------------------------------------
    # Prompt Instructions
    # ---------------------------------------------------------

    def _instructions(self) -> str:
        """
        High-level instructions describing the extraction task.
        """

        return """
You are an expert senior financial analyst specializing in SEC filings,
annual reports (10-K), quarterly reports (10-Q), and earnings call
transcripts.

Your task is to extract structured financial knowledge from the provided
document.

Carefully analyze the entire document and identify only information that
is explicitly stated.

Never invent information.

Never estimate values.

Never infer values that are not directly supported by the document.

If a value cannot be found:

- use null for scalar values
- use [] for arrays
- use "" only when an empty string is appropriate

Extract information as accurately as possible.

If the document is a 10-K:

- fiscal_quarter should be null.

If the document is a 10-Q:

- populate fiscal_quarter if available.

If the document is not an earnings transcript,
return an empty transcript_analysis object using the required schema.

If a value appears multiple times in the filing,
prefer the value from the consolidated financial statements
over narrative discussion.

If this document is NOT an earnings call transcript,
return transcript_analysis with:

key_topics=[]

analyst_questions=[]

management_responses=[]

notable_announcements=[]

unanswered_concerns=[]

company populated when known

fiscal_year populated when known

fiscal_quarter populated when known

If no management guidance exists,
populate guidance_summary with

null numeric/string values

empty arrays

Do not invent guidance.

Likewise, if guidance information is unavailable,
return the guidance_summary object with null values and empty arrays.

Every section of the JSON MUST be returned.

Do NOT omit any top-level object.

Required top-level objects:

- financial_snapshot
- business_segments
- management_discussion
- risk_assessment
- guidance_summary
- transcript_analysis

Do not abbreviate business segment names.

Use the exact names used by management.

Return concise bullet-style sentences.

Do not return long paragraphs.

Choose severity using:

low

medium

high

Never use:

critical

moderate

minor

severe

The JSON structure must EXACTLY match the provided schema.

Do not rename fields.

Do not add new fields.

Do not remove fields.

Return ONLY valid JSON.

Do not include explanations.

Do not include markdown.

Do not include code fences.

Do not include comments.
"""

    def _output_rules(self) -> str:
        """
        Returns formatting and serialization rules
        for the language model.
        """

        return """
OUTPUT RULES

1. Return ONLY valid JSON.

2. Do not wrap the JSON inside markdown.

3. Do not use ```json.

4. Do not include explanations.

5. Do not include comments.

6. Do not add additional top-level fields.

7. Every required top-level object must exist.

8. Missing numeric values must be null.

9. Missing string values must be null unless the schema
   specifically expects an empty string.

10. Missing arrays must be [].

11. Decimal values must be numbers.

12. Percentages should be numeric.

Correct:
32.5

Incorrect:
"32.5%"
"32.5 percent"

13. Currency values should be numeric.

Correct:
391035000000

Incorrect:
"$391,035"

14. fiscal_year must be an integer.

15. fiscal_quarter must be an integer or null.

16. Risk severity must be exactly one of:

- low
- medium
- high

17. Do not hallucinate.

18. If a section is unavailable, return the object with
null values and empty arrays.

19. Every field in the schema must be present.

20. Follow the schema exactly.
"""

    # ---------------------------------------------------------
    # JSON Schema
    # ---------------------------------------------------------

    def _json_schema(self) -> str:
        """
        JSON contract expected by ExtractedKnowledgeMapper.
        """

        return r"""
{
  "financial_snapshot": {
    "company": "string",
    "fiscal_year": 2025,
    "fiscal_quarter": null,
    "revenue": null,
    "gross_margin": null,
    "operating_income": null,
    "net_income": null,
    "earnings_per_share": null,
    "operating_cash_flow": null
  },

  "business_segments": {

    "company": "string",

    "fiscal_year": 2025,

    "fiscal_quarter": null,

    "segments": [

      {

        "name": "string",

        "revenue": null,

        "operating_income": null,

        "growth_rate": null,

        "description": "string"

      }

    ]
  },

  "management_discussion": {

    "company": "string",

    "fiscal_year": 2025,

    "fiscal_quarter": null,

    "business_summary": "string",

    "performance_drivers": [

      "string"

    ],

    "operational_highlights": [

      "string"

    ],

    "strategic_initiatives": [

      "string"

    ],

    "management_commentary": [

      "string"

    ]

  },

  "risk_assessment": {

    "company": "string",

    "fiscal_year": 2025,

    "fiscal_quarter": null,

    "overall_summary": "string",

    "risks": [

      {

        "title": "string",

        "category": "string",

        "description": "string",

        "severity": "low",

        "evidence": "string"

      }

    ]

  },

  "guidance_summary": {

    "company": "string",

    "fiscal_year": 2025,

    "fiscal_quarter": null,

    "revenue_guidance": null,

    "earnings_guidance": null,

    "margin_guidance": null,

    "cash_flow_guidance": null,

    "capital_expenditure_guidance": null,

    "strategic_outlook": [

      "string"

    ],

    "management_expectations": [

      "string"

    ]

  },

  "transcript_analysis": {

    "company": "string",

    "fiscal_year": 2025,

    "fiscal_quarter": null,

    "key_topics": [

      "string"

    ],

    "analyst_questions": [

      "string"

    ],

    "management_responses": [

      "string"

    ],

    "notable_announcements": [

      "string"

    ],

    "unanswered_concerns": [

      "string"

    ]

  }

}
"""