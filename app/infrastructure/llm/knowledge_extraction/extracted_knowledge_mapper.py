from __future__ import annotations

from decimal import Decimal, InvalidOperation
from typing import Any

from app.application.models import ExtractedKnowledge
from app.domain.knowledge import (
    BusinessSegment,
    BusinessSegments,
    FinancialSnapshot,
    GuidanceSummary,
    ManagementDiscussion,
    RiskAssessment,
    RiskSeverity,
    TranscriptAnalysis,
)


class ExtractedKnowledgeMapper:
    """
    Maps validated LLM response data into immutable domain objects.

    Responsibility:
        dict -> ExtractedKnowledge

    This class acts as the normalization boundary between
    the LLM response and the domain model.
    """

    def map(
        self,
        data: dict[str, Any],
    ) -> ExtractedKnowledge:
        """
        Full mapping is intentionally deferred until all
        component mappers are implemented.
        """
        raise NotImplementedError(
            "Full knowledge mapping has not been implemented yet."
        )

    # ---------------------------------------------------------
    # Financial Snapshot
    # ---------------------------------------------------------

    def _map_financial_snapshot(
        self,
        data: dict[str, Any],
    ) -> FinancialSnapshot:
        """
        Map a financial snapshot dictionary into a
        FinancialSnapshot domain object.
        """

        return FinancialSnapshot(
            company=self._require(data, "company"),
            fiscal_year=self._to_int(
                self._require(data, "fiscal_year")
            ),
            fiscal_quarter=self._to_int(
                data.get("fiscal_quarter")
            ),
            revenue=self._to_decimal(
                data.get("revenue")
            ),
            gross_margin=self._to_decimal(
                data.get("gross_margin")
            ),
            operating_income=self._to_decimal(
                data.get("operating_income")
            ),
            net_income=self._to_decimal(
                data.get("net_income")
            ),
            earnings_per_share=self._to_decimal(
                data.get("earnings_per_share")
            ),
            operating_cash_flow=self._to_decimal(
                data.get("operating_cash_flow")
            ),
        )

    # ---------------------------------------------------------
    # Business Segments
    # ---------------------------------------------------------

    def _map_business_segment(
        self,
        data: dict[str, Any],
    ) -> BusinessSegment:
        """
        Map a single business segment dictionary into a
        BusinessSegment domain object.
        """

        return BusinessSegment(
            name=self._require(data, "name"),
            revenue=self._to_decimal(
                data.get("revenue")
            ),
            operating_income=self._to_decimal(
                data.get("operating_income")
            ),
            growth_rate=self._to_decimal(
                data.get("growth_rate")
            ),
            description=data.get("description"),
        )

    def _map_business_segments(
        self,
        data: dict[str, Any],
    ) -> BusinessSegments:
        """
        Map a business segments dictionary into a
        BusinessSegments domain object.
        """

        segments = tuple(
            self._map_business_segment(segment)
            for segment in data.get("segments", [])
        )

        return BusinessSegments(
            company=self._require(data, "company"),
            fiscal_year=self._to_int(
                self._require(data, "fiscal_year")
            ),
            fiscal_quarter=self._to_int(
                data.get("fiscal_quarter")
            ),
            segments=segments,
        )

    # ---------------------------------------------------------
    # Remaining Mappers
    # ---------------------------------------------------------

    def _map_management_discussion(
    self,
    data: dict[str, Any],
    ) -> ManagementDiscussion:
        """
        Map a management discussion dictionary into a
        ManagementDiscussion domain object.
        """

        return ManagementDiscussion(
            company=self._require(data, "company"),
            fiscal_year=self._to_int(
                self._require(data, "fiscal_year")
            ),
            fiscal_quarter=self._to_int(
                data.get("fiscal_quarter")
            ),
            business_summary=data.get("business_summary"),
            performance_drivers=self._to_tuple(
                data.get("performance_drivers")
            ),
            operational_highlights=self._to_tuple(
                data.get("operational_highlights")
            ),
            strategic_initiatives=self._to_tuple(
                data.get("strategic_initiatives")
            ),
            management_commentary=self._to_tuple(
                data.get("management_commentary")
            ),
        )

    def _map_risk_assessment(
        self,
        data: dict[str, Any],
    ) -> RiskAssessment:
        raise NotImplementedError

    def _map_guidance_summary(
        self,
        data: dict[str, Any],
    ) -> GuidanceSummary:
        raise NotImplementedError

    def _map_transcript_analysis(
        self,
        data: dict[str, Any],
    ) -> TranscriptAnalysis:
        raise NotImplementedError

    # ---------------------------------------------------------
    # Helper Methods
    # ---------------------------------------------------------

    def _require(
        self,
        data: dict[str, Any],
        key: str,
    ) -> Any:
        """
        Return a required value from a dictionary.
        """

        if key not in data:
            raise ValueError(
                f"Missing required field '{key}'."
            )

        value = data[key]

        if value is None:
            raise ValueError(
                f"Required field '{key}' cannot be null."
            )

        return value

    def _to_decimal(
        self,
        value: Any,
    ) -> Decimal | None:
        """
        Convert a value into a Decimal.
        """

        if value is None:
            return None

        if isinstance(value, Decimal):
            return value

        if isinstance(value, (int, float)):
            return Decimal(str(value))

        if isinstance(value, str):
            value = value.strip()

            if not value:
                return None

            value = value.replace(",", "")

            try:
                return Decimal(value)

            except InvalidOperation as exc:
                raise ValueError(
                    f"Invalid decimal value '{value}'."
                ) from exc

        raise ValueError(
            f"Unsupported decimal type '{type(value).__name__}'."
        )

    def _to_int(
        self,
        value: Any,
    ) -> int | None:
        """
        Convert a value into an integer.
        """

        if value is None:
            return None

        if isinstance(value, int):
            return value

        if isinstance(value, float):
            return int(value)

        if isinstance(value, str):
            value = value.strip()

            if not value:
                return None

            try:
                return int(value)

            except ValueError as exc:
                raise ValueError(
                    f"Invalid integer value '{value}'."
                ) from exc

        raise ValueError(
            f"Unsupported integer type '{type(value).__name__}'."
        )

    def _to_tuple(
        self,
        value: Any,
    ) -> tuple[str, ...]:
        """
        Convert a sequence into an immutable tuple.
        """

        if value is None:
            return ()

        if isinstance(value, tuple):
            return value

        if isinstance(value, list):
            return tuple(
                str(item)
                for item in value
            )

        raise ValueError(
            f"Expected list or tuple, got '{type(value).__name__}'."
        )

    def _to_severity(
        self,
        value: Any,
    ) -> RiskSeverity:
        """
        Convert a string into a RiskSeverity enum.
        """

        if isinstance(value, RiskSeverity):
            return value

        if not isinstance(value, str):
            raise ValueError(
                "Risk severity must be a string."
            )

        mapping = {
            "low": RiskSeverity.LOW,
            "medium": RiskSeverity.MEDIUM,
            "high": RiskSeverity.HIGH,
        }

        normalized = value.strip().lower()

        try:
            return mapping[normalized]

        except KeyError as exc:
            raise ValueError(
                f"Unknown risk severity '{value}'."
            ) from exc