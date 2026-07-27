---
name: handoff
description: Cross-project / cross-session baton pass — the "throw". Hand a task with full context to a Claude session in another project (or a future session of this one). Triggers when the user says "hand this off to X", "handoff to project Y", "pass this to the next session". Output = a handoff card (Markdown file) in the target project's `.claude/handoffs/`, picked up on the other side with /pickup.
---

# /handoff — baton pass · throw

Hand a task **reliably** to another Claude session (a different project, or the next session of this one).

The core problem: the receiving session cannot read this conversation's context. Verbal instructions get lost, chat history gets cut — so the handoff card must be **a file on disk**, written so completely that a stranger session can take over from the card alone.

> 🤖 R2-D2 moment: Leia stores the Death Star plans and her plea inside R2's memory —
> that's a handoff. The message doesn't rely on Leia delivering it in person; it relies on
> the droid that will roll across a desert to find Obi-Wan.

## Handoff card format

One card = one Markdown file, in the **target project's** `.claude/handoffs/` directory:

```
<target project root>/.claude/handoffs/YYYYMMDD-HHMM-<short-slug>.md
```

```markdown
---
status: pending          # pending → picked → done
from: <source project or session description>
to: <target project>
created: YYYY-MM-DD HH:MM
priority: high | normal | low
---

# <the task in one sentence>

## What to do
<concrete, actionable task description>

## Context (readable by a session that knows nothing)
<why this matters, what's been done so far, decision background>

## Related files / links
- <one path or URL per line>

## Definition of done
<verifiable conditions — evidence, not vibes>
```

## Usage

`/handoff <target project path or name> <task>`

- No target given → ask the user.
- Target is "a future session of this same project" → write into this project's own `.claude/handoffs/`.

## Actions

1. **Create the directory** (if missing): `mkdir -p <target>/.claude/handoffs`
2. **Write the card** per the format above. "Context" and "Definition of done" are the card's soul — a title-only handoff card is no handoff at all.
3. **Verify it landed**: `cat` the file back and confirm the content is complete (writes can fail silently; never trust a literal success message).
4. **Report**: card path + one-line summary + remind the user "the receiving session runs `/pickup` to take over".

## Iron rules

- **One card, one task.** Two tasks = two cards. Don't bundle.
- **Self-contained context**: assume the reader session knows nothing about your conversation. All background, links, and paths go on the card.
- **For time-sensitive items**, besides writing the card, also ping the user through whatever immediate channel you have (notification, message) — cards are a pull model; the other side won't read until it starts work.
- Paired command = `/pickup` (the catch).

## Advanced: plug in your own task system

If you run a cross-project task manager (CLI todo, Notion, Linear, GitHub Issues…), replace "write the card" with "create a type=handoff task in your system", and swap the query on the `/pickup` side to match. The file-based version is the zero-dependency lowest common denominator, not the ceiling.
