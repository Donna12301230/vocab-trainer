# 單字練習

背單字的小網頁：閃卡、標記不熟的字、每天 10 個今日複習、考試、英文發音。手機和電腦都能用，不需要安裝。

**網址：https://donna12301230.github.io/vocab-trainer/**

## 功能

- **閃卡**：點一下翻面，按「不熟」或「記得」。一輪結束可以只重練不熟的字，直到全部記得。
- **不熟清單**：閃卡按「不熟」或考試答錯的字會自動加進來，在閃卡按「記得」就會移出。
- **今日複習**：每天從不熟清單挑 10 個（優先挑最久沒複習、錯最多次的），首頁會顯示進度和連續天數。
- **考試**：看英文選中文、看中文選英文、聽發音選中文、看中文拼英文，或混合出題。
- **發音**：使用瀏覽器內建的英文語音（電腦用 Edge 聲音最自然）。
- **多個單字庫**：在「切換／新增單字庫」頁面貼上單字表（可以直接從 Excel 複製），或選 CSV／文字檔。

## 資料存在哪裡

| 資料 | 存放位置 |
| --- | --- |
| 內建單字庫（TSL 多益 1250） | 這個 repo 的 `data/` 資料夾，打包在網頁裡 |
| 自己新增的單字庫、學習進度 | 你當下使用的瀏覽器裡（localStorage），不會上傳 |

手機和電腦的進度不會自動同步。要換裝置時，到「設定 → 匯出進度」存成檔案，再到另一台「匯入進度」。

## 新增內建單字庫（給維護者）

一般使用者直接在網頁上新增單字庫就好。如果想讓單字庫內建在網頁裡（所有裝置都看得到）：

1. 在 `data/` 新增一個 JSON 檔，例如 `02_phrases.json`，格式寫在 `tools/build.py` 開頭的說明裡。
2. 執行 `python tools/build.py`，會重新產生 `index.html`。
3. commit 並 push，GitHub Pages 約一分鐘後更新。

網頁程式在 `src/template.html`，改完一樣要執行 `tools/build.py`。

## 授權

TSL 單字資料來自 Browne, C. & Culligan, B., *The TOEIC Service List 1.2*（[newgeneralservicelist.com](https://www.newgeneralservicelist.com/)），採 [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) 授權；中文翻譯與詞性為自行補充，同樣以 CC BY-SA 4.0 分享。
