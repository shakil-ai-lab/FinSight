from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.analysis import AnalysisRequest, AnalysisPlan

class PlanningService(ABC):
    """
    Defines the application capability responsible for
    creating an analysis plan from an analysis request.
    """

    @abstractmethod
    def plan(
        self,
        request: AnalysisRequest,
    ) -> AnalysisPlan:
        """
        Create an execution plan for the requested analysis.
        """
        raise NotImplementedError