from __future__ import annotations

from app.application.models.analysis_insights import AnalysisInsights
from app.application.models.decision_result import DecisionResult
from app.application.models.extracted_knowledge import ExtractedKnowledge
from app.domain.decision_support import MaterialityAssessment
from app.domain.presentation import AnalystBrief


class DecisionSupportMapper:
    """
    Maps the LLM response together with previously generated
    knowledge and analysis into the Decision Support domain
    objects.

    The LLM performs reasoning only.

    Construction of domain objects remains the responsibility
    of this mapper.
    """

    def map(
        self,
        response: dict,
        knowledge: ExtractedKnowledge,
        insights: AnalysisInsights,
    ) -> DecisionResult:
        """
        Create the DecisionResult produced by the
        Decision Support capability.
        """

        materiality = MaterialityAssessment(
            quarter_comparison=insights.quarter_comparison,
            trend_analysis=insights.trend_analysis,
            consistency_analysis=insights.consistency_analysis,
            communication_analysis=insights.communication_analysis,
            risk_assessment=knowledge.risk_assessment,
            critical_findings=tuple(
                response.get("critical_findings", [])
            ),
            significant_findings=tuple(
                response.get("significant_findings", [])
            ),
            informational_findings=tuple(
                response.get("informational_findings", [])
            ),
            overall_assessment=response.get(
                "overall_assessment"
            ),
            recommendation=response.get(
                "recommendation"
            ),
        )

        analyst_brief = AnalystBrief(
            materiality_assessment=materiality,
            executive_summary=response.get(
                "executive_summary",
                "",
            ),
            investment_highlights=tuple(
                response.get(
                    "investment_highlights",
                    [],
                )
            ),
            key_risks=tuple(
                response.get(
                    "key_risks",
                    [],
                )
            ),
            recommendation=response.get(
                "recommendation",
                "",
            ),
        )

        return DecisionResult(
            materiality_assessment=materiality,
            
        )