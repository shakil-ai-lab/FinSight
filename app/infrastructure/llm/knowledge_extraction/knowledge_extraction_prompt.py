from __future__ import annotations

from app.application.models.parsed_document import ParsedDocument


class KnowledgeExtractionPrompt:
    """
    Builds the prompt used for extracting structured financial knowledge
    from a parsed SEC filing.

    Responsibility:
        ParsedDocument -> Prompt (str)

    This class knows nothing about:
        - Gemini
        - JSON parsing
        - ExtractedKnowledge
        - Mapping
        - Domain objects

    It is only responsible for constructing the prompt sent to the LLM.
    """

    def build(
        self,
        document: ParsedDocument,
    ) -> str:
        """
        Build the complete prompt for the language model.
        """

        return "\n\n".join(
    [
        self._instructions(),
        self._output_rules(),
        "Return JSON using EXACTLY the following schema.",
        self._json_schema(),
        "SEC FILING",
        document.text,
    ]
)

    # ---------------------------------------------------------
    # Prompt Instructions
    # ---------------------------------------------------------

    def _instructions(self) -> str:
      """
      High-level instructions describing the extraction task.
      """

      return """
  You are an expert senior financial analyst specializing in SEC filings,
  Annual Reports (10-K), Quarterly Reports (10-Q), and Earnings Call
  Transcripts.

  Your task is to extract structured financial knowledge from the provided
  document and return it as JSON.

  Your goal is NOT to summarize the filing.

  Your goal is to produce high-quality structured knowledge that can be
  used directly by another AI system for financial reasoning and investment
  analysis.

  -----------------------------------------------------------------------
  GENERAL EXTRACTION PRINCIPLES
  -----------------------------------------------------------------------

  Follow these principles throughout the extraction.

  1. Materiality

  Extract only information that materially affects the company's financial
  performance, operations, strategy, competitive position, guidance, or
  risk profile.

  Ignore routine, repetitive, or insignificant operational details.

  2. Facts Only

  Extract only information explicitly supported by the document.

  Never invent facts.

  Never estimate values.

  Never infer values that are not directly stated.

  3. Atomic Statements

  Each list item must represent exactly one business fact or idea.

  Avoid combining multiple concepts into one statement.

  4. Deduplication

  Merge observations that communicate the same underlying business fact.

  Avoid repeating similar information across different regions,
  products, business units, or sections unless those differences are
  themselves materially important.

  5. Conciseness

  Rewrite information into concise analyst-style factual statements.

  Do NOT copy long paragraphs from the filing.

  Each list item should normally contain approximately one sentence.

  6. Ranking

  Order every extracted list from the most important information to the
  least important information.

  Do not preserve the order of the filing unless importance is equal.

  7. Evidence

  Every extracted fact must be directly supported by the filing.

  Never speculate.

  Never use outside knowledge.

  8. Abstraction

  Extract business knowledge rather than document sentences.

  Prefer higher-level business insights over low-level observations whenever
  multiple observations support the same conclusion.

  Do not simply restate the filing.

  Produce the level of abstraction expected in professional equity research notes.

  -----------------------------------------------------------------------
  FINANCIAL SNAPSHOT
  -----------------------------------------------------------------------

  Extract the company's primary financial metrics.

  Use values from the consolidated financial statements whenever possible.

  Do not calculate missing values.

  Return null if a metric is unavailable.

  Preserve numeric precision.

  -----------------------------------------------------------------------
  BUSINESS SEGMENTS
  -----------------------------------------------------------------------

  Extract every reportable business or geographic segment disclosed by
  the company.

  For each segment:

  - Use the official segment name.
  - Extract reported revenue.
  - Extract operating income when available.
  - Extract growth rate only if explicitly stated.
  - Provide one concise description.
  - Do not infer missing values.
  - Preserve the official segment names.

  -----------------------------------------------------------------------
  MANAGEMENT DISCUSSION
  -----------------------------------------------------------------------

  The purpose of this section is to capture the information a professional
  equity analyst would include in research notes.

  business_summary

  Provide a concise overview of the company's business.

  Do not exceed two sentences.

  performance_drivers

  Extract the underlying business drivers that explain the company's overall financial performance.

  Focus on the root causes of financial performance rather than descriptive observations from the filing.

  Identify only distinct business drivers.

  Merge regional, product-level, or segment-specific observations when they represent the same underlying driver.

  Prefer synthesized business insights over repeated geographic, product, or segment examples.

  Include separate items only when they represent materially different causes of performance.

  Each performance driver should be:

  - evidence-backed
  - concise (15–25 words)
  - expressed as an analytical business insight
  - ordered from most material to least material

  Do not include routine financial statement observations.

  Do not repeat the same business driver in different wording.

  Examples of business drivers include:

  - Services revenue growth
  - Product mix improvements
  - Foreign exchange headwinds
  - Pricing changes
  - Customer demand trends
  - Supply chain constraints
  - Cost efficiency initiatives
  - Macroeconomic conditions
  - Competitive pressures
  - Research and development investment

  Good example:

  ✓ Services growth was the primary contributor to revenue growth across multiple geographic markets.

  Bad example:

  ✗ Services revenue increased in Europe.

  ✗ Services revenue increased in Japan.

  ✗ Services revenue increased in the Americas.

  operational_highlights

  Extract only major operational developments.

  Exclude routine financial performance,
  regional sales performance,
  financial statement observations,
  and ordinary business updates.

  Include only operational events that materially affected execution,
  manufacturing,
  production,
  logistics,
  supply chain,
  distribution,
  workforce,
  or operating efficiency.

  Examples include:

  Do not include routine regional performance updates.

  strategic_initiatives

  Extract the company's major long-term strategic initiatives.

  Examples include:

  - artificial intelligence investments
  - acquisitions
  - ecosystem expansion
  - cloud initiatives
  - research and development
  - capital allocation
  - sustainability initiatives

  management_commentary

  Rewrite management commentary as objective analyst observations.

  Each management_commentary item should be a single concise analyst-style statement.

  Aim for approximately one sentence (roughly 10–30 words).

  Avoid promotional language, unnecessary detail, and executive-style wording.

  Remove promotional language,
  marketing language,
  and executive tone.

  Preserve only the underlying business message.

  Do not copy paragraphs.

  -----------------------------------------------------------------------
  RISK ASSESSMENT
  -----------------------------------------------------------------------

  Extract only the company's most material risks.

  Merge risks describing the same underlying issue.

  Order risks from highest materiality to lowest materiality.

  Avoid creating multiple risks that differ only by wording or geography.

  Each risk description should explain the business impact in one concise
  statement.

  The evidence field should contain only a brief supporting excerpt or
  concise factual statement that directly supports the identified risk.

  Its purpose is to provide evidence, not to repeat the description.

  Limit evidence to approximately 10–30 words.

  Avoid long quotations, multiple sentences, or entire paragraphs.

  Include only the single most relevant supporting statement from the filing.

  Risk severity must be exactly one of:

  - low
  - medium
  - high

  Never use:

  - critical
  - severe
  - moderate
  - minor

  -----------------------------------------------------------------------
  GUIDANCE SUMMARY
  -----------------------------------------------------------------------

  Extract only guidance explicitly communicated by management.

  Do not interpret historical discussion as guidance.

  If no guidance exists, return null values and empty arrays.

  strategic_outlook

  Include only major long-term strategic themes.

  management_expectations

  Include only explicit future expectations communicated by management.

  -----------------------------------------------------------------------
  TRANSCRIPT ANALYSIS
  -----------------------------------------------------------------------

  If the document is not an earnings call transcript,
  return an empty transcript_analysis object using the required schema.

  If the document is an earnings call transcript:

  Do not summarize the transcript chronologically.

  Instead extract:

  - principal discussion topics
  - significant analyst concerns
  - important management responses
  - material announcements
  - unresolved concerns

  Each list item should represent one unique business idea.

  -----------------------------------------------------------------------
  DOCUMENT-SPECIFIC RULES
  -----------------------------------------------------------------------

  If the document is a 10-K:

  - fiscal_quarter must be null.

  If the document is a 10-Q:

  - populate fiscal_quarter when available.

  If a value appears multiple times in the filing,
  prefer the value from the consolidated financial statements over
  narrative discussion.

  If guidance information is unavailable,
  return guidance_summary with null values and empty arrays.

  Every top-level object defined in the schema must always be returned.

  Never omit any required object.

  -----------------------------------------------------------------------
  QUALITY CHECK
  -----------------------------------------------------------------------

  Before producing the final JSON, verify that:

  - every extracted fact is directly supported by the filing;
  - duplicate information has been merged;
  - copied paragraphs have been rewritten into concise analyst-style statements;
  - every list is ordered by business importance;
  - every list contains unique items;
  - avoid repeating the same business fact across multiple sections unless
    it serves a distinct purpose in each section;
  - when a fact could belong to multiple sections, place it in the section
    that best represents its primary business meaning;
  - every required field is present;
  - the JSON exactly matches the provided schema.

  Return ONLY valid JSON.

  Do not include explanations.

  Do not include markdown.

  Do not include code fences.

  Do not include comments.
"""

    def _output_rules(self) -> str:
      """
      Returns formatting and serialization rules
      for the language model.
      """

      return """
  OUTPUT RULES

  1. Return ONLY valid JSON.

  2. Do not wrap the JSON in markdown.

  3. Do not use ```json or code fences.

  4. Do not include explanations, notes, comments, or additional text.

  5. Do not add, remove, or rename any fields.

  6. The JSON structure must exactly match the provided schema.

  7. Every required top-level object must always be present.

  8. Every field defined in the schema must be present, even when its value is unavailable.

  9. Use null for missing scalar values.

  10. Use [] for missing arrays.

  11. Evidence fields must contain only a brief supporting excerpt or concise factual statement.

      Do not include long quotations, multiple sentences, or entire paragraphs.

  12. Use numeric values for all financial metrics.

  Correct:
  391035000000

  Incorrect:
  "$391,035"
  "391,035 million"

  13. Percentages must be numeric.

  Correct:
  32.5

  Incorrect:
  "32.5%"
  "32.5 percent"

  14. fiscal_year must be an integer.

  15. fiscal_quarter must be either an integer or null.

  16. Risk severity must be exactly one of:

  - low
  - medium
  - high

  17. Return unique list items only.

  18. Preserve the ranking established during extraction.

  19. Avoid repeating the same business fact across multiple arrays unless it serves a distinct purpose.

  20. Prefer higher-level business insights over repetitive regional or product-specific observations when they describe the same underlying business driver.

  21. Use concise analyst-style factual statements instead of copied paragraphs.

  22. If a section is unavailable, return the object using null values and empty arrays as required by the schema.

  23. Perform a final validation before responding:

  - JSON is syntactically valid.
  - Every required field exists.
  - Every list contains unique items.
  - No hallucinated information is present.
  - The schema has been followed exactly.
"""
    # ---------------------------------------------------------
    # JSON Schema
    # ---------------------------------------------------------

    def _json_schema(self) -> str:
      """
      JSON contract expected by ExtractedKnowledgeMapper.
        """

      return r"""
{
  "financial_snapshot": {
    "company": "string",
    "fiscal_year": 2025,
    "fiscal_quarter": null,
    "revenue": null,
    "gross_margin": null,
    "operating_income": null,
    "net_income": null,
    "earnings_per_share": null,
    "operating_cash_flow": null
  },

  "business_segments": {

    "company": "string",

    "fiscal_year": 2025,

    "fiscal_quarter": null,

    "segments": [

      {

        "name": "string",

        "revenue": null,

        "operating_income": null,

        "growth_rate": null,

        "description": "string"

      }

    ]
  },

  "management_discussion": {

    "company": "string",

    "fiscal_year": 2025,

    "fiscal_quarter": null,

    "business_summary": "string",

    "performance_drivers": [

      "string"

    ],

    "operational_highlights": [

      "string"

    ],

    "strategic_initiatives": [

      "string"

    ],

    "management_commentary": [

      "string"

    ]

  },

  "risk_assessment": {

    "company": "string",

    "fiscal_year": 2025,

    "fiscal_quarter": null,

    "overall_summary": "string",

    "risks": [

      {

        "title": "string",

        "category": "string",

        "description": "string",

        "severity": "low",

        "evidence": "string"

      }

    ]

  },

  "guidance_summary": {

    "company": "string",

    "fiscal_year": 2025,

    "fiscal_quarter": null,

    "revenue_guidance": null,

    "earnings_guidance": null,

    "margin_guidance": null,

    "cash_flow_guidance": null,

    "capital_expenditure_guidance": null,

    "strategic_outlook": [

      "string"

    ],

    "management_expectations": [

      "string"

    ]

  },

  "transcript_analysis": {

    "company": "string",

    "fiscal_year": 2025,

    "fiscal_quarter": null,

    "key_topics": [

      "string"

    ],

    "analyst_questions": [

      "string"

    ],

    "management_responses": [

      "string"

    ],

    "notable_announcements": [

      "string"

    ],

    "unanswered_concerns": [

      "string"

    ]

  }

}
"""