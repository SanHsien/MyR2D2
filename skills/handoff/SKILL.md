---
name: handoff
description: 跨專案／跨 session 交接「推球」。把一件事連同完整脈絡交給另一個專案（或同專案的未來 session）的 Claude。當使用者說「交接給 X」「handoff 給某專案」「把這件事丟給下個 session」時觸發。產出＝目標專案 `.claude/handoffs/` 下的一張交接卡（Markdown 檔），對面 session 用 /pickup 接手。 English triggers: "hand this off to X", "handoff to <project>", "pass this to the next session".
---

# /handoff — 交接·推球

把一件事**可靠地**交給另一個 Claude session（別的專案、或同專案的下一個 session）。

核心問題：對面 session 讀不到你這個對話的 context。口頭交代會漏、聊天記錄會斷 —— 所以交接卡必須是**磁碟上的檔案**，寫清楚到「陌生 session 光看這張卡就能接手」。

> 🤖 R2-D2 時刻：Leia 把 Death Star 圖紙和求救訊息存進 R2 的記憶體 —— 這就是 handoff。
> 訊息不靠 Leia 本人送達，靠的是那台會自己滾去找 Obi-Wan 的機器人。

## 交接卡格式

一張卡 = 一個 Markdown 檔，放在**目標專案**的 `.claude/handoffs/` 目錄：

```
<目標專案根目錄>/.claude/handoffs/YYYYMMDD-HHMM-<短slug>.md
```

```markdown
---
status: pending          # pending → picked → done
from: <來源專案或 session 描述>
to: <目標專案>
created: YYYY-MM-DD HH:MM
priority: high | normal | low
---

# <事項一句話>

## 要做什麼
<具體、可執行的任務描述>

## 脈絡（陌生 session 也看得懂的程度）
<為什麼要做、之前做到哪、決策背景>

## 相關檔案／連結
- <路徑或 URL，一行一個>

## 完成的定義
<怎樣算做完 —— 可驗證的條件，不是感覺>
```

## 用法

`/handoff <目標專案路徑或名稱> <事項>`

- 沒給目標 → 問使用者。
- 目標是「同專案的未來 session」→ 寫進本專案自己的 `.claude/handoffs/`。

## 動作

1. **建目錄**（若不存在）：`mkdir -p <目標專案>/.claude/handoffs`
2. **寫卡**：依上述格式。「脈絡」與「完成的定義」是卡的靈魂 —— 只寫標題的交接卡等於沒交接。
3. **驗證落地**：寫完 `cat` 回讀確認內容完整（寫入可能靜默失敗，別信工具回的成功訊息字面）。
4. **回報**：卡片路徑＋一句摘要＋提醒「對面 session 跑 `/pickup` 即可接手」。

## 鐵律

- **一卡一事**。兩件事就寫兩張卡，別打包。
- **脈絡自包含**：假設讀卡的 session 對你的對話一無所知。需要的背景、連結、路徑全放卡上。
- **時效性高的事**，除了寫卡，再用你手上現有的即時通道（通知、訊息）提醒使用者一聲 —— 卡是 pull 模型，對面不開工就不會讀。
- 配對命令＝`/pickup`（對面接手）。

## 進階：接上你自己的任務系統

如果你有跨專案的任務管理系統（CLI todo、Notion、Linear、GitHub Issues…），可以把「寫卡」替換成「在你的系統建一筆 type=handoff 的任務」，`/pickup` 端同步替換查詢方式。檔案版是零依賴的最小公倍數，不是天花板。
