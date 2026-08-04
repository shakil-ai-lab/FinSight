from __future__ import annotations

import requests

from app.config.settings import settings


class SECClient:
    """
    Thin HTTP client for communicating with the SEC EDGAR system.
    """

    def __init__(self) -> None:
        self._user_agent = settings.SEC_USER_AGENT
        self._timeout = settings.SEC_TIMEOUT

    def download_document(self, url: str) -> str:
        response = requests.get(
            url,
            headers={
                "User-Agent": self._user_agent,
                "Accept-Encoding": "gzip, deflate",
                
            },
            timeout=self._timeout,
        )

        response.raise_for_status()

        return response.text

    def download_json(
        self,
        url: str,
    ) -> dict:
        response = requests.get(
            url,
            headers={
                "User-Agent": self._user_agent,
                "Accept-Encoding": "gzip, deflate",
                
            },
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