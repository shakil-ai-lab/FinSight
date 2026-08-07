# ====================================================================
#                       TEST1
# ====================================================================

# from pprint import pprint

# from app.infrastructure.document_sources.sec.sec_client import SECClient

# client = SECClient()

# submissions = client.get_company_submissions(320193)  # Apple

# recent = submissions["filings"]["recent"]

# print("Fields available in recent:")
# print("-" * 40)

# for key in recent.keys():
#     print(key)

# ====================================================================
#                       TEST 2
# ====================================================================
# from app.infrastructure.document_sources.sec.sec_client import SECClient

# client = SECClient()

# # submissions = client.get_company_submissions(320193)

# # print("Top-level keys:")
# # print("-" * 40)

# # for key in submissions.keys():
# #     print(key)

# companies = {
#     "Apple": 320193,
#     "Microsoft": 789019,
#     "Tesla": 1318605,
#     "NVIDIA": 1045810,
#     "Amazon": 1018724,
#     "Alphabet": 1652044,
#     "Meta": 1326801,
# }

# for name, cik in companies.items():
#     submissions = client.get_company_submissions(cik)
#     print(f"{name:<12} -> {submissions['fiscalYearEnd']}")

# # print("\nRecent filings keys:")
# # print("-" * 40)
# # print(f"Fiscal Year End: {submissions['fiscalYearEnd']}")

# ====================================================================
#                       TEST 3
# ====================================================================
from app.infrastructure.document_sources.sec.sec_client import SECClient
from pprint import pprint

client = SECClient()

# Apple
submissions = client.get_company_submissions(320193)

recent = submissions["filings"]["recent"]

print(f"Fiscal Year End: {submissions['fiscalYearEnd']}")
print()

print(
    f"{'Idx':<4}"
    f"{'Form':<8}"
    f"{'Report Date':<15}"
    f"{'Filing Date':<15}"
    f"{'Primary Document'}"
)

print("-" * 90)

for i, (
    form,
    report_date,
    filing_date,
    primary_document,
) in enumerate(
    zip(
        recent["form"],
        recent["reportDate"],
        recent["filingDate"],
        recent["primaryDocument"],
    ),
    start=1,
):
    if form not in ("10-K", "10-Q"):
        continue

    print(
        f"{i:<4}"
        f"{form:<8}"
        f"{report_date:<15}"
        f"{filing_date:<15}"
        f"{primary_document}"
    )

pprint(submissions["filings"]["files"])   
print("#"*100) 
print(f"Filing.Keys: {submissions['filings'].keys()}")
# print(submissions["filings"].keys())



print("\n" + "=" * 100)
print("Company Facts")
print("=" * 100)

facts = client.get_company_facts(320193)

print("Top-level keys:")
print("-" * 40)

for key in facts.keys():
    print(key)