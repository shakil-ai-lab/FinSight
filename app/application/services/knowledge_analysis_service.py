from __future__ import annotations



from app.application.models import AnalysisInsights, ExtractedKnowledge


class KnowledgeAnalysisService:
    """
    Defines the application capability responsible for
    analyzing extracted business knowledge.
    """

    
    def analyze(
        self,
        knowledge: ExtractedKnowledge,
    ) -> AnalysisInsights:
        """
        Produce analytical insights from extracted knowledge.
        """
        raise NotImplementedError