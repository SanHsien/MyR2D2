# 維護決策

## 2026-08-24：採用維護型 fork

決定保留 MyR2D2 的產品名稱、MIT 歷史、原作者歸屬與 10-skill 介面，只新增維護治理與跨平台開發環境。原因是上游已有真實產品、發布與回歸矩陣；重新包裝核心只會增加漂移。

## 2026-08-24：Windows-first 不等於假裝 NTFS 是 POSIX

Windows 使用 PowerShell 作 canonical entrypoint，產品 shell 測試由 Git for Windows Bash 執行。NTFS 無法用 `ls -l` 證明 `0600`，因此 Windows 只允許該單一斷言明確 skip；Linux CI 仍須完整通過，沒有平台豁免。

## 2026-08-24：不建立 Python 套件

Python 維護工具只使用標準庫與 `gh`，不新增 `pyproject.toml` 或 requirements；`package-lock.json` 僅固定 `skills`／`skills-ref` 維護工具及其 integrity。repo 的交付物是 Agent Skills，不是 Python library。

## 2026-09-02：採納的上游程式碼要在 Windows 上「真的跑一次」，不是只跑矩陣

v0.8.0 交付時，`ai-search` 的相容性評級與真實後端行為都掛著「沿用上游、本 fork 未驗」。
把那幾格逐一實跑之後，浮出三個**只有真跑才會出現**的缺陷：`codex.exe` 讀不懂 POSIX 路徑
（`ai-review` 也有，等於兩支腳本在 Windows 上從沒碰到過真實後端）、矩陣的 frontmatter 驗證
在 Windows 上假紅兩次（路徑＋locale 解碼）、取時區的退路在 Git Bash 印出空標籤。

結論定為慣例：**採納上游腳本時，「矩陣全綠」不等於「在本平台可用」**。矩陣的 stub 是 sh 腳本，
天然吃得下 POSIX 路徑，看不見原生 exe 的介面差異。凡是會呼叫外部程式的 skill，採納時
至少對真實後端跑一次，並把該次觀察寫進 `docs/TEST_PLAN.md`——即使結果是失敗（本次就只驗到
`failed_quota`，因為帳號額度用盡）。**驗到失敗分類正確，也是證據；宣稱未驗，不是。**

## 2026-09-02：採納上游 v0.7.0–v0.7.3 的 15 個 commit

逐筆評估後採納兩支新 skill（`new-mission`、`ai-search`）與其連動改動，repo 由 12 支變 14 支。版號走 fork 自己的序列 `v0.8.0`，不對齊上游 `v0.7.3`——兩邊的 `v0.7.0` 已經是不同內容（fork 是 `recap`＋`blind-review`，上游是 `ai-search`＋`new-mission`），追平版號只會讓兩個 `v0.7.x` 更難分辨。

唯一 `skip` 的項目是 `docs/cheatsheet.png`：那是 12 支的渲染圖卡，與本 fork 的 14 支對不上，而 repo 沒有重製它的來源檔。缺一張圖優於放一張講錯支數的圖，`docs/cheatsheet.md` 內以一行說明取代。

`ai-search` 的相容性評級沿用上游實測、**未在本 fork 重驗**，此事在 README 註⁷ 與 TEST_PLAN F 段各標一次；行為矩陣則已接進兩個 canonical gate 與 CI，屬本 fork 自己會跑到的證據。
（**v0.8.1 更新**：這段的「未重驗」已大部分補上——安裝層本 fork 自量 14/14 × 三個 agent、矩陣在 Windows 實跑、真實後端驗到 `failed_quota` 分類正確；仍未驗的只剩真實後端的 `ok` 路徑與 Gemini 發現層。補驗過程翻出四個真缺陷，見上一則決策。）

## 2026-08-24：upstream 水位分離

commit、PR、issue 與 branch head 分別記錄。Baseline 表示已審查，不表示已合併；每次只處理水位之後的新狀態，避免重複成本與標題式判斷。
