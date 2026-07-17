from __future__ import annotations

from dataclasses import dataclass

import requests


@dataclass(slots=True, frozen=True)
class SECClient:
    """
    Thin HTTP client for communicating with the SEC EDGAR system.

    This class is responsible only for downloading raw filing
    content from SEC endpoints. It contains no business logic and
    has no knowledge of domain objects.
    """

    user_agent: str
    timeout: int = 30

    def download_document(
        self,
        url: str,
    ) -> str:
        """
        Download the raw document located at the given SEC URL.

        Args:
            url:
                Absolute SEC document URL.

        Returns:
            Raw document text.

        Raises:
            requests.HTTPError:
                If the SEC request fails.
        """
        response = requests.get(
            url,
            headers={
                "User-Agent": self.user_agent,
                "Accept-Encoding": "gzip, deflate",
                "Host": "www.sec.gov",
            },
            timeout=self.timeout,
        )

        response.raise_for_status()

        return response.text