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
                "Host": "www.sec.gov",
            },
            timeout=self._timeout,
        )

        response.raise_for_status()

        return response.text