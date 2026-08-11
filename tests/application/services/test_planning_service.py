from app.application.services.planning_service import PlanningService
from app.domain.analysis import AnalysisRequest, AnalysisType
from app.domain.documents import DocumentType
from app.domain.fiscal import FiscalQuarter


def test_plan_preserves_fiscal_quarter_in_document_request():
    service = PlanningService()

    request = AnalysisRequest(
        company="Apple",
        ticker="AAPL",
        analysis_type=AnalysisType.QUARTERLY,
        fiscal_year=2025,
        fiscal_quarter=FiscalQuarter.Q1,
    )

    plan = service.plan(request)

    assert len(plan.document_requests) == 1

    document_request = plan.document_requests[0]

    assert document_request.document_type == DocumentType.TEN_Q
    assert document_request.fiscal_year == 2025
    assert document_request.fiscal_quarter is FiscalQuarter.Q1

def test_plan_preserves_none_fiscal_quarter_for_annual_request():
    service = PlanningService()

    request = AnalysisRequest(
        company="Apple",
        ticker="AAPL",
        analysis_type=AnalysisType.ANNUAL,
        fiscal_year=2025,
        fiscal_quarter=None,
    )

    plan = service.plan(request)

    document_request = plan.document_requests[0]

    assert document_request.document_type == DocumentType.TEN_K
    assert document_request.fiscal_year == 2025
    assert document_request.fiscal_quarter is None    