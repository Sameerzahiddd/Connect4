# GitHub Webhook Payload — Field Reference

Fields available in Lindy after a PR event fires. All paths are prefixed with the Lindy payload root.

---

## Event-Level Fields

| Field | Path | Example Value | Used For |
|---|---|---|---|
| Event type | `headers.x-github-event` | `"pull_request"` | Confirming source |
| Unique delivery ID | `headers.x-github-delivery` | `"27635e60-..."` | Deduplication |
| PR action | `body.action` | `"closed"` | Condition 1 filter |

---

## Pull Request Fields

| Field | Path | Example Value | Used For |
|---|---|---|---|
| Merged? | `body.pull_request.merged` | `true` | Condition 1 filter |
| PR number | `body.pull_request.number` | `1` | Reference / logging |
| PR title | `body.pull_request.title` | `"Add SSO for enterprise"` | Classification input |
| PR description | `body.pull_request.body` | `"This PR adds..."` | Classification input + Linear ID extraction |
| PR URL | `body.pull_request.html_url` | `"https://github.com/..."` | Logging / linking |
| State | `body.pull_request.state` | `"closed"` | Condition 1 filter |
| Draft? | `body.pull_request.draft` | `false` | Filter out drafts |
| Merged at | `body.pull_request.merged_at` | `"2026-04-27T23:59:..."` | Timestamp for Sheet row |
| Merged by | `body.pull_request.merged_by.login` | `"Sameerzahiddd"` | Logging |
| Labels | `body.pull_request.labels` | `[]` | Classification hint |
| Commits | `body.pull_request.commits` | `1` | Context |
| Files changed | `body.pull_request.changed_files` | `1` | Classification hint |
| Lines added | `body.pull_request.additions` | `1` | Context |
| Lines deleted | `body.pull_request.deletions` | `1` | Context |

---

## Branch Fields

| Field | Path | Example Value | Used For |
|---|---|---|---|
| Source branch name | `body.pull_request.head.ref` | `"sameer/lin-123-add-sso"` | **Linear ID extraction** |
| Source commit SHA | `body.pull_request.head.sha` | `"c362c95..."` | Logging |
| Target branch | `body.pull_request.base.ref` | `"main"` | Condition 1 filter |

---

## Author Fields

| Field | Path | Example Value | Used For |
|---|---|---|---|
| Author username | `body.pull_request.user.login` | `"Sameerzahiddd"` | Logging |
| Author type | `body.pull_request.user.type` | `"User"` | Bot filter (must be "User") |
| Sender username | `body.sender.login` | `"Sameerzahiddd"` | Logging |
| Sender type | `body.sender.type` | `"User"` | Bot filter (must be "User") |

---

## Repository Fields

| Field | Path | Example Value | Used For |
|---|---|---|---|
| Repo name | `body.repository.name` | `"Connect4"` | Context |
| Full name | `body.repository.full_name` | `"Sameerzahiddd/Connect4"` | Logging |
| Default branch | `body.repository.default_branch` | `"main"` | Dynamic main check |
| Repo URL | `body.repository.html_url` | `"https://github.com/..."` | Linking |

---

## Fields Critical to the Pipeline

These are the ones every downstream step depends on:

1. `body.action` → Condition 1
2. `body.pull_request.merged` → Condition 1
3. `body.pull_request.base.ref` → Condition 1
4. `body.pull_request.user.type` → Bot filter
5. `body.pull_request.head.ref` → Linear ID extraction (regex `LIN-\d+`)
6. `body.pull_request.body` → Linear ID extraction (fallback) + classification input
7. `body.pull_request.title` → Classification input
8. `body.pull_request.merged_at` → Timestamp for Google Sheet row
