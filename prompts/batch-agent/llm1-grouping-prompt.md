# LLM Call 1 — Grouping Prompt

**Purpose:** Group the raw PR rows from the last 15 days into coherent release themes before generating the 5 output formats.
**Recommended model:** Claude Sonnet 4.6

---

## Prompt

You are organizing a list of pull requests into logical groups. Your job is purely structural — group related changes under a theme title. Do not rewrite, paraphrase, or summarize any of the PR content. Every word in the `summary` fields must be passed through exactly as it appears in the input.

Here is the raw data from the recent changes:

{{recent_sheet_output}}

---

Each row contains: date, pr_number, pr_title, pr_url, linear_id, author, summary, change_type, customer_impact, include_sales, include_cs.

Follow these steps:

**Step 1 — Identify themes**
Group the remaining rows into 2-5 release themes. A theme is a logical grouping of related changes — for example, "Authentication & Security", "Performance Improvements", or "Billing & Invoicing". Do not force unrelated changes together. If a change stands alone, it can be its own theme.

**Step 2 — Classify each theme**
For each theme, determine:
- Whether it contains any breaking changes
- Whether it is customer-facing
- Whether it should be included in the sales brief
- Whether it should be included in the CS FAQ

**Step 3 — Return structured JSON**

```json
{
  "period": "<start date> to <end date>",
  "total_changes": <number of PRs included>,
  "themes": [
    {
      "theme_title": "<short, plain English theme name>",
      "has_breaking_change": true or false,
      "customer_facing": true or false,
      "include_sales": true or false,
      "include_cs": true or false,
      "changes": [
        {
          "date": "<date from the row>",
          "pr_number": "<pr_number from the row>",
          "pr_title": "<pr_title from the row>",
          "pr_url": "<pr_url from the row>",
          "linear_id": "<linear_id from the row>",
          "author": "<author from the row>",
          "summary": "<summary from the row — copy exactly, word for word>",
          "change_type": "<change_type from the row>",
          "customer_impact": "<customer_impact from the row>",
          "include_sales": "<include_sales from the row>",
          "include_cs": "<include_cs from the row>"
        }
      ]
    }
  ]
}
```

Return only the JSON object. No explanation, no extra text.
