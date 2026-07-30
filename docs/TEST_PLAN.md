# MyR2D2 測試計畫

> 本計畫的存在理由：v0.1.1 帶著 5 支無效 YAML 上線三天無人發現（`npx skills add` 對**所有** agent 0/5 全滅，不只 Claude Code）。教訓＝**發布關卡必須擋在 push 之前，且驗證範圍要涵蓋所有宣稱相容的工具**。
>
> 各項標註可測性：🟢 本機純機械可測／🟡 需對應 agent CLI 在場／✋ 需人工判讀。

## 層次定義（跨工具相容的三層，逐層驗、不可混談）

1. **安裝層**：`npx skills add` 能把檔案裝進該 agent 的 skills 目錄。
2. **發現層**：該 agent 本體真的列出／載入這些 skill（安裝成功 ≠ 看得到，見 CROSS-02 的 trusted-folder 教訓）。
3. **執行層**：agent 收到觸發詞後真的照 SKILL.md 內文正確行事。

---

## A. 發布前回歸（每次 release tag 前必跑，全綠才可 push）

### REG-01 🟢 YAML frontmatter 雙 parser 驗證

```bash
python3 -c "
import yaml,glob,re
for f in sorted(glob.glob('skills/*/SKILL.md')):
    m=re.match(r'^---\n(.*?)\n---\n',open(f).read(),re.S)
    try: print('OK  ',f,list(yaml.safe_load(m.group(1)).keys()))
    except Exception as e: print('FAIL',f,type(e).__name__)
"
```

**通過**：5 支全 `OK`。有第二個 parser（ruby psych／js-yaml）就交叉驗。這是 v0.1.1 事故的直接回歸項。

### REG-02 🟢 agentskills.io 官方 validator

```bash
for d in skills/*/; do npx --yes skills-ref validate "$d"; done
```

**通過**：5 支全過。驗 name 格式（小寫/連字號/=目錄名）、description ≤1024 字等規格硬約束。

### REG-03 🟢 本地安裝煙霧測試

```bash
cd "$(mktemp -d)" && git init -q . && npx --yes skills@latest add <repo根目錄> -y
```

**通過**：回報 `Installed 5 skills`、0 個 Skipped。

### REG-04 🟢 公開內容守門

跑 repo `CLAUDE.md` 鐵則 1 的守門 grep（含 `--untracked` 與 `-i`），除已知預期命中外 0 命中。

### REG-05 🟢 文件連動掃描

依 `CLAUDE.md` 鐵則 3 連動清單逐項核對（README 雙檔／plugin.json／marketplace.json／adapters 矩陣）。

---

## B. 跨工具相容（宣稱相容的每個工具，逐層驗證）

### CROSS-01 🟢 多 agent 安裝層矩陣

```bash
for a in gemini-cli codex cursor github-copilot; do
  (cd "$(mktemp -d)" && git init -q . && npx --yes skills@latest add <repo根目錄> --agent $a -y)
done
```

**通過**：每個 agent 都 `Installed 5 skills`、0 Skipped。
狀態（2026-07-30）：gemini-cli／codex 已實測通過；cursor／github-copilot 未實測。

### CROSS-02 🟡 Gemini CLI 發現層（trusted-folder 關卡）

```bash
gemini skills list --all   # 分別在「未信任」與「已信任」的專案目錄各跑一次
```

**通過**：未信任時輸出含 `Skipping project agents due to untrusted folder`（skill 不出現＝**預期行為**，不是 bug）；信任該資料夾後 5 支全部列出並標 `[Enabled]`。
⚠️ 這道關卡是無聲的（不報錯），文件必須揭露，否則使用者會以為安裝失敗。建議用隔離 `HOME` 測「已信任」情境，避免動到真實 `~/.gemini/trustedFolders.json`。
狀態（2026-07-30，gemini 0.40.0）：未信任情境已實測吻合；已信任情境未實測。

### CROSS-03 🟡 Codex CLI 發現層（原生注入驗證）

```bash
# 於已用 --agent codex 裝好的專案目錄：
codex debug prompt-input "test" | grep -E "dropoff|pickup|save-all|token-optimizer|flight-to-calendar"
```

**通過**：5 支 name＋description 均出現在 model-visible prompt 的 skills 區塊。
狀態（2026-07-30，codex-cli 0.145.0）：已實測通過——Codex 有原生 skill 機制（`~/.codex/skills/.system/`），**不需**手動併入 AGENTS.md。

### CROSS-04 🟢 ChatGPT 消費版陰性對照

```bash
npx --yes skills@latest add <repo根目錄> --agent chatgpt -y
```

**通過**：CLI 回報 `Invalid agents: chatgpt`（**預期失敗**）。ChatGPT 消費版無檔案系統／無 CLI，唯一路徑是 `adapters/openai/` 的手動貼入法。此項用來持續確認該定位仍準確。

### CROSS-05 ✋ 執行層端到端（每個 release 至少抽測一支）

在隔離目錄以各 agent 非互動模式觸發低風險 skill（建議 `dropoff`）：

```bash
codex exec "觸發 dropoff：幫示範任務寫一張交接卡"     # 或 gemini -p "..."
```

**通過**：真的產出交接卡檔案，frontmatter（status/from/to/created）齊全、內容符合 SKILL.md 步驟。需人工核對格式，「有產出檔案」不算過。
狀態（2026-07-30）：未實測（gemini／codex 皆在場可測）。

### CROSS-06 🟢 事故回歸（YAML × 真實安裝）

REG-01 ＋ REG-03 合跑。此缺陷影響**所有** npx-skills 下游 agent，不是 Claude Code 特有——發布關卡的涵蓋範圍要與此對齊。

### CROSS-07 ✋ 矩陣宣稱 × 實測交叉稽核

README 相容性矩陣與 adapters 上的每個 ✅／⚠️／❌，都要能對應到一次實際指令輸出佐證（本項曾抓到 adapters 對 Codex 的描述整段過時）。有落差→下個 release tag 前修文件或重測。

---

## C. 相容性結論快照（2026-07-30，過期重驗）

| 工具 | 安裝層 | 發現層 | 執行層 |
|---|---|---|---|
| Claude Code CLI | ✅ 實測（npx／plugin 雙路徑） | ✅ | ✅（日常使用） |
| Gemini CLI 0.40.0 | ✅ 實測 5/5 | ⚠️ 需先信任資料夾（無聲關卡） | ❓ 未測 |
| Codex CLI 0.145.0 | ✅ 實測 5/5 | ✅ 實測（原生注入 prompt） | ❓ 未測 |
| ChatGPT 消費版 | ❌ 無安裝路徑（產品限制） | ❌ 無 skill 概念 | 僅手動貼入，網頁端人工驗 |
| Cursor／Copilot 等 | ❓ `npx skills` 支援但未實測 | ❓ | ❓ |
