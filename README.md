# journal-reading-pptx-skill

從五份神經科 journal reading 範例歸納的**論文閱讀與簡報製作邏輯**，不是單一配色或版型模板。

改寫自 [Gabberflast/academic-pptx-skill](https://github.com/Gabberflast/academic-pptx-skill)（基準 commit `9f2b703ffe8d1449851617665ab1ffb3516d54ac`），保留 MIT 授權與原作者聲明。

## 它會怎麼做

1. 配對主文、supplement、相關文獻與參考簡報，先核實來源。
2. 依用途選擇研究導讀、觀念／機轉、臨床工具三種教學路徑。
3. 把研究問題、必要方法、結果與限制整理成證據表，再做逐頁大綱。
4. **使用論文原圖與原表**，以全貌、panel 放大、讀圖與解釋建立理解。
5. 用作者結論、實際證據與報告者評讀三個層次討論，最後回答開場問題。
6. 核對數字、圖表完整性與實際投影片渲染。

預設不使用 AI 圖、素材圖、自製示意圖或重畫 paper 統計圖。找不到合適原圖時用有來源的文字說明，不造圖補位。標題、解讀、來源與重點標註保留可編輯。

## 使用

把本 repository 的內容放在支援 Agent Skills 的環境中，skill 入口為 `SKILL.md`。Codex 的 skill 目錄可命名為 `journal-reading-pptx`；呼叫名稱為 `$journal-reading-pptx`。在其他環境，使用該環境的 skill 載入方式。

例如：

> 使用 $journal-reading-pptx，根據這篇 paper 與 supplement 做 30 分鐘 journal reading。先補足讀懂方法所需的概念，圖片全部用論文原圖，結果要帶我讀圖，再討論限制與臨床適用範圍。投影片英文，口頭講解要點用繁體中文。

或：

> 幫我把這幾篇文獻整理成機轉教學型 journal club。每篇只保留回答共同問題所需的方法與原圖，最後整合它們支持與無法支持的結論。

本 skill 處理內容與製作判斷；PPTX／Google Slides 等實際建立與匯出由使用環境的簡報工具完成，未綁定某一套雲端服務或不存在的固定路徑。

## 檔案

| 檔案 | 功能 |
|---|---|
| [SKILL.md](SKILL.md) | 入口、原圖規則與整體工作流程 |
| [content_guidelines.md](content_guidelines.md) | 三條教學路徑、讀圖、數字與推論 |
| [slide_patterns.md](slide_patterns.md) | 依教學問題選版面、連續帶讀與樣式 |
| [references/derivation.md](references/derivation.md) | 五份範例的頁次對照、來源配對、原版規則的修改理由 |
| [references/paper_figures.md](references/paper_figures.md) | 原圖搜尋、裁切、標註與引用 |
| [references/quality_checks.md](references/quality_checks.md) | 內容、數字、圖片與渲染驗證 |
| [scripts/paper_assets.py](scripts/paper_assets.py) | PDF 索引、預覽、原圖裁切、雜湊與像素驗證 |
| [tests/test_paper_assets.py](tests/test_paper_assets.py) | 擷取工具的功能測試 |
| [tests/scenarios.md](tests/scenarios.md) | 維護時的情境檢查題目 |

## 擷取工具

需要 Python 3.10+ 與 PyMuPDF；只使用文字規則時不必安裝 Python 套件。

```bash
python -m pip install -r requirements.txt
python scripts/paper_assets.py --help
python -m unittest discover -s tests -v
```

詳見 [原圖處理說明](references/paper_figures.md)。工具不自動辨識 figure，不會生成科學圖，也不判定 citation 或醫學內容正確。`verify` 核對來源與圖片雜湊，並重新渲染比對像素；仍須人工／模型視覺核對裁切是否完整與解讀是否正確。座標處理依據 [PyMuPDF Page 文件](https://pymupdf.readthedocs.io/en/latest/page.html#Page.remove_rotation)。

## 來源與授權

歸納使用五份 journal reading，以及 Reeves 2024、ATLAS 主文與補充資料、CMT 主文與補充資料、CRS-R acute-care cohort 等使用者提供的材料。完整配對與缺件界線見 [推導紀錄](references/derivation.md)。這是製作邏輯的整理，沒有宣稱所有範例醫學內容皆正確。

repository 不包含原始論文、原簡報或擷取圖片。MIT 授權僅涵蓋本 repository 的 skill 文件與程式；第三方論文及圖片依其各自授權。
