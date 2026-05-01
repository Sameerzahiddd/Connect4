# Condition 3 — What type of change was this, and who needs to know right now?

---

## Path A: Breaking Change

**Go down this path if** the `change_type` extracted from the LLM output is `breaking_change`. This means existing behavior has changed in a way that could disrupt current users or integrations, and CS and Product must be alerted immediately — this cannot wait for a batch report.

---

## Path B: Customer-Facing New Feature

**Go down this path if** the `change_type` is `new_feature` AND `customer_impact` is `customer_facing`. A brand new capability is now live for end customers and the product team should know so they can follow up with release notes and announcements.

---

## Path C: Feature Behind a Flag

**Go down this path if** the `change_type` is `feature_flag`. The code has shipped to production but is not yet visible to customers. Engineering needs a reminder that a flag is now live so it does not get forgotten and left dormant indefinitely.

---

## Path D: Customer-Facing Bug Fix

**Go down this path if** the `change_type` is `bug_fix` AND `customer_impact` is `customer_facing`. Something that was broken for customers is now fixed. CS should be informed immediately so they can proactively update any affected customers without waiting for the next batch report.

---

## Path E: Internal Change

**Go down this path if** the `change_type` is `internal` or `improvement` AND `customer_impact` is `internal_only`. Nothing customer-facing changed. The row has been logged. No immediate action needed — stop here.
