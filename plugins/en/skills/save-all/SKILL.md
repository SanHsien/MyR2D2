---
name: save-all
description: Pre-reboot / end-of-day "landing check". Run once in every open session to externalize everything that lives only in this conversation — write it to disk and VERIFY it landed — then report "safe to reboot / X items not yet synced". Triggers when the user says "save-all", "/save-all", "about to reboot", "shutting down", "wrapping up for today", "before restart". ⚠️ This skill only lands data and reports — it never reboots the machine.
---

# /save-all — landing check before you power down

Before rebooting (or just wrapping up), run this once in **every open conversation session**.

## Why this exists

- When a session closes, **its conversation context is gone**. Anything that lives only in the conversation — lessons learned, freshly-spawned todos, half-finished work state — evaporates.
- Landing = externalizing those into files on disk.
- And **writes can fail silently** (tools returning "success" while the file never changed is a real failure mode) → **after landing, always verify the write actually hit disk**. This is an iron rule of this skill, not an optional step.

> 🤖 R2-D2 moment: if the Death Star plans had lived only in Leia's head, the story ends
> when the Tantive IV is boarded. Stored in R2, ejected in the escape pod — data landed,
> story continues.

## Actions (do in order, report item by item)

### 0. Check the clock
Run `date` first — landing records need correct timestamps, not guessed ones.

### 1. Inventory this session's in-flight state

For each category ask: "will this survive the session closing? If not, land it":

- **① Lessons / decisions / surprising discoveries** → belongs in long-term memory (memory dir, project notes)
- **② Todos spawned during this session** → belongs in your task list
- **③ Things to hand to another project / future session** → needs a handoff card (→ `/handoff`)
- **④ System-level changes made** (installed/changed/disabled schedulers, automation scripts, config) → belongs in project docs
- **⑤ Narrative of half-finished work** → belongs in a HANDOFF / progress note

If the session is idle with nothing in flight → skip to step 5 and report "no in-flight state, safe to reboot". **Don't invent items.**

### 2. Land each item

- ①④⑤ → write into the corresponding notes / memory / doc files.
- ② → into your task system (or a project TODO file if you have none).
- ③ → run `/handoff` to write a handoff card (use the skill if installed; don't re-implement it here).

**Verify every write immediately**: `wc -l` for line count, `stat` for a just-now mtime, `grep` for the new content → confirm it truly landed. If it didn't, write again — **never trust a literal "success" message**.

### 3. Flush git (if this session touched a git-managed directory)

Even directories with auto-sync — the reboot may come before the next sync tick, so push manually:

```bash
git add -A && git commit -m "pre-reboot flush $(date +%m%d-%H%M)" && git push
```

(Glance at `git status` before committing — make sure nothing that shouldn't be in the repo got swept in.)

### 4. Count tokens spent by this save-all (Claude Code CLI only, optional)

> Cowork / claude.ai environments have no local transcript — skip this step entirely; nothing else depends on it.

Read the real `usage` from this session's transcript (do not self-estimate — models cannot reliably introspect their own usage):

```bash
tx=$(find ~/.claude/projects -name "${CLAUDE_CODE_SESSION_ID}.jsonl" 2>/dev/null | head -1)
[ -n "$tx" ] && python3 - "$tx" <<'PY'
import json,sys
i=o=cc=cr=n=0
for line in open(sys.argv[1]):
    try: u=json.loads(line).get('message',{}).get('usage')
    except: continue
    if not isinstance(u,dict): continue
    i+=u.get('input_tokens',0); o+=u.get('output_tokens',0)
    cc+=u.get('cache_creation_input_tokens',0); cr+=u.get('cache_read_input_tokens',0); n+=1
print(f"session total {n} turns: input={i:,} output={o:,} cache_creation={cc:,} cache_read={cr:,}")
PY
```

### 5. Report go / no-go

After re-verifying each item, give a clear signal:

- ✅ **Everything landed, no in-flight residue** → "Safe to reboot" + list what landed and into which file.
- ⚠️ **X items not yet synced** → list unlanded items and why, then: "recommend handling X before rebooting, or accept the risk (rebooting loses X)" — the user decides.

## Iron rules

- 🚫 **This skill never reboots the machine.** Landing + reporting only; the user presses the button.
- ✅ **Every landing gets verified on disk.**
- 🔁 **Run once per open session** — each session only knows its own in-flight state; don't try to land another session's from here.
- 📝 **Record as you go, report item by item** — no batch catch-up at the end.
