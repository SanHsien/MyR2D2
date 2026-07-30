# MyR2D2 🤖

### Your everyday astromech droid — a Claude skillset (zh-TW body, bilingual triggers)

**[繁體中文 (primary)](README.md) | English (this page)**

---

R2-D2 was never the protagonist, but every episode runs on him: smuggling out the Death Star plans, rolling across a desert to find Obi-Wan, quietly fixing the ship and managing power from the back of an X-wing.

That's MyR2D2's job description — 5 skills covering things that "won't kill you if skipped, but keep the whole workflow alive when done":

| Skill | One-liner | R2-D2 parallel |
|---|---|---|
| **save-all** | Before wrap-up/reboot: land everything that lives only in the conversation, and **verify** it hit disk | Plans stored in R2, escape pod away |
| **dropoff** | Write a task + full context into a handoff card for another session | Leia recording "Help me, Obi-Wan" |
| **pickup** | New session fetches the cards, reads in full, claims, starts | R2 finds Obi-Wan, plays the hologram |
| **token-optimizer** | Iron rules before multi-agent dispatch: model tiering, compressed reporting, stop after 3 failures | Power allocation — don't let shields drain the engines |
| **flight-to-calendar** | Booked flights → Google Calendar: timezone-correct, one leg per event, sunset seats | Navigation — the astromech's actual day job |

## One skill set, two language habits

The skill bodies are written in Traditional Chinese (single source of truth — no parallel translations to maintain). **Trigger phrases come in matched zh/en pairs** in each skill's description:

- 中文習慣:「要重開機了」「交接給 X」「有沒有交接給我的」
- English habit: "about to reboot", "hand this off to X", "anything handed off to me?"

Claude follows the zh-TW instructions and replies in whatever language you speak — English users lose nothing, and there's only ever one copy of each skill to maintain.

## Why this pack?

Claude sessions are **amnesiac**: close the conversation and everything not written to disk evaporates. The common theme here is fighting that amnesia:

- `save-all` covers "before closing" — externalize in-flight state, and **verify it actually landed** (silent write failures are real; never trust a literal "success").
- `dropoff` / `pickup` cover "after crossing over" — cards written so a stranger session can take over from the card alone.
- `token-optimizer` covers the other scarce resource: **usage quota** on subscription plans. One missing model spec in a fan-out and your quota evaporates.

All three were iterated out of real daily-driver usage, not theory.

## Install

### skills.sh (`npx skills`) — recommended, one command

[![skills.sh](https://skills.sh/b/tingyulu/MyR2D2)](https://skills.sh/tingyulu/MyR2D2)

```bash
npx skills add tingyulu/MyR2D2
```

[`npx skills`](https://github.com/vercel-labs/skills) supports Claude Code and many other agents (`gemini-cli`, `codex`, `cursor`, … — full list in the upstream README). This repo has verified the install layer for gemini-cli / codex (method & evidence in [docs/TEST_PLAN.md](docs/TEST_PLAN.md)); other targets are untested. It installs to the **project scope** `./.claude/skills/` by default; add `-g` for a global install. Use `--skill` to pick individual skills.

### Claude Code CLI — Plugin (deep integration)

```
/plugin marketplace add tingyulu/MyR2D2
/plugin install myr2d2@myr2d2
```

Skills land under the `myr2d2:` namespace (`/myr2d2:dropoff`, …) — structurally conflict-free with any same-name skills you already have, and centrally updatable via the marketplace.

### Claude Code CLI — manual copy

```bash
git clone https://github.com/tingyulu/MyR2D2.git
cp -rn MyR2D2/skills/* ~/.claude/skills/
```

⚠️ Note the `-n` (no-clobber): if `~/.claude/skills/` already has folders with these names, plain `cp -r` **overwrites them silently**. Diff first if you're updating an existing install.

### Cowork / claude.ai

Add the skill folders you want (`skills/<name>/`) to your Cowork project skills (or the project's `.claude/skills/`).

Then trigger with `/save-all`, `/dropoff`, `/pickup`, or natural language in either language.

## Compatibility matrix

| Skill | Claude Code CLI | Cowork / claude.ai | Gemini CLI | Codex CLI | ChatGPT (manual paste only) |
|---|---|---|---|---|---|
| save-all | ✅ | ✅ (token-count step auto-skips) | ✅ (same) | ✅ (drop the token-count step) | ⚠️ checklist only |
| dropoff / pickup | ✅ | ✅ | ✅ | ✅ | ❌ (no shared disk) |
| token-optimizer | ✅ | ✅ (rules-only, no tool deps) | ⚠️ principles port¹ | ⚠️ principles port¹ | ⚠️ principles port¹ |
| flight-to-calendar | ✅ (needs Calendar connector) | ✅ (needs Calendar connector) | ⚠️ bring your own Calendar MCP (untested) | ❌ no Calendar tool | ⚠️ needs an Action |

¹ The five iron rules port; swap model names for your vendor's tiers. §1's "advanced backstop" (settings.json / env) only works in Claude Code — skip it elsewhere.

- **Gemini CLI / Codex CLI**: install & discovery layers verified — including Gemini's trusted-folder gate (if skills don't show up, trust the project folder first); execution layer untested.
- **ChatGPT**: no CLI / no filesystem — manual paste is the only path (see adapters).
- Other `npx skills` targets (Cursor, Copilot, …): untested.

Porting guide for ChatGPT / Codex (preferred `npx skills` path, AGENTS.md fallback, three gotchas): **[adapters/openai/](adapters/openai/README.md)**.

## Per-skill dependencies

| Skill | Dependencies |
|---|---|
| save-all | None (the token-count step is Claude Code CLI-only and optional) |
| dropoff / pickup | None — cards are Markdown files under the project's `.claude/handoffs/` |
| token-optimizer | None (rules-only; Workflow-specific items need the Workflow tool; §1's advanced backstop is Claude Code CLI-only) |
| flight-to-calendar | **Google Calendar MCP connector** (hard dependency) |

dropoff/pickup default to the zero-dependency file-based version; if you run your own task system (CLI todo, Notion, Linear…), each SKILL.md includes a "plug in your own task system" section.

## Design principles

1. **Verification over declaration** — writes get read back, completion needs evidence, literal success messages are not trusted.
2. **Self-contained context** — handoff cards assume the reader knows nothing.
3. **Zero-dependency lowest common denominator** — file-based by default, external systems are the upgrade path.
4. **Quota is a shared resource** — thrift is the default for multi-agent dispatch; full power is an explicit switch.
5. **Single source of truth** — one copy per skill (zh-TW); language habits are handled by paired bilingual triggers, not parallel translations.

## Repo layout

```
MyR2D2/
├── .claude-plugin/                    ← plugin.json + marketplace.json (single plugin)
├── skills/                            ← 5 skills (zh-TW body, bilingual triggers)
│   ├── save-all/  ├── dropoff/  ├── pickup/
│   ├── token-optimizer/  └── flight-to-calendar/
├── adapters/openai/                   ← ChatGPT / Codex porting kit
├── README.md                          ← zh-TW (primary)
└── README.en.md                       ← this page
```

## Attribution

- `token-optimizer` is adapted from [kieiken/ultracode-token-optimization](https://github.com/kieiken/ultracode-token-optimization) (MIT), generalized for all-Claude environments.

## License

MIT — see [LICENSE](LICENSE).

*MyR2D2 is fan-tribute naming, unaffiliated with Lucasfilm / Disney; R2-D2 and Star Wars are trademarks of their respective owners.*
