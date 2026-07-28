from __future__ import annotations

from app.application.models import DecisionResult
from app.application.ports.presentation_engine import PresentationEngine

from app.domain.presentation import AnalystBrief


class PresentationService:
    """
    Application service responsible for producing the
    final analyst brief.
    """

    def __init__(
        self,
        engine: PresentationEngine,
    ) -> None:
        self._engine = engine

    def present(
        self,
        result: DecisionResult,
    ) -> AnalystBrief:

        return self._engine.present(result)