from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional

from .request import AnalysisRequest, DocumentType


class CapabilityType(Enum):
    """
    Business capabilities supported by FinSight.

    These represent the major stages of the analysis workflow.
    """

    PLANNING = "planning"
    DOCUMENT_ACQUISITION = "document_acquisition"
    KNOWLEDGE_EXTRACTION = "knowledge_extraction"
    KNOWLEDGE_ANALYSIS = "knowledge_analysis"
    DECISION_SUPPORT = "decision_support"
    PRESENTATION = "presentation"


class PlanStatus(Enum):
    """
    Lifecycle states of an analysis plan.
    """

    CREATED = "created"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass(slots=True)
class AnalysisPlan:
    """
    Represents the execution strategy for an analysis request.

    Purpose
    -------
    Defines what FinSight needs to do before execution begins.

    Created By
    ----------
    Planning Capability

    Consumed By
    -----------
    - Document Acquisition
    - LangGraph Workflow
    - Analysis State
    """

    request: AnalysisRequest

    required_documents: tuple[DocumentType, ...] = field(default_factory=tuple)

    capabilities: tuple[CapabilityType, ...] = field(default_factory=tuple)

    status: PlanStatus = PlanStatus.CREATED

    created_at: datetime = field(default_factory=datetime.utcnow)

    description: Optional[str] = None