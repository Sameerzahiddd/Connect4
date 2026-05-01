# Sheet Append Prompts — all_prs

Each prompt goes into the "Prompt AI" field for its column in Lindy's Append Row step.
For cells pulling from the LLM classification step, link that step's output at the end of the prompt.

---

### `date`
```
Extract the date when this pull request was merged. Use the field body.pull_request.merged_at from the webhook payload. Format it as: YYYY-MM-DD with no time, no timezone, nothing else. Example: 2026-04-28. Return only the date in this exact format.
```
> Link: webhook output

---

### `pr_number`
```
Extract the pull request number from the webhook payload. Use the field body.pull_request.number. Return only the number as a plain integer, nothing else.
```
> Link: webhook output

---

### `pr_title`
```
Extract the pull request title from the webhook payload. Use the field body.pull_request.title. Return the title exactly as written, nothing else.
```
> Link: webhook output

---

### `pr_url`
```
Extract the pull request URL from the webhook payload. Use the field body.pull_request.html_url. Return only the URL, nothing else.
```
> Link: webhook output

---

### `linear_id`
```
Return the Linear ticket ID that was extracted earlier in this workflow. It will be in the format LIN-XXX (e.g. LIN-123). If no Linear ID was found, return the word: none
```
> Link: set variable output (linear_id)

---

### `author`
```
Extract the GitHub username of the person who opened this pull request. Use the field body.pull_request.user.login from the webhook payload. Return only the username, nothing else.
```
> Link: webhook output

---

### `summary`
```
Extract the value of the "summary" field from the LLM classification output. It should be 3-4 sentences in plain English. Return it exactly as written, no modifications.
```
> Link: LLM classification output

---

### `change_type`
```
Extract the value of the "change_type" field from the LLM classification output. Return only the exact value — it must be one of: new_feature, improvement, bug_fix, breaking_change, internal, feature_flag. No other text.
```
> Link: LLM classification output

---

### `customer_impact`
```
Extract the value of the "customer_impact" field from the LLM classification output. Return only the exact value — it must be one of: customer_facing, internal_only, api_change. No other text.
```
> Link: LLM classification output

---

### `include_sales`
```
Extract the value of the "include_sales" field from the LLM classification output. Return only: yes or no. No other text, no punctuation.
```
> Link: LLM classification output

---

### `include_cs`
```
Extract the value of the "include_cs" field from the LLM classification output. Return only: yes or no. No other text, no punctuation.
```
> Link: LLM classification output
