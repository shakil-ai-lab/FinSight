from unittest.mock import Mock

import pytest

from app.application.services.filing_discovery_service import (
    FilingDiscoveryService,
)
from app.domain.company import AvailableFilings, Company


def test_discover_resolves_company_and_discovers_filings() -> None:
    company_resolver = Mock()
    filing_discovery = Mock()

    company = Company(
        name="Apple Inc.",
        ticker="AAPL",
        cik="0000320193",
    )

    available_filings = AvailableFilings(
        company=company,
        filings=[],
    )

    company_resolver.resolve.return_value = company
    filing_discovery.discover.return_value = available_filings

    service = FilingDiscoveryService(
        company_resolver=company_resolver,
        filing_discovery=filing_discovery,
    )

    result = service.discover("AAPL")

    company_resolver.resolve.assert_called_once_with("AAPL")
    filing_discovery.discover.assert_called_once_with(company)

    assert result is available_filings


def test_discover_does_not_call_filing_discovery_when_company_resolution_fails() -> None:
    company_resolver = Mock()
    filing_discovery = Mock()

    error = ValueError("Company not found")

    company_resolver.resolve.side_effect = error

    service = FilingDiscoveryService(
        company_resolver=company_resolver,
        filing_discovery=filing_discovery,
    )

    with pytest.raises(ValueError, match="Company not found"):
        service.discover("INVALID")

    company_resolver.resolve.assert_called_once_with("INVALID")
    filing_discovery.discover.assert_not_called()