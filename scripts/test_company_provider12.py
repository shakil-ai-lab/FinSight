from app.infrastructure.document_sources.sec.sec_client import SECClient
from app.infrastructure.document_sources.sec.sec_company_provider import (
    SECCompanyProvider,
)

client = SECClient()
provider = SECCompanyProvider(client)

company1 = provider.resolve("Apple")
company2 = provider.resolve("NVDA")
company3 = provider.resolve("Tesla")
company4 = provider.resolve("Microsoft")
company5 = provider.resolve("MSFT")

print(f"Apple: {company1}")
print(f"NVDA: {company2}")
print(f"Tesla: {company3}")
print(f"Microsoft: {company4}")
print(f"MSFT: {company5}")