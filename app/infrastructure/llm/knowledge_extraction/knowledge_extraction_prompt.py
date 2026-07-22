from app.application.models.parsed_document import ParsedDocument


class KnowledgeExtractionPrompt:
    """
    Builds the prompt used for extracting structured financial knowledge
    from an SEC filing.

    Responsibility:
        ParsedDocument -> Prompt (str)

    This class knows nothing about:
        - Gemini
        - JSON parsing
        - ExtractedKnowledge
        - Pydantic
    """

    
    def build(document: ParsedDocument) -> str:
        return f"""
You are a senior financial analyst specializing in SEC filings.

Your task is to analyze the following SEC filing and extract the important
financial information.

Return ONLY a valid JSON object.

Rules:
- Do not include markdown.
- Do not include explanations.
- Do not invent information.
- Use null when information is unavailable.
- Preserve all numerical values exactly as written.

Return JSON using this structure:

{{
    "financial_snapshot": {{
        "company_name": null,
        "ticker": null,
        "reporting_period": null,
        "revenue": null,
        "net_income": null,
        "eps": null,
        "operating_income": null,
        "cash_and_equivalents": null
    }},
    "business_segments": [],
    "management_discussion": {{
        "summary": null
    }},
    "risk_assessment": {{
        "key_risks": []
    }},
    "guidance_summary": {{
        "guidance": null
    }},
    "transcript_analysis": null
}}

==================== SEC FILING ====================

{document.content}
"""