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

## 2026-09-05 審查：`0f74f67` → `699b438`（15 個 commit，上游 v0.7.0–v0.7.3）

上游在此區間新增第 11、12 支 skill 並對 `new-mission` 做了五輪行為修正。逐筆判斷如下——分類依據是實際 diff 與本 fork 現況，不是 commit 標題。

| 上游 commit | 內容 | 判斷 | 依據 |
|---|---|---|---|
| `4de53ea` | 新增 `ai-search`、`new-mission` 兩支 skill＋prompts 四檔＋連動 | `adopt` | 兩支皆與 fork 既有 skill 無衝突；`ai-search` 與 `ai-review` 同架構，測試矩陣可直接接進本 fork 的 gate |
| `455517d` | 發版前跨模型二審的措辭修正（`ai-review`／`ai-search`／`new-mission`／README／TEST_PLAN） | `adopt` | `ai-review/SKILL.md` 的兩處（用法錯誤不印狀態、`ok` 的語意界定）與 fork 的 timeout 客製不重疊，手動併入而非整檔覆蓋 |
| `e002378` `ea27d9c` `60f5d82` `699b438` | 上游四次 `plugin.json` 版號 bump（v0.7.0／v0.7.1／v0.7.2／v0.7.3） | `skip` | 版號是 fork 自己的序列（見 `docs/DECISIONS.md` 2026-09-05）；內容改動已個別採納 |
| `49587f1` | `new-mission` 第 7 步收尾報告五格＋`damage-report` 交叉引用 | `adopt` | `damage-report/SKILL.md` 在 fork 端未曾改動，整檔取上游版無衝突 |
| `73d79e4` | TEST_PLAN 的 CROSS-01 per-agent 重驗記錄（gemini-cli／codex 各 12/12） | `defer` | 那是**上游 12 支** working tree 量出來的數字，與 fork 的 14 支不可相加。已在 TEST_PLAN C 段以 v0.8.0 註記明寫「不改寫成 14/14」；重查條件＝本 fork 自己重跑 CROSS-01 |
| `ea78177` `a0148f3` `6b01129` `cee6243` `75bed90` `e3c24bc` | `new-mission` 的五輪行為修正（開場分流／候選編號化／報告附 prompt 全文／落地優先於蒸發／時間行含 IANA 時區／時區「驗過才印」）＋末兩筆連帶改 `save-all` | `adopt` | 這些改動已包含在採納的 `new-mission/SKILL.md` 最終狀態內；`save-all/SKILL.md` 在 fork 端未曾改動，整檔取上游版無衝突 |
| `ea3513d` | 12 支速查小抄 `docs/cheatsheet.md` ＋ 4:5 圖卡 `docs/cheatsheet.png` | `adopt`（md）／`skip`（png） | md 改寫為 14 支並補上 `recap`／`blind-review` 兩列；png 是 12 支的渲染圖、repo 無來源檔可重製，收錄等於在 repo 裡放一張講錯支數的圖 |

🔑 **採納的上游檔案中，有三處不是逐字照收**——下次 `git fetch upstream` 會在這三處撞衝突，先記在這裡：

| 檔案 | 與 `699b438` 的差異 | 為什麼 |
|---|---|---|
| `skills/ai-search/tests/matrix.sh` | 落檔權限 `0600` 一項補上 `MINGW*\|MSYS*` → `skip_` 分支（與 `ai-review/tests/matrix.sh` 同形） | 上游只有單行 `ok_ \|\| no_`，在 Windows Git Bash 上必紅（NTFS 不提供 POSIX mode-bit 證據）。這是本 fork 既有的平台邊界，不是放水：Linux CI 仍必驗該項 |
| `skills/ai-search/SKILL.md` | ① 第 116 行去尾隨空白 ② 測試段的平台宣稱改寫 | ① 上游該行帶尾隨空白，本 repo 的 `git diff --check` 關卡會擋 ② 上游寫「Windows 未實測」，但本 fork 已把矩陣接進 Windows canonical gate 並實測 42 過 1 略，照抄會與 `docs/TEST_PLAN.md` F-01 打架；順帶依鐵則 1 拿掉本機實測的日期戳 |
| `skills/ai-review/SKILL.md` | 上游 `455517d` 的兩處措辭手動併入，未整檔覆蓋 | fork 端有 `--timeout`／測項數等客製，整檔取上游會清掉 |

v0.8.1 又多了四處（都是 Windows 實跑才浮出來的真缺陷，見 `docs/TEST_PLAN.md` F-05）：

| 檔案 | 差異 | 為什麼 |
|---|---|---|
| `skills/ai-search/scripts/ai-search.sh`、`skills/ai-review/scripts/ai-review.sh` | 新增 `winpath()`，傳給 codex 的 `-C`／`-o` 在 MSYS 上經 `cygpath -w` 轉換 | 原生 Windows 的 `codex.exe` 讀不懂 POSIX 路徑，回 `os error 2` 並被歸成 `failed_unknown`。**兩支腳本在 Windows 上從來沒真正碰到過真實後端**，而矩陣看不見（stub 是 sh 腳本、POSIX 路徑照吃） |
| `skills/ai-search/tests/matrix.sh`、`skills/ai-review/tests/matrix.sh` | 新增「傳給後端的 `-C` 路徑格式」測項（攔截 argv） | 上一格那個缺陷沒有任何測試守得住；附陽性對照確認會轉紅 |
| 同上兩份矩陣 | frontmatter YAML 驗證改走 stdin＋`stdin.buffer.decode('utf-8')` | 原寫法把 POSIX 路徑交給原生 Windows `python3`（FileNotFoundError），改 stdin 後又依 locale 解碼（cp950 → `unacceptable character #xdce5`）。兩者都把合法 frontmatter 誤判成壞掉，且有沒有設 `PYTHONIOENCODING` 結果不同＝假 flaky |
| `skills/new-mission/SKILL.md`、`skills/save-all/SKILL.md` | 取時區的退路由 `%Z` 縮寫改為 `UTC±hhmm`（有縮寫才附上） | Git Bash 沒有 `/etc/localtime` 也沒有 `/usr/share/zoneinfo/`，`date +%Z` 回空白字串——上游寫法在本 fork 的主平台上 100% 印出空的時區標籤，等於那一行的存在理由（讓人讀得出是哪裡的幾點）被抹掉。實測改後為 `UTC+0800（非 IANA 名稱）` |

其餘採納檔案（`ai-search/scripts/ai-search.sh` 的其餘部分、`damage-report`、四份 prompts）與上游逐位元組相同。

🔁 **這四處都值得回貢上游**（同樣的缺陷在上游 repo 也在）。依 fork 規則，回貢要維護者在當次對話明確同意，**本次未提 PR**。

fork 端的連動改動（同一批）：兩份 README 計數 12→14＋新增列＋新註⁷、`docs/cheatsheet.md`、`CLAUDE.md` 連動表行號與 H3 慣例、`AGENTS.md`／`FORK.md` 支數敘述、`.claude-plugin/` 兩檔、`.github/workflows/ci.yml`（計數 12→14＋ai-search 矩陣關卡）、`tools/check_repo_contract.py`（12→14）、`tools/dev_check.sh`／`dev_check.ps1`（接上 ai-search 矩陣）、`.gitignore`（`.ai-searches/`）、`docs/TEST_PLAN.md`（計數、F 段、C 段 v0.8.0 註）。

~~`defer`：時區退路~~ → **v0.8.1 已修**（上表第四列），不再是待辦。

本次沒有對 upstream 寫入。

## 2026-09-06 補驗：v0.8.0 誠實帳上最後兩項

v0.8.1 收尾時仍掛著兩項「本 fork 未驗」。兩項都用繞道補上了，**繞道方式本身也是結論的一部分**：

| 項目 | 阻礙 | 繞道 | 結果 |
|---|---|---|---|
| `ai-search` 真實後端 `ok` 路徑 | 預設後端 codex 帳號額度用盡（`try again at Sep 7th`） | 改走 skill 自己文件化的可插拔後端 `AI_SEARCH_CMD='claude -p --allowedTools WebSearch'` | ✅ `AI_SEARCH_STATUS: ok`＋exit 0，結論先行、附兩個官方來源、主動標時效與未查範圍。**答出 Codex `0.153.4`（比本機安裝的 `0.150.0` 還新）＝確實查了即時網路** |
| Gemini CLI 發現層 | 本機沒裝 Gemini CLI | `npx --yes @google/gemini-cli`（免全域安裝）＋隔離 `HOME`／隔離專案 | ✅ 未信任時磁碟 14 支、列出 **0** 支並印關卡訊息；信任後列出 **14 支全 `[Enabled]`**（gemini-cli 0.58.0） |

**2026-09-06 續**：上面那兩條「要等額度／範圍未及」的尾巴當天就清掉了——

| 項目 | 結果 |
|---|---|
| 預設 codex `web_search` 路徑的 `ok` | ✅ 額度恢復後補驗通過（附官方來源、自行分級官方 vs 二手） |
| F-04：`web_search` 旗標是否真的生效 | ⚠️ **上游推論被否證**——做了上游沒做的負對照（拿掉旗標、其餘相同），**照樣會搜**；本機 config 查無相關設定，排除「使用者自己全域開啟」。旗標保留但不再宣稱是搜尋的成因，腳本註解與 SKILL.md 同步改寫 |
| 執行層（CROSS-05，**repo 建立以來從沒跑過**） | ✅ `dropoff` 在 **Codex CLI** 與 **Claude Code CLI** 各端到端跑一次，兩張卡的 frontmatter 逐欄符合規格；兩個 agent 還各自獨立走到「無門鈴能力就降級」的正確行為 |
| 附帶修正 | README 註⁵ 的「Windows 非互動 `-p` 跑不出來」收窄為**特定 skill（`damage-report`）的**限制——同一個 `-p` 模式成功跑完 `dropoff` |

❓ 真正還沒量的只剩兩處，都寫上了解除條件：
- **`gemini-cli` 執行層**：`skills list` 不需憑證，真的呼叫模型要 Google 帳號／API key，
  屬使用者才能決定的事，未代為設定。
- **執行層抽測只涵蓋 `dropoff` 一支**，不自動延伸到需外部 connector（`flight-to-calendar`）
  或需子代理（`blind-review`）的 skill。

📌 過程中撞到第三次同款 Windows 路徑坑：`git -C "$(mktemp -d)"` 讓原生 Windows git 收 POSIX 路徑，
靜默失敗 → 0 支裝進去 → 第一次的「未信任時看不到 skill」是**假陽性**（本來就沒東西可看）。
改用 `cygpath -w` 重做才是真的。這已經是同一天內第三次（`codex.exe`、`python3`、`git`）——
`docs/DECISIONS.md` 已把它升為慣例。

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
