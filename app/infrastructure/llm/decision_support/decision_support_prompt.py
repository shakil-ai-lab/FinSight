from __future__ import annotations

import json

from app.application.models.analysis_insights import AnalysisInsights
from app.application.models.extracted_knowledge import ExtractedKnowledge


class DecisionSupportPrompt:
    """
    Builds the prompt used by the Decision Support capability.

    This capability receives extracted financial knowledge together
    with analytical insights and produces an investment-oriented
    assessment.

    The LLM is responsible ONLY for reasoning.

    It must NOT recreate existing domain objects.
    """

    def build(
        self,
        knowledge: ExtractedKnowledge,
        insights: AnalysisInsights,
    ) -> str:
        payload = {
            "knowledge": {
                "financial_snapshot": knowledge.financial_snapshot,
                "business_segments": knowledge.business_segments,
                "risk_assessment": knowledge.risk_assessment,
                "management_discussion": knowledge.management_discussion,
                "guidance_summary": knowledge.guidance_summary,
                "transcript_analysis": knowledge.transcript_analysis,
            },
            "analysis": {
                "consistency_analysis": insights.consistency_analysis,
                "communication_analysis": insights.communication_analysis,
                "quarter_comparison": insights.quarter_comparison,
                "trend_analysis": insights.trend_analysis,
            },
        }

        return f"""
You are a Senior Equity Research Analyst.

Your objective is to evaluate the provided financial knowledge and
analytical insights and produce an investment-oriented assessment.

You are NOT extracting facts.

You are NOT recreating financial statements.

You are making professional investment judgments.

--------------------------------------------------
Instructions
--------------------------------------------------

1. Prioritize findings by materiality.

2. Separate findings into:

- Critical
- Significant
- Informational

3. Produce an overall assessment of the company.

4. Provide a balanced investment recommendation.

Recommendations should be one of:

- Strong Buy
- Buy
- Hold
- Sell
- Strong Sell

5. Write an executive summary suitable for investors.

6. Highlight the most important investment strengths.

7. Highlight the key investment risks.

--------------------------------------------------
Rules
--------------------------------------------------

• Do NOT invent facts.

• Base every conclusion only on the supplied data.

• If quarter comparison is unavailable, ignore it.

• If trend analysis is unavailable, ignore it.

• Keep the executive summary concise.

• Investment highlights should be short bullet-style statements.

• Key risks should be concise.

--------------------------------------------------
Input
--------------------------------------------------

{json.dumps(payload, default=str, indent=2)}

--------------------------------------------------
Output
--------------------------------------------------

Return ONLY valid JSON.

{{
    "overall_assessment": "...",

    "recommendation": "...",

    "critical_findings": [
        "...",
        "..."
    ],

    "significant_findings": [
        "...",
        "..."
    ],

    "informational_findings": [
        "...",
        "..."
    ],

    "executive_summary": "...",

    "investment_highlights": [
        "...",
        "..."
    ],

    "key_risks": [
        "...",
        "..."
    ]
}}
"""