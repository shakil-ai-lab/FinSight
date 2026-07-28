from __future__ import annotations

from app.application.exceptions import MappingError
from app.application.models import (
    AnalysisInsights,
    ExtractedKnowledge,
)
from app.domain.insights import (
    CommunicationAnalysis,
    ConsistencyAnalysis,
    QuarterComparison,
    TrendAnalysis,
)

from app.application.models import (
    AnalysisInsights,
    ExtractedKnowledge,
)


class AnalysisMapper:

    def map(
    self,
    data: dict,
    knowledge: ExtractedKnowledge,
) -> AnalysisInsights:

        try:

            quarter = None
            if "quarter_comparison" in data:
                quarter = self._map_quarter(
                    data["quarter_comparison"]
                )

            trend = None
            if "trend_analysis" in data:
                trend = self._map_trend(
                    data["trend_analysis"]
                )

            consistency = self._map_consistency(
                data["consistency_analysis"],
                knowledge,
            )

            communication = self._map_communication(
                data["communication_analysis"],
                knowledge,
            )

            return AnalysisInsights(
                quarter_comparison=quarter,
                trend_analysis=trend,
                consistency_analysis=consistency,
                communication_analysis=communication,
            )

        except (KeyError, TypeError, ValueError) as exc:
            raise MappingError(
                "Failed to map analysis insights."
            ) from exc

    def _map_quarter(self, data):
        return QuarterComparison(**data)

    def _map_trend(self, data):
        return TrendAnalysis(**data)

    def _map_consistency(
    self,
    data,
    knowledge: ExtractedKnowledge,
) -> ConsistencyAnalysis:

        return ConsistencyAnalysis(
            financial_snapshot=knowledge.financial_snapshot,
            management_discussion=knowledge.management_discussion,
            guidance_summary=knowledge.guidance_summary,
            consistency_score=data.get("consistency_score"),
            supporting_observations=tuple(
                data.get("supporting_observations", [])
            ),
            inconsistencies=tuple(
                data.get("inconsistencies", [])
            ),
            summary=data.get("summary"),
        )

    def _map_communication(
    self,
    data,
    knowledge: ExtractedKnowledge,
) -> CommunicationAnalysis:

        return CommunicationAnalysis(
            management_discussion=knowledge.management_discussion,
            transcript_analysis=knowledge.transcript_analysis,
            guidance_summary=knowledge.guidance_summary,
            communication_quality=data.get("communication_quality"),
            confidence_level=data.get("confidence_level"),
            transparency_assessment=data.get("transparency_assessment"),
            key_messages=tuple(
                data.get("key_messages", [])
            ),
            notable_concerns=tuple(
                data.get("notable_concerns", [])
            ),
            summary=data.get("summary"),
        )