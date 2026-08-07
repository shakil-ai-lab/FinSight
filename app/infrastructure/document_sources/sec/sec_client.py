from __future__ import annotations

import requests

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from app.config.settings import settings


class SECClient:
    """
    Thin HTTP client for communicating with the SEC EDGAR system.
    """

    def __init__(self) -> None:
        self._timeout = settings.SEC_TIMEOUT

        self._headers = {
            "User-Agent": settings.SEC_USER_AGENT,
            "Accept-Encoding": "gzip, deflate",
        }

        retry_strategy = Retry(
            total=3,
            connect=3,
            read=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)

        self._session = requests.Session()
        self._session.mount("https://", adapter)
        self._session.mount("http://", adapter)

    def download_document(self, url: str) -> str:
        response = self._session.get(
            url,
            headers=self._headers,
            timeout=self._timeout,
        )

        response.raise_for_status()

        return response.text

    def download_json(
        self,
        url: str,
    ) -> dict:
        response = self._session.get(
            url,
            headers=self._headers,
            timeout=self._timeout,
        )

        response.raise_for_status()

        return response.json()

    def get_company_tickers(self) -> dict:
        return self.download_json(
            "https://www.sec.gov/files/company_tickers.json"
        )

    def get_company_submissions(
        self,
        cik: int,
    ) -> dict:
        cik_str = str(cik).zfill(10)

        return self.download_json(
            f"https://data.sec.gov/submissions/CIK{cik_str}.json"
        )

    