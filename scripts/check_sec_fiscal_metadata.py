from bs4 import BeautifulSoup

from app.infrastructure.document_sources.sec.sec_client import SECClient


def main() -> None:
    client = SECClient()

    url = (
        "https://www.sec.gov/Archives/edgar/data/"
        "320193/000032019324000081/"
        "aapl-20240629.htm"
    )

    html = client.download_document(url)

    print(f"Downloaded filing: {len(html):,} characters")
    print()

    soup = BeautifulSoup(html, "html.parser")

    # Search the filing for the XBRL fiscal-period concepts.
    target_names = {
        "DocumentFiscalYearFocus",
        "DocumentFiscalPeriodFocus",
    }

    found = False

    for element in soup.find_all():
        name = element.get("name")

        if not name:
            continue

        local_name = name.split(":")[-1]

        if local_name in target_names:
            found = True

            print("XBRL fiscal metadata found")
            print("-" * 60)
            print(f"name: {name}")
            print(f"tag: {element.name}")
            print(f"text: {element.get_text(strip=True)}")
            print(f"attributes: {element.attrs}")
            print()

    if not found:
        print(
            "DocumentFiscalYearFocus / "
            "DocumentFiscalPeriodFocus were not found."
        )


if __name__ == "__main__":
    main()