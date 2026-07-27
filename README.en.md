# MyR2D2 🤖

### Your everyday astromech droid — a bilingual skillset for Claude (zh-TW primary)

**[繁體中文 (primary)](README.md) | English (this page)**

---

R2-D2 was never the protagonist, but every episode runs on him: smuggling out the Death Star plans, rolling across a desert to find Obi-Wan, quietly fixing the ship and managing power from the back of an X-wing.

That's MyR2D2's job description — 5 skills, one set each in Traditional Chinese and English, all covering things that "won't kill you if skipped, but keep the whole workflow alive when done":

| Skill | One-liner | R2-D2 parallel |
|---|---|---|
| **save-all** | Before wrap-up/reboot: land everything that lives only in the conversation, and **verify** it hit disk | Plans stored in R2, escape pod away |
| **handoff** | Write a task + full context into a handoff card for another session | Leia recording "Help me, Obi-Wan" |
| **pickup** | New session fetches the cards, reads in full, claims, starts | R2 finds Obi-Wan, plays the hologram |
| **token-optimizer** | Iron rules before multi-agent dispatch: model tiering, compressed reporting, stop after 3 failures | Power allocation — don't let shields drain the engines |
| **flight-to-calendar** | Booked flights → Google Calendar: timezone-correct, one leg per event, sunset seats | Navigation — the astromech's actual day job |

## Why this pack?

Claude sessions are **amnesiac**: close the conversation and everything not written to disk evaporates. The common theme here is fighting that amnesia:

- `save-all` covers "before closing" — externalize in-flight state, and **verify it actually landed** (silent write failures are real; never trust a literal "success").
- `handoff` / `pickup` cover "after crossing over" — cards written so a stranger session can take over from the card alone.
- `token-optimizer` covers the other scarce resource: **usage quota** on subscription plans. One missing model spec in a fan-out and your quota evaporates.

All three were iterated out of real daily-driver usage, not theory.

## Install

**Pick ONE language edition** (identical skill names; installing both causes collisions):

### Claude Code CLI — Plugin (recommended)

```
/plugin marketplace add tingyulu/MyR2D2
/plugin install myr2d2-en@myr2d2        # English edition
/plugin install myr2d2-zh-tw@myr2d2     # Traditional Chinese edition
```

### Claude Code CLI — manual copy

```bash
git clone https://github.com/tingyulu/MyR2D2.git
cp -r MyR2D2/plugins/en/skills/* ~/.claude/skills/   # English (swap path for zh-tw)
```

### Cowork / claude.ai

Add the skill folders you want (`plugins/en/skills/<name>/`) to your Cowork project skills (or the project's `.claude/skills/`). The skill content is environment-agnostic — see the compatibility matrix.

Then trigger with `/save-all`, `/handoff`, `/pickup`, or natural language ("about to reboot", "anything handed off to me?").

## Compatibility matrix

| Skill | Claude Code CLI | Cowork / claude.ai | Codex / ChatGPT |
|---|---|---|---|
| save-all | ✅ | ✅ (token-count step auto-skips) | ✅ Codex / ⚠️ ChatGPT as checklist only |
| handoff / pickup | ✅ | ✅ | ✅ Codex / ❌ ChatGPT (no shared disk) |
| token-optimizer | ✅ | ✅ (rules-only, no tool deps) | ⚠️ principles port; swap model names |
| flight-to-calendar | ✅ (needs Calendar connector) | ✅ (needs Calendar connector) | ❌ Codex / ⚠️ ChatGPT needs an Action |

Porting guide for ChatGPT / Codex (AGENTS.md merge, routing line, three gotchas): **[adapters/openai/](adapters/openai/README.md)**.

## Per-skill dependencies

| Skill | Dependencies |
|---|---|
| save-all | None (the token-count step is Claude Code CLI-only and optional) |
| handoff / pickup | None — cards are Markdown files under the project's `.claude/handoffs/` |
| token-optimizer | None (rules-only; Workflow-specific items need an environment with the Workflow tool) |
| flight-to-calendar | **Google Calendar MCP connector** (hard dependency) |

handoff/pickup default to the zero-dependency file-based version; if you run your own task system (CLI todo, Notion, Linear…), each SKILL.md includes a "plug in your own task system" section.

## Design principles

1. **Verification over declaration** — writes get read back, completion needs evidence, literal success messages are not trusted.
2. **Self-contained context** — handoff cards assume the reader knows nothing.
3. **Zero-dependency lowest common denominator** — file-based by default, external systems are the upgrade path.
4. **Quota is a shared resource** — thrift is the default for multi-agent dispatch; full power is an explicit switch.

## Repo layout

```
MyR2D2/
├── .claude-plugin/marketplace.json    ← one marketplace, two plugins (zh-tw / en)
├── plugins/
│   ├── zh-tw/skills/…                 ← 5 skills, Traditional Chinese (primary)
│   └── en/skills/…                    ← 5 skills, English (same names)
├── adapters/openai/                   ← ChatGPT / Codex porting kit
├── README.md                          ← zh-TW (primary)
└── README.en.md                       ← this page
```

## Attribution

- `token-optimizer` is adapted from [kieiken/ultracode-token-optimization](https://github.com/kieiken/ultracode-token-optimization) (MIT), generalized for all-Claude environments.

## License

MIT — see [LICENSE](LICENSE).

*MyR2D2 is fan-tribute naming, unaffiliated with Lucasfilm / Disney; R2-D2 and Star Wars are trademarks of their respective owners.*
