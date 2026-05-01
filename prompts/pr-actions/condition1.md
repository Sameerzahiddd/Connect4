# Condition 1 — Is this a real, merged change to production?

---

## Path A: Continue

**Go down this path if** the pull request was successfully merged (not just closed or abandoned), the target branch was `main`, and the author was a human developer — not an automated bot like Dependabot or Renovate.

In short: a real engineer just shipped something to production. Keep going.

---

## Path B: Stop

**Go down this path if** the pull request was closed without merging, merged into a branch other than `main`, or opened by a bot.

In short: nothing meaningful shipped. Stop and do nothing.
