# Condition 2 — Is there a Linear ticket linked to this PR?

---

## Path A: Linear ID found — fetch ticket details

**Go down this path if** a Linear ticket ID (pattern: `LIN-` followed by digits) is found using the following priority order:

1. **Check branch name first** (`body.pull_request.head.ref`). If a Linear ID is found here, use it and stop — this is the authoritative source since Linear auto-generates branch names from tickets.
2. **Only if the branch name has no Linear ID**, check the PR description (`body.pull_request.body`) — but only extract an ID if it appears immediately after the words "Fixes", "Closes", or "Resolves" (e.g., `Fixes LIN-123`). Ignore any other Linear references in the body as they may refer to unrelated tickets.

---

## Path B: No Linear ID — skip Linear lookup

**Go down this path if** neither the branch name nor the PR description contains any reference to a Linear ticket ID. We proceed with only the PR data available and skip the Linear API call entirely.
