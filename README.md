# MyR2D2 🤖

### 你的隨行 astromech droid — Claude skillset（繁中本體、中英雙語觸發）

**繁體中文（本頁）| [English](README.en.md)**

---

R2-D2 從來不是主角，但每一集都靠它：把 Death Star 圖紙帶出來、滾過沙漠找到 Obi-Wan、在 X-wing 後座默默修飛船管能源。

MyR2D2 就是這個定位 —— 5 支 skills，管的都是「不做不會死、但做了整個工作流才活得下去」的事:

| Skill | 一句話 | R2-D2 對應 |
|---|---|---|
| **save-all** | 收工/重開機前，把只活在對話裡的東西全部落地並**驗證**寫進磁碟 | 圖紙存進 R2、彈射逃生艙 |
| **handoff** | 把一件事連同完整脈絡寫成交接卡，推給另一個 session | Leia 錄下「Help me, Obi-Wan」 |
| **pickup** | 新 session 開場撈交接卡，讀全文、認領、開工 | R2 找到 Obi-Wan，播放訊息 |
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
- `handoff` / `pickup` 管「跨過去之後」— 交接卡寫到陌生 session 光看卡就能接手的程度。
- `token-optimizer` 管另一種資源：訂閱制的**用量配額**。多代理 fan-out 漏指定模型，配額瞬間蒸發。

三者都是在真實日常使用中踩坑迭代出來的，不是理論設計。

## 安裝

### Claude Code CLI — Plugin（推薦）

```
/plugin marketplace add tingyulu/MyR2D2
/plugin install myr2d2@myr2d2
```

### Claude Code CLI — 手動複製

```bash
git clone https://github.com/tingyulu/MyR2D2.git
cp -r MyR2D2/skills/* ~/.claude/skills/
```

### Cowork / claude.ai

把要用的 skill 資料夾（`skills/<名稱>/`）加進你的 Cowork 專案 skills（或專案目錄的 `.claude/skills/`）。

裝完打 `/save-all`、`/handoff`、`/pickup` 即可觸發，或用上面任一語言的自然語句。

## 相容性矩陣

| Skill | Claude Code CLI | Cowork / claude.ai | Codex / ChatGPT |
|---|---|---|---|
| save-all | ✅ | ✅（token 統計步自動跳過） | ✅ Codex / ⚠️ ChatGPT 僅檢查清單 |
| handoff / pickup | ✅ | ✅ | ✅ Codex / ❌ ChatGPT（無共用磁碟） |
| token-optimizer | ✅ | ✅（規則類，無工具依賴） | ⚠️ 原則通用，模型名自行對換 |
| flight-to-calendar | ✅（需 Calendar connector） | ✅（需 Calendar connector） | ❌ Codex / ⚠️ ChatGPT 需自備 Action |

ChatGPT / Codex 的移植方法（AGENTS.md 併入法、路由法、三個坑）見 **[adapters/openai/](adapters/openai/README.md)**。

## 各 skill 的依賴

| Skill | 依賴 |
|---|---|
| save-all | 無（token 統計那步限 Claude Code CLI，選跑） |
| handoff / pickup | 無 — 交接卡就是專案目錄下的 Markdown 檔(`.claude/handoffs/`) |
| token-optimizer | 無（規則類 skill;Workflow 相關條目需要有 Workflow tool 的環境） |
| flight-to-calendar | **Google Calendar MCP connector**（硬依賴） |

handoff/pickup 預設是零依賴的檔案版；如果你有自己的任務系統(CLI todo、Notion、Linear…),SKILL.md 內附「接上你自己的任務系統」的替換說明。

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
├── skills/                            ← 5 支 skill(繁中本體、雙語觸發)
│   ├── save-all/  ├── handoff/  ├── pickup/
│   ├── token-optimizer/  └── flight-to-calendar/
├── adapters/openai/                   ← ChatGPT / Codex 移植包
├── README.md                          ← 本頁(中文為主)
└── README.en.md                       ← English
```

## Attribution

- `token-optimizer` 改寫自 [kieiken/ultracode-token-optimization](https://github.com/kieiken/ultracode-token-optimization)(MIT)，泛化為全 Claude 環境版本。

## License

MIT — 詳見 [LICENSE](LICENSE)。

*MyR2D2 是粉絲致敬命名，與 Lucasfilm / Disney 無任何關聯；R2-D2 及 Star Wars 為其各自權利人之商標。*
