# 維護決策

## 2026-08-24：採用維護型 fork

決定保留 MyR2D2 的產品名稱、MIT 歷史、原作者歸屬與 10-skill 介面，只新增維護治理與跨平台開發環境。原因是上游已有真實產品、發布與回歸矩陣；重新包裝核心只會增加漂移。

## 2026-08-24：Windows-first 不等於假裝 NTFS 是 POSIX

Windows 使用 PowerShell 作 canonical entrypoint，產品 shell 測試由 Git for Windows Bash 執行。NTFS 無法用 `ls -l` 證明 `0600`，因此 Windows 只允許該單一斷言明確 skip；Linux CI 仍須完整通過，沒有平台豁免。

## 2026-08-24：不建立 Python 套件

維護工具只使用 Python 標準庫與 `gh`，不新增 `pyproject.toml`、requirements 或 lockfile。repo 的交付物是 Agent Skills，不是 Python library。

## 2026-08-24：upstream 水位分離

commit、PR、issue 與 branch head 分別記錄。Baseline 表示已審查，不表示已合併；每次只處理水位之後的新狀態，避免重複成本與標題式判斷。
