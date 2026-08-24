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
