# MyR2D2 → ChatGPT / Codex 移植包
# MyR2D2 → ChatGPT / Codex adapter

*中文為主,English below per section.*

SKILL.md 本體就是純 Markdown 指令,任何能讀指令的 LLM 都吃得下。差別在「觸發機制」與「工具依賴」。本移植包告訴你哪些能直接搬、哪些要改、哪些搬不動。

The SKILL.md files are plain Markdown instructions — any instruction-following LLM can consume them. What differs is the *trigger mechanism* and *tool dependencies*. This adapter tells you what ports as-is, what needs edits, and what doesn't port.

## 可移植性總表 | Portability matrix

| Skill | Codex CLI | ChatGPT | 說明 Notes |
|---|---|---|---|
| save-all | ✅ | ⚠️ | Codex:git/檔案操作全通,token 統計那步刪掉(那是讀 Claude Code transcript 的)。ChatGPT:無本機檔案系統,只能當「收工檢查清單」用。<br>Codex: git/file ops all work; delete the token-count step (it reads Claude Code transcripts). ChatGPT: no local filesystem — usable only as a wrap-up checklist. |
| dropoff / pickup | ✅ | ❌ | 交接卡=磁碟上的 Markdown 檔,Codex CLI 完全可用。ChatGPT 沒有跨 session 共用磁碟,搬不動。<br>Cards are Markdown files on disk — fully portable to Codex CLI. ChatGPT has no cross-session shared disk. |
| token-optimizer | ⚠️ 原則通用 | ⚠️ 原則通用 | 五鐵則(分層/壓縮上報/角色鎖死/獨立驗證/失敗三停)通用;§1 模型名換成你家的檔位(如 o4-mini vs o3)、§6 的 Workflow API 條目刪掉。有趣的是:本 skill 的原作 kieiken/ultracode-token-optimization 就是 Codex 環境寫的,等於「移植回老家」。<br>The five iron rules are universal; swap §1 model names for your vendor's tiers, drop §6's Workflow-API items. Fun fact: the upstream (kieiken) was written FOR Codex — porting it back is going home. |
| flight-to-calendar | ❌ | ⚠️ | 硬依賴 Google Calendar 寫入工具。Codex CLI 無;ChatGPT 需自備 Calendar 的 Action/connector 才能用,規則本身(時區換算/一段一事件/夕陽座位)全通用。<br>Hard dependency on a Google Calendar write tool. Codex CLI: none. ChatGPT: needs a Calendar Action/connector; the rules themselves (timezone math, one-leg-one-event, sunset seats) are universal. |

## Codex CLI 安裝法 | Codex CLI setup

Codex 讀 `AGENTS.md`(專案根目錄或 `~/.codex/AGENTS.md`),沒有 skill 觸發機制 —— 把規則直接併進去:

Codex reads `AGENTS.md` (project root or `~/.codex/AGENTS.md`) and has no skill-trigger mechanism — merge the rules in directly:

```bash
# 把要用的 skill 內文(去掉 YAML frontmatter)接進 AGENTS.md
# Append the skill bodies (minus YAML frontmatter) into AGENTS.md
for s in save-all dropoff pickup token-optimizer; do
  echo -e "\n\n<!-- MyR2D2: $s -->" >> AGENTS.md
  sed '1,/^---$/d' ../../skills/$s/SKILL.md | sed '1,/^---$/d' >> AGENTS.md
done
```

或更省 context 的做法:AGENTS.md 只放一句路由 ——

Or the context-cheaper route — AGENTS.md carries one routing line:

```markdown
When the user says "save-all" / "dropoff" / "pickup", read and follow
docs/myr2d2/<name>.md before acting.
```

再把 skill 檔複製到 `docs/myr2d2/`。/ …and copy the skill files into `docs/myr2d2/`.

## 移植時的三個坑 | Three porting gotchas

1. **觸發詞不會自己生效** — Claude Code 靠 description 自動路由;Codex/ChatGPT 要嘛使用者手動說「照 save-all 流程走」,要嘛靠上面那句路由指令。<br>*Triggers don't fire by themselves — Claude Code auto-routes on descriptions; elsewhere the user invokes by name or you add the routing line.*
2. **「驗證落地」規則照搬** — 寫入靜默失敗不是 Claude 特有的,任何 agent 環境都該回讀驗證。這是全包最值得帶走的一條。<br>*Keep the "verify the write" rule — silent write failures aren't Claude-specific. It's the single most portable rule in this pack.*
3. **R2-D2 註解可刪** — 那是給人看的調味,不影響行為。<br>*The R2-D2 asides are seasoning for humans; deleting them changes nothing.*
