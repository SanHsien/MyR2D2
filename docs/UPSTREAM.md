# Upstream review ledger

Upstream：[`tingyulu/MyR2D2`](https://github.com/tingyulu/MyR2D2)

除非維護者在當次對話明確授權，所有 PR、push、release 與 workflow dispatch 只指向 `SanHsien/MyR2D2`。

## 2026-08-24 初始水位

- `upstream/main`：`0f74f6737dc19f2dd055681a981121f8b29191f0`
- fork 建立時 `origin/main`：同一 SHA
- PR 水位：`0`（觀測時沒有任何 PR）
- issue 水位：`0`（觀測時沒有任何 issue）
- branch：只有 `main`，head 為同一 SHA

本次建立 fork、維護 overlay，並修正 `mission-log` 的 Windows UTF-8、主機名稱與時區邊界；沒有對 upstream 寫入，也沒有宣稱審查水位之後的未來狀態。

## 2026-09-02 審查：`0f74f67` → `699b438`（15 個 commit，上游 v0.7.0–v0.7.3）

上游在此區間新增第 11、12 支 skill 並對 `new-mission` 做了五輪行為修正。逐筆判斷如下——分類依據是實際 diff 與本 fork 現況，不是 commit 標題。

| 上游 commit | 內容 | 判斷 | 依據 |
|---|---|---|---|
| `4de53ea` | 新增 `ai-search`、`new-mission` 兩支 skill＋prompts 四檔＋連動 | `adopt` | 兩支皆與 fork 既有 skill 無衝突；`ai-search` 與 `ai-review` 同架構，測試矩陣可直接接進本 fork 的 gate |
| `455517d` | 發版前跨模型二審的措辭修正（`ai-review`／`ai-search`／`new-mission`／README／TEST_PLAN） | `adopt` | `ai-review/SKILL.md` 的兩處（用法錯誤不印狀態、`ok` 的語意界定）與 fork 的 timeout 客製不重疊，手動併入而非整檔覆蓋 |
| `e002378` `ea27d9c` `60f5d82` `699b438` | 上游四次 `plugin.json` 版號 bump（v0.7.0／v0.7.1／v0.7.2／v0.7.3） | `skip` | 版號是 fork 自己的序列（見 `docs/DECISIONS.md` 2026-09-02）；內容改動已個別採納 |
| `49587f1` | `new-mission` 第 7 步收尾報告五格＋`damage-report` 交叉引用 | `adopt` | `damage-report/SKILL.md` 在 fork 端未曾改動，整檔取上游版無衝突 |
| `73d79e4` | TEST_PLAN 的 CROSS-01 per-agent 重驗記錄（gemini-cli／codex 各 12/12） | `defer` | 那是**上游 12 支** working tree 量出來的數字，與 fork 的 14 支不可相加。已在 TEST_PLAN C 段以 v0.8.0 註記明寫「不改寫成 14/14」；重查條件＝本 fork 自己重跑 CROSS-01 |
| `ea78177` `a0148f3` `6b01129` `cee6243` `75bed90` `e3c24bc` | `new-mission` 的五輪行為修正（開場分流／候選編號化／報告附 prompt 全文／落地優先於蒸發／時間行含 IANA 時區／時區「驗過才印」）＋末兩筆連帶改 `save-all` | `adopt` | 這些改動已包含在採納的 `new-mission/SKILL.md` 最終狀態內；`save-all/SKILL.md` 在 fork 端未曾改動，整檔取上游版無衝突 |
| `ea3513d` | 12 支速查小抄 `docs/cheatsheet.md` ＋ 4:5 圖卡 `docs/cheatsheet.png` | `adopt`（md）／`skip`（png） | md 改寫為 14 支並補上 `recap`／`blind-review` 兩列；png 是 12 支的渲染圖、repo 無來源檔可重製，收錄等於在 repo 裡放一張講錯支數的圖 |

🔑 **採納的上游檔案中，有三處不是逐字照收**——下次 `git fetch upstream` 會在這三處撞衝突，先記在這裡：

| 檔案 | 與 `699b438` 的差異 | 為什麼 |
|---|---|---|
| `skills/ai-search/tests/matrix.sh` | 落檔權限 `0600` 一項補上 `MINGW*\|MSYS*` → `skip_` 分支（與 `ai-review/tests/matrix.sh` 同形） | 上游只有單行 `ok_ \|\| no_`，在 Windows Git Bash 上必紅（NTFS 不提供 POSIX mode-bit 證據）。這是本 fork 既有的平台邊界，不是放水：Linux CI 仍必驗該項 |
| `skills/ai-search/SKILL.md` | ① 第 116 行去尾隨空白 ② 測試段的平台宣稱改寫 | ① 上游該行帶尾隨空白，本 repo 的 `git diff --check` 關卡會擋 ② 上游寫「Windows 未實測」，但本 fork 已把矩陣接進 Windows canonical gate 並實測 42 過 1 略，照抄會與 `docs/TEST_PLAN.md` F-01 打架；順帶依鐵則 1 拿掉本機實測的日期戳 |
| `skills/ai-review/SKILL.md` | 上游 `455517d` 的兩處措辭手動併入，未整檔覆蓋 | fork 端有 `--timeout`／45 項測試等客製，整檔取上游會清掉 |

其餘採納檔案（`new-mission/SKILL.md`、`ai-search/scripts/ai-search.sh`、`damage-report`、`save-all`、四份 prompts）與上游逐位元組相同。

fork 端的連動改動（同一批）：兩份 README 計數 12→14＋新增列＋新註⁷、`docs/cheatsheet.md`、`CLAUDE.md` 連動表行號與 H3 慣例、`AGENTS.md`／`FORK.md` 支數敘述、`.claude-plugin/` 兩檔、`.github/workflows/ci.yml`（計數 12→14＋ai-search 矩陣關卡）、`tools/check_repo_contract.py`（12→14）、`tools/dev_check.sh`／`dev_check.ps1`（接上 ai-search 矩陣）、`.gitignore`（`.ai-searches/`）、`docs/TEST_PLAN.md`（計數、F 段、C 段 v0.8.0 註）。

`defer`（本次不動、記下重查條件）：`new-mission` 與 `save-all` 第 0／5 步的零依賴取時間片段標的是 macOS／Linux，靠 `/etc/localtime` 取 IANA 時區名——**Git Bash 沒有這個檔**，在本 fork 的主平台上必然落到 `date +%Z` 退路，而 Windows 的 `%Z` 回空字串，於是印出的時區標籤是空的。這不是正確性缺陷（片段的第三道守門本來就要求「對不上就標非 IANA、不准猜」，它確實沒猜），但在 Windows-first 的 fork 裡等於那條退路 100% 觸發卻無人記載。重查／處理條件：等上游自己補 Windows 分支，或本 fork 要動這兩支時一併補；先不為此改上游檔案，避免再多一處 fetch 衝突面。

本次沒有對 upstream 寫入。`ai-search` 的相容性評級沿用上游實測結論，本 fork **未重驗**，此事在 README 註⁷ 與 TEST_PLAN F 段各標一次。

## 判斷規則

- `adopt`：本 fork 已採用並有驗證證據。
- `skip`：有可檢查證據證明不適用。
- `defer`：問題可能有效，但要等明確觸發條件再重查。
- `baseline`：已存在於目前共同 ancestry，不需重做。

只看分類或標題不算證據。每筆判斷應指出實際 diff、受影響檔案、本 fork 現況與重查條件。

## 操作

```bash
git fetch upstream main
python tools/check_upstream_updates.py --strict
```

處理完新項目後，先更新本 ledger 與 `docs/DECISIONS.md`，跑完整 gate，再推進 `tools/upstream_baseline.json`。
