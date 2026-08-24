# AGENTS.md

本檔提供 Codex、Claude Code、Cursor 與其他自動化代理在本 fork 工作時的共同指引。產品規格先讀 [`README.md`](README.md) 與 [`CLAUDE.md`](CLAUDE.md)；開發與驗收細節見 [`docs/DEVELOPMENT.md`](docs/DEVELOPMENT.md)。

## 專案定位

本 repo 是 [`tingyulu/MyR2D2`](https://github.com/tingyulu/MyR2D2) 的 MIT 維護型 fork：

- `origin`：`SanHsien/MyR2D2`
- `upstream`：`tingyulu/MyR2D2`
- 預設分支：`main`
- Windows 權威入口：`pwsh -NoProfile -File tools\dev_check.ps1`
- Linux／macOS 入口：`sh tools/dev_check.sh`

主要開發平台是 Windows 11；Codex／Claude 等 Windows Desktop、Windows TUI 與 Windows CLI 都是一級宿主。Git Bash 只提供必要的 POSIX shell 相容層，Linux CI 補驗 POSIX 權限與多 shell 語義。

保留 MyR2D2 名稱、上游作者歸屬、10 支 skill、公開介面與 MIT 授權。fork 的維護差異記在 [`FORK.md`](FORK.md)、[`docs/DECISIONS.md`](docs/DECISIONS.md) 與 [`docs/UPSTREAM.md`](docs/UPSTREAM.md)。

## 硬性邊界

- 遵守 `CLAUDE.md` 的去識別化、SKILL.md 格式、連動清單、版號與本機安裝隔離規則。
- 不提交 API key、token、cookie、帳號資料、私人 prompt、真實客戶資料或 `.ai-reviews/` 產物。
- 跨模型 review 前先去識別化；送給後端的內容視為已離開本機信任邊界。
- 不把 Git Bash／NTFS 的 mode-bit 顯示當成 POSIX 權限證據。`0600` 安全斷言由 Linux CI 驗證。
- 不直接 push／force-push `main`，不刪除 `upstream` remote，不盲目 merge upstream。
- 不新增 CHANGELOG；版本與 release 慣例沿用 `CLAUDE.md`。

## 開發方式

- 所有變更使用 branch → `SanHsien/MyR2D2` PR → required checks → merge；branch protection 對管理者同樣生效。
- commit 使用 Conventional Commits，例如 `chore: add Windows development gate`。
- 修 bug 先建立可重現測試，再做最小修正。
- 改 skill 時必須同步檢查兩份 README、plugin metadata、adapter 與 `docs/TEST_PLAN.md`。
- `README.md` 與 `README.en.md` 行數必須一致。

## 上游同步

1. `git fetch upstream main`
2. `python tools/check_upstream_updates.py --strict`
3. 逐筆檢查 commit、PR、issue 與 branch head。
4. 把採用／略過／延後的證據寫入 `docs/UPSTREAM.md` 與 `docs/DECISIONS.md`。
5. 跑完整 gate 後才更新 `tools/upstream_baseline.json`。

Baseline 只表示「已審查」，不表示「全部已合併」。

## 對外邊界

- PR、push、release 一律指向 `SanHsien/MyR2D2`。
- 未經維護者在當次對話明確同意，不得對 `tingyulu/MyR2D2` push、開 PR、發 release 或觸發 workflow。
- 每個 clone 先執行 `gh repo set-default SanHsien/MyR2D2`，並以 `gh repo set-default --view` 核對。
- 建立 PR 時仍須明寫 `--repo SanHsien/MyR2D2`，並檢查輸出 URL 的 owner。

## 完成條件

```powershell
pwsh -NoProfile -File tools\dev_check.ps1
git diff --check
git status --short
```

沒有實際跑過 gate、檢查完整 diff 與遠端 exact SHA，不宣稱完成。
