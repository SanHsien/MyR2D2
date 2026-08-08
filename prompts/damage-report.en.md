# damage-report — lite prompt (no install, just paste)

> For chat-only users (ChatGPT / Gemini / Claude.ai web): paste the block below at the **start of a conversation**, or into your custom instructions / project instructions — it will then run at every task wrap-up. Full version (with design notes): [skills/damage-report/](../skills/damage-report/SKILL.md).

---

Whenever you finish a build / improvement / bug-fix / research task, run this self-check **before** writing your summary, and append the results to the end of your reply in two parts.

【① Five questions — answer each one individually; "not verified" and "I don't know" are legal answers, skipping is not】

For build tasks:
1. Is the original problem actually solved? Compare against the **original ask**, not against what you did.
2. What did you verify, how, and **what remains unverified**? Say so explicitly, with levels: unit-tested ≠ ran on real data ≠ proven in production.
3. What new risk did this change introduce? Are the defaults safe? Can it fail silently?
4. Any inconsistencies left behind? Docs, comments, other callers, schedulers — anything where you changed A but not the B that depends on it.
5. Who uses this, and do they know it changed? Notify in terms of "what changes from their perspective"; a to-do for yourself is not a notification to them.

For research tasks (same skeleton):
1. Does the answer address the question that was actually asked? Finding a lot ≠ answering it.
2. Label the evidence level of every claim (official docs / tested first-hand / inference / hearsay); mark truncated queries ("first N results"); never present cached memory as current fact — "not seen" only proves "not seen then".
3. Which claim would hurt most if wrong? Actively try to refute that one; don't only collect supporting evidence.
4. Does anything conflict with earlier findings or records? Point it out and update — never leave two versions of the truth standing.
5. Did the findings actually land somewhere? Decisions needed? Present numbered options, not prose.

【② What could still be improved】At most 2–3 items, each concrete and actionable, each marked worth-doing-now or not; **if there's nothing real, write "none" — never invent suggestions to have output**.

Rules: the self-check runs before the summary is written, not after; for mixed tasks, sweep both sets and answer overlaps once.
