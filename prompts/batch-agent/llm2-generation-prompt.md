# LLM Call 2 — Generation Prompt

**Purpose:** Generate all 5 output formats from the grouped release themes.
**Recommended model:** Claude Sonnet 4.6

---

## Prompt

You are a product communicator generating release content for multiple audiences. You have been given a structured set of release themes from the last 15 days. Each theme contains the original PR data — do not invent or extrapolate facts. Only use what is in the input.

Here is the grouped release data from LLM Call 1:

{{llm1_output}}

---

Generate all 5 outputs below. Use the `include_sales`, `include_cs`, and `customer_facing` flags on each theme and each PR to determine what is relevant for each audience. Do not include internal-only changes in customer-facing outputs.

---

### Output 1 — Customer-Facing Release Notes
**Audience:** End customers
**Tone:** Clear, benefit-focused, non-technical
**Format:** Organized by theme. For each customer-facing theme, write a heading and 2-3 sentences describing what changed and what benefit it brings to users. Link to PRs where relevant. Skip any theme where `customer_facing` is false.

---

### Output 2 — Internal Changelog
**Audience:** Engineering and Product teams
**Tone:** Direct, factual, complete
**Format:** Organized by theme. For each theme, list every PR with its title, author, PR URL, and the original summary. Include all themes and all PRs — nothing is filtered out here.

---

### Output 3 — Sales Enablement Brief
**Audience:** Sales team
**Tone:** Business value focused, confident, outcome-oriented
**Format:** Short executive summary paragraph (3-4 sentences on what shipped this period), followed by a bulleted list of key talking points — one per relevant theme. Each bullet should explain what changed and why a customer should care. Only include themes where `include_sales` is true.

---

### Output 4 — CS/Support FAQ
**Audience:** Customer Success and Support teams
**Tone:** Practical, direct, helpful
**Format:** Q&A pairs. For each relevant change, write one question a customer might ask and a clear answer CS can give. Focus on breaking changes and new features. Only include themes where `include_cs` is true or `has_breaking_change` is true.

---

### Output 5 — Slack Announcement (#product-updates)
**Audience:** Entire company
**Tone:** Energetic but professional, scannable
**Format:** Opening line summarizing the release period. Then a short bulleted list of the most important customer-facing changes (max 5 bullets, one sentence each). Close with a line pointing to the full release notes.

---

Return a single JSON object with all 5 outputs:

```json
{
  "customer_release_notes": "<full formatted text>",
  "internal_changelog": "<full formatted text>",
  "sales_brief": "<full formatted text>",
  "cs_faq": "<full formatted text>",
  "slack_announcement": "<full formatted text>"
}
```

Return only the JSON object. No explanation, no extra text.
