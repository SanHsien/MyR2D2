# MyR2D2 🤖

### 你的隨行 astromech droid — Claude skillset（繁中本體、中英雙語觸發）

**繁體中文（本頁）| [English](README.en.md)**

---

R2-D2 從來不是主角，但每一集都靠它：把 Death Star 圖紙帶出來、滾過沙漠找到 Obi-Wan、在 X-wing 後座默默修飛船管能源。

MyR2D2 就是這個定位 —— 9 支 skills，管的都是「不做不會死、但做了整個工作流才活得下去」的事:

| Skill | 一句話 | R2-D2 對應 |
|---|---|---|
| **save-all** | 收工/重開機前，把只活在對話裡的東西全部落地並**驗證**寫進磁碟 | 圖紙存進 R2、彈射逃生艙 |
| **dropoff** | 把一件事連同完整脈絡寫成交接卡，推給另一個 session | Leia 錄下「Help me, Obi-Wan」 |
| **pickup** | 新 session 開場撈交接卡，讀全文、認領、開工 | R2 找到 Obi-Wan，播放訊息 |
| **mission-log** | 零 token 收割任一天的 session 活動骨架（transcript 本來就在記，只差讀取器） | 飛行記錄器從不休息 |
| **daily-debrief** | 日結：做了什麼＋reflection，趕在 transcript 30 天蒸發前把價值撈上岸 | 任務歸來的 debrief |
| **weekly-debrief** | 週結：7 份日結收斂成主線與趨勢 | 看得出補給線問題的是戰役，不是單次任務 |
| **damage-report** | 收尾自檢五問：寫回報前先對照原始需求跑一輪；建議欄沒有就寫「無」 | 修完飛船自己跑一輪診斷，嗶嗶回報損傷——不等 Luke 問 |
| **token-optimizer** | 多代理派工前的節流鐵則：模型分層、壓縮上報、失敗三次就停 | 能源分配，別讓護盾吃光動力 |
| **flight-to-calendar** | 航班上 Google Calendar：跨時區不出錯、轉機拆段、夕陽座位 | astromech 本職：導航 |

## 一組 skill、兩種語言習慣

Skill 本體是繁體中文（單一真相，不維護平行翻譯版）;**觸發詞中英各一組對應**，寫在每支 skill 的 description 裡:

- 中文習慣：「要重開機了」「交接給 X」「有沒有交接給我的」
- English habit: "about to reboot", "hand this off to X", "anything handed off to me?"

Claude 讀繁中指令、照樣用你的對話語言回覆 —— 英文使用者的體驗不打折，而 skill 永遠只有一份要維護。

## 為什麼需要這套？

Claude 的 session 是**失憶的**：對話一關，沒寫進磁碟的東西全部蒸發。這套 skills 的共同主題就是對抗失憶:

- `save-all` 管「關掉之前」— in-flight 狀態外部化，而且**驗證真的落地**（寫入會靜默失敗，別信「成功」字面）。
- `dropoff` / `pickup` 管「跨過去之後」— 交接卡寫到陌生 session 光看卡就能接手的程度。
- `mission-log` / `daily-debrief` / `weekly-debrief` 管「更長的時間軸」— transcript 30 天就自動刪除，日結/週結把價值在蒸發前收斂成可長存的記錄。
- `damage-report` 管「收尾那一刻」— 「改完能跑」不等於「做對了」，五問攔下假完成／假驗證／安靜失敗。
- `token-optimizer` 管另一種資源：訂閱制的**用量配額**。多代理 fan-out 漏指定模型，配額瞬間蒸發。

以上全部是在真實日常使用中踩坑迭代出來的，不是理論設計。

## 安裝

### skills.sh（`npx skills`）——推薦，一行裝完

[![skills.sh](https://skills.sh/b/tingyulu/MyR2D2)](https://skills.sh/tingyulu/MyR2D2)

```bash
npx skills add tingyulu/MyR2D2
```

[`npx skills`](https://github.com/vercel-labs/skills) 支援 Claude Code 與其他多種 agent（`gemini-cli`、`codex`、`cursor`…，完整清單見上游 README）。本 repo 已實測 gemini-cli／codex 的安裝層（方法與證據見 [docs/TEST_PLAN.md](docs/TEST_PLAN.md)），其餘目標未實測。**預設裝到專案層** `./.claude/skills/`；要裝成全域才加 `-g`。想只裝其中幾支用 `--skill`。

### Claude Code CLI — Plugin（深度整合）

```
/plugin marketplace add tingyulu/MyR2D2
/plugin install myr2d2@myr2d2
```

skill 掛在 `myr2d2:` 命名空間下（`/myr2d2:dropoff`…）——與你機器上既有的同名 skill 結構上不衝突，且可經 marketplace 集中更新。

### Claude Code CLI — 手動複製

```bash
git clone https://github.com/tingyulu/MyR2D2.git
cp -rn MyR2D2/skills/* ~/.claude/skills/
```

⚠️ 用 `-n`（不覆蓋既有檔）：若你 `~/.claude/skills/` 底下已有同名資料夾，`cp -r` 會**直接覆蓋且不提示**。想更新既有的，先自己 diff 過再決定。

### 只用網頁版 Chat？免安裝簡版

不用 CLI、不裝任何東西：[prompts/](prompts/) 有可直接貼進對話（或 custom instructions）的簡版 prompt，規則類 skill 適用——首發 `damage-report`（[繁中](prompts/damage-report.md)｜[EN](prompts/damage-report.en.md)；另有 ≤1,500 字元[極簡版](prompts/damage-report.lite.md)供 ChatGPT Free 等窄欄位）。

### Cowork / claude.ai

把要用的 skill 資料夾（`skills/<名稱>/`）加進你的 Cowork 專案 skills（或專案目錄的 `.claude/skills/`）。

裝完打 `/save-all`、`/dropoff`、`/pickup`、`/daily-debrief` 等即可觸發，或用上面任一語言的自然語句。

## 更新

skill 裝進去的是當下快照，**有新版不會自動通知**。更新方式：

```bash
npx skills update
```

一行更新所有已裝 skill（來源記在安裝時的 lock 檔；`-g`／`-p` 限定全域／專案層）。Plugin 路徑裝的改用 `/plugin` 介面更新 marketplace。想在新版發布時收到通知：GitHub 上對本 repo **Watch → Custom → Releases**。

## 相容性矩陣

| Skill | Claude Code CLI | Cowork / claude.ai | Gemini CLI | Codex CLI | ChatGPT（僅手動貼入） |
|---|---|---|---|---|---|
| save-all | ✅ | ✅（token 統計步自動跳過） | ✅（同左） | ✅（token 統計步刪掉） | ⚠️ 僅檢查清單 |
| dropoff / pickup | ✅ | ✅ | ✅ | ✅ | ❌（無共用磁碟） |
| mission-log / daily-debrief / weekly-debrief | ✅ | ❌（無本機 transcript） | ❌² | ❌² | ❌² |
| damage-report | ✅ | ✅（規則類，零工具依賴） | ✅（規則類） | ✅（規則類） | ⚠️ 貼入當收尾檢查清單 |
| token-optimizer | ✅ | ✅（規則類，無工具依賴） | ⚠️ 原則通用¹ | ⚠️ 原則通用¹ | ⚠️ 原則通用¹ |
| flight-to-calendar | ✅（需 Calendar connector） | ✅（需 Calendar connector） | ⚠️ 需自備 Calendar MCP（未實測） | ❌ 無 Calendar 工具 | ⚠️ 需自備 Action |

¹ 五鐵則通用、模型名自行對換；§1「進階兜底」（settings.json／env）僅 Claude Code 生效，其他工具跳過。
² 日誌三支的資料來源是 **Claude Code 自家的 transcript**（`~/.claude/projects/`）——skill 格式裝得進其他工具，但那裡沒有這份資料，故標 ❌。

- **Gemini CLI／Codex CLI**：安裝與發現層已實測——含 Gemini 的 trusted-folder 關卡（skill 沒出現時，先信任專案資料夾）；執行層未實測。
- **ChatGPT**：無 CLI／無檔案系統，唯一路徑＝手動貼入（見 adapters）。
- Cursor／Copilot 等其他 `npx skills` 目標：未實測。

ChatGPT / Codex 的移植方法（首選 `npx skills`、備援 AGENTS.md 併入、三個坑）見 **[adapters/openai/](adapters/openai/README.md)**。

## 各 skill 的依賴

| Skill | 依賴 |
|---|---|
| save-all | 無（token 統計那步限 Claude Code CLI，選跑） |
| dropoff / pickup | 無 — 交接卡就是專案目錄下的 Markdown 檔(`.claude/handoffs/`) |
| mission-log | 無 — 收割器為純標準庫 python3 腳本，零 token |
| daily-debrief | **需一併安裝 mission-log**（收割器在那支裡） |
| weekly-debrief | **需一併安裝 daily-debrief 與 mission-log**（缺日結會自動補生成） |
| damage-report | 無（純規則;第 5 問提到的 `/dropoff` 為選用交叉引用） |
| token-optimizer | 無（規則類 skill;Workflow 相關條目需要有 Workflow tool 的環境;§1「進階兜底」僅 Claude Code CLI 生效） |
| flight-to-calendar | **Google Calendar MCP connector**（硬依賴） |

dropoff/pickup 預設是零依賴的檔案版；如果你有自己的任務系統(CLI todo、Notion、Linear…),SKILL.md 內附「接上你自己的任務系統」的替換說明。

## 設計原則

1. **驗證優先於宣告** — 寫入要回讀驗證，完成要證據，不信字面成功訊息。
2. **脈絡自包含** — 交接卡假設讀者對前情一無所知。
3. **零依賴的最小公倍數** — 預設檔案版，進階才接外部系統。
4. **配額是共享資源** — 多代理派工的預設是省，全力跑是顯式開關。
5. **單一真相** — skill 只有一份（繁中），語言習慣靠雙語觸發詞對應，不維護平行翻譯版。

## Repo 結構

```
MyR2D2/
├── .claude-plugin/                    ← plugin.json + marketplace.json(單一 plugin)
├── skills/                            ← 9 支 skill(繁中本體、雙語觸發)
│   ├── save-all/  ├── dropoff/  ├── pickup/
│   ├── mission-log/  ├── daily-debrief/  ├── weekly-debrief/
│   ├── damage-report/  ├── token-optimizer/  └── flight-to-calendar/
├── prompts/                           ← 免安裝簡版(貼進 Chat 就能用)
├── adapters/openai/                   ← ChatGPT / Codex 移植包
├── README.md                          ← 本頁(中文為主)
└── README.en.md                       ← English
```

## Attribution

- `token-optimizer` 改寫自 [kieiken/ultracode-token-optimization](https://github.com/kieiken/ultracode-token-optimization)(MIT)，泛化為全 Claude 環境版本。

## License

MIT — 詳見 [LICENSE](LICENSE)。

*MyR2D2 是粉絲致敬命名，與 Lucasfilm / Disney 無任何關聯；R2-D2 及 Star Wars 為其各自權利人之商標。*
