---
name: token-optimizer
description: Token / quota discipline for multi-agent orchestration. BEFORE any Agent tool call or Workflow dispatch — whether or not the user mentioned saving tokens, and even for a single subagent — read this skill first. Also triggers when the user says "save tokens", "quota", "don't burn my limit". Trigger words - workflow, multi-agent, fan-out, subagent, orchestration, dispatch, token optimizer.
license: MIT
---

# Token Optimizer — discipline rules for multi-agent orchestration

> Adapted from [kieiken/ultracode-token-optimization](https://github.com/kieiken/ultracode-token-optimization) (MIT), generalized for all-Claude environments, 2026-07.
> Core insight: **saving tokens is not about unit price — it's about killing rework loops and context flooding.**
> The edit→review→re-edit→re-review loop, and piping raw diffs/logs back into the orchestrator,
> are where the real waste lives.

## 0. Why

- On subscription plans (e.g. Claude Max), saving tokens ≠ saving money — it's **saving usage quota**. Quota exhausted = every session stalls at once, which hurts more than a bill.
- **Flagship-tier models burn quota far faster than mid-tier.** That turns "model tiering" from nice-to-have into an iron rule.
- This skill covers two scenarios: ① Workflow scripts (`agent()`/`parallel()`/`pipeline()`) ② regular sessions spawning subagents via the Agent tool. Same principles for both.

## 1. Model tiering table (iron rule)

| Role | Assignment | Rationale |
|---|---|---|
| Orchestrator (the session itself) | Follows the session; don't touch | Judgment and arbitration only |
| Executor (writes code / edits files) | Mid-tier (e.g. `sonnet`) | Quality is enough, quota-friendly |
| Reviewer (fault-finding / review) | Mid-tier by default | Escalate to flagship only for high-risk domains (below) |
| Mechanical work (summaries / formatting / grep digests) | Low tier (e.g. `haiku`) or mid-tier + `effort: 'low'` | Don't spend expensive models on judgment-free work |
| Arbitration / final call | Unspecified (inherits session) | **The only exception — must carry a comment explaining why** |

**Reviewer escalation threshold** (any one qualifies): auth / payments / data-loss risk / security / concurrency / persistence / public API / large refactor.

**🔴 Absolute rule: when the session model is flagship-tier, every single `agent()` call must specify `model` explicitly** (arbitration lane excepted, with a comment). One omission = the whole fan-out inherits the expensive tier and your quota evaporates. This is reason #1 this skill exists.
> The criterion is "**the session runs on something pricier than mid-tier**", not any specific model name — new releases don't require editing this rule.

**⚙️ Backstop**: setting `env.CLAUDE_CODE_SUBAGENT_MODEL=sonnet` in `settings.json` hard-caps all subagents at mid-tier (empirically a hard ceiling — even explicit per-call overrides get clamped), so omissions stop burning flagship quota. To temporarily run at full power: override the env in **that project's** `.claude/settings.local.json` (affects only that project, takes effect live), delete when done. Precedence: project local > user global > process env > call parameter.

## 2. Compress results before reporting up (iron rule)

- Fix the subagent's report format in its prompt: **"reply only: done/not-done + changed-file list + test result, three-line summary."**
- Raw diffs, full logs, big JSON **never** flow back into the orchestrator's context — when detail is needed, dispatch a low-tier agent to read it and return a digest.
- In Workflows, force structured output with the `schema` parameter (validation failures auto-retry; more reliable and cheaper than free text).
- Regular Agent tool: end the prompt with "your final message IS the return value — conclusions and key evidence only, no process narration."

## 3. Role lockdown (iron rule)

- **The orchestrator never implements.** Detail decisions are delegated to agents in their lanes; the orchestrator intervenes only at phase boundaries and escalations.
- **Reviewers output findings only** (each with: trigger condition + repro steps + line references) — no fixes, no verdicts. Prompt says: "you output findings and severity; approval/rejection is not your jurisdiction."
- **Reviewer output never goes straight to the executor** — a synthesis agent (mid-tier is fine) sits between, filtering out unsupported findings and condensing the rest into terse fix instructions. Findings without evidence are dropped.
- **Executors don't self-certify.** "Done!" doesn't count.

## 4. Independent verification (iron rule)

- Define "done" in the prompt before work starts: file exists, test exit code, commit hash — machine-checkable evidence, not feelings.
- Completion is confirmed by a **dedicated verification agent**: verifies only, fixes nothing, returns structured evidence (testExit, diff summary).
- Final sign-off is **human**: return "a proposal awaiting the user's approval" — no auto-commit, no auto-publish.

## 5. Stop after three failures (iron rule)

- Every retry loop carries a **counter**: same error three times in a row → stop, report status and blockers, no more spinning.
- Workflow loops add a `budget.remaining()` guard (when a budget is set); flows without budgets use the counter + "3 identical failures = stop".
- The right response to consecutive failures is **changing the angle** (different model tier, different decomposition, or escalate the blocker) — not attempt #4 in place.

## 6. Structural thrift (defaults when writing scripts)

- **`pipeline()` over `parallel()`**: multi-stage multi-item flows use pipeline (no barrier, items flow independently); use a parallel barrier only when the next stage genuinely needs ALL previous results (dedup, aggregation, early-exit checks).
- One `agent()` does one thing; multiple targets = single-target thunks.
- Every `agent()` gets a `label`; keep volatile data (timestamps, random values) out of prompts so `resumeFromRunId` reruns hit cache.
- Diff cap per submission: 200–300 lines; anything bigger returns a split plan first.
- Only lanes that mutate files in parallel get `isolation: 'worktree'` (it has a cost); read-only lanes don't.

## 7. Pre-dispatch checklist (run through before submitting any script / dispatch)

- [ ] No raw diff/log/big JSON in the orchestrator prompt (§2)
- [ ] Every `agent()` has an explicit `model`, or a comment justifying inheritance (§1)
- [ ] Session on flagship tier → zero exceptions, all models specified (§1 absolute rule)
- [ ] Reviewer prompts include "no verdict authority; findings + severity + line refs" (§3)
- [ ] Reviewer output passes through a synthesis agent before reaching executors (§3)
- [ ] Completion confirmed by a dedicated verifier with evidence, not self-declared (§4)
- [ ] Retry counters + stop-after-3-identical-failures (§5)
- [ ] Multi-stage multi-item = `pipeline()`, no gratuitous barriers (§6)
- [ ] Subagent outputs structured via `schema` (§2)
- [ ] Every `agent()` labeled, prompts free of volatile data (§6)
- [ ] Final output is "a proposal awaiting approval", no auto-commit (§4)

## 8. Limitations (honest notes)

- This is a **behavioral code, not a hard token cap** — real ceilings need the Workflow `budget` mechanism plus `budget.remaining()` guards in scripts.
- The value comes from locking out the common waste patterns before the script is written (diff flooding, trusting self-certification, reviewer overreach) — no specific percentage savings are promised.
- The original used OpenAI Codex as executor for cross-vendor mutual review; in an all-Claude environment, heterogeneity via **model-tier differences** (mid-tier execute × mid-tier review with separate contexts, flagship arbitration when needed) is a partial substitute — inherently weaker, which is why §4's independent verification matters more here.
