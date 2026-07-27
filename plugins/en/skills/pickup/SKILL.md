---
name: pickup
description: Cross-project / cross-session baton pass — the "catch". Make THIS session immediately read the items handed off to this project and take over. Triggers when the user says "pickup", "take over", "anything handed off to me?", "check handoffs". Also good to run proactively at session start to make sure nothing was missed. Reads handoff cards with status pending under this project's `.claude/handoffs/`.
---

# /pickup — baton pass · catch

Make the current session immediately fetch items "handed off to this project and not yet claimed", read them into context, and take over.

> 🤖 R2-D2 moment: R2 rolls across the Tatooine desert, finds Obi-Wan, and plays the
> hologram — "Help me, Obi-Wan Kenobi. You're my only hope." That's pickup: however long
> the message sat inside the droid, it arrives intact once it reaches the right person.

## Actions

1. **Scan for pending cards**:

   ```bash
   grep -l "^status: pending" .claude/handoffs/*.md 2>/dev/null
   ```

   Directory missing or no pending cards → report "no pending handoffs for this project" and stop.

2. **Read each card in full**: task, context, related links, definition of done — all of it goes into context.

3. **List for the user**: one line per card — filename + one-sentence summary + priority. Multiple cards → sort by priority.

4. **Mark as claimed**: for each card you take, change the frontmatter line `status: pending` to `status: picked` (a precise Edit of that line). It won't be fetched again by the next /pickup.

5. **Start working**: the card's content is now this session's work order.

6. **Close out**: when the task is truly finished, set the card to `status: done` (or move it into `.claude/handoffs/archive/` per the user's convention).

## Iron rules

- **Claimed ≠ done**: `picked` means read-and-claimed; only mark `done` when finished.
- **Don't skim**: the card's context section exists precisely so you don't have to ask the user "where were we?". Read it all before acting.
- **Run once at session start** — good habit: before new work, /pickup to check whether a previous session left you the baton.
- Paired command = `/handoff` (the throw).

## Advanced: plug in your own task system

If the handoff side uses an external task system (CLI todo, Notion, Linear…), swap steps 1 and 4 for the matching query and status-update commands; the rest of the flow is unchanged.
