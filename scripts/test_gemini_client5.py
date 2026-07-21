from app.infrastructure.llm.gemini import GeminiClient


def main() -> None:
    client = GeminiClient()

    response = client.generate(
        "In one sentence, explain what a balance sheet is."
    )

    print("=" * 80)
    print("Gemini Client Test")
    print("=" * 80)
    print(response)


if __name__ == "__main__":
    main()