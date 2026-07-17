from app.infrastructure.document_sources.sec.sec_client import SECClient


def main() -> None:
    client = SECClient(
        user_agent="FinSight/1.0 sanjaralap@gmail.com",
    )

    # Replace with a real SEC filing URL
    url = (
        "https://www.sec.gov/Archives/edgar/data/320193/"
        "000032019324000123/aapl-20240928.htm"
    )

    content = client.download_document(url)

    with open("data/raw/sec/apple_10k.html", "w", encoding="utf-8") as file:
        file.write(content)

    print("=" * 80)
    print("Download successful")
    print("=" * 80)
    print(f"Characters downloaded: {len(content)}")
    print()
    print(content[:1000])  # Print the first 1000 characters


if __name__ == "__main__":
    main()