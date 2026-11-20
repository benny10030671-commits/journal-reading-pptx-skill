# 原文圖片與圖表處理

## 來源優先順序

1. 使用者提供的主論文與 supplement。
2. 同一篇的正式 publisher figure／高解析原檔，核對版本與 caption。
3. 必要背景或機轉的其他論文，取得並讀到原圖後明確引用。

參考簡報中的圖片只能作尋找原文的線索。論文找不到、圖片來源不明、只有抽象描述時，不生成替代圖，也不擷取無關搜尋結果。可以先完成文字與其他可核實頁面，並精準列出欠缺的來源。

原文沒有圖，不代表必須加圖。文字與公式可以直接解釋。paper 中已有的 schematic 也屬原圖；自行重建同樣 schematic 仍不是原圖，也不取代它。學術單位標誌、裝飾背景、病人照片及現成 AI 示意圖不因出現在參考 deck 而取得沿用許可。

報告者自繪的可編輯示意圖是另一類物件，不是原圖。它只用於研究設計、時間軸、流程與概念關係這類非數據內容，而且只在論文沒有合適的圖時使用；規則見 [slide_patterns.md](../slide_patterns.md) 的「可編輯示意圖」。研究結果的圖表仍只來自上面的來源。

## 圖表清單

每個候選 exhibit 記錄 source ID、正式圖／表號、panel、PDF 實際頁次、印刷頁碼、caption、教學問題、預定 slide、所需裁切、來源註記及使用限制。

全文 PDF 頁次、期刊頁碼、supplement 目錄標碼不可混用。protocol 的預定 figure 編號也可能不同於發表版。依實際 figure caption 核對，不用全文關鍵字第一次命中作定位。

## 擷取流程

先檢視整頁，再裁切。從 PDF 嵌入圖片直接取出時，檢查文字、軸線、legend 是否另存在 vector 或 text layer；不完整就改用整個區域渲染。不要只取 XObject 而遺失標籤。

附帶工具只做擷取，不畫圖：

```bash
python -m pip install -r requirements.txt
python scripts/paper_assets.py index paper.pdf --output work/paper-index.json
python scripts/paper_assets.py render paper.pdf --page 6 --output work/page6.png
python scripts/paper_assets.py crop paper.pdf --page 6 --bbox X0 Y0 X1 Y1 --dpi 300 --label "Figure 1" --citation "Author et al. Journal. Year. DOI" --source-id main --output work/figure1.png
python scripts/paper_assets.py verify work/figure1.png.json --pdf paper.pdf
```

`X0 Y0 X1 Y1` 需從**這份 PDF 的實際頁面**取得，不直接複用示例數值。單位是 PDF point（72 point = 1 inch），原點左上，與 `index` 輸出的文字座標同系統。頁次從 1 開始。工具會為每頁旋轉到正常方向，再使用該頁顯示座標，處理方式會記入 metadata。

`render` 只提供定位預覽，不是已認證的論文 figure。`crop` 會輸出 PNG 及相鄰 `.png.json`，包含來源檔雜湊、圖片雜湊、頁次、裁切區、DPI、圖表標籤與引用。它不會自動找圖，也不會判斷輸入的 citation 是否正確。

## 保留原貌

- 保留 panel 字母、座標軸、單位、圖例、color scale、null line、CI／error bar、risk table 與解讀必需的 footnote。
- 完整圖太密時分頁裁切，避免縮到無法讀。裁切列必須帶欄名，拆 panel 必須保留辨識資訊；legend 若另置，仍須能同頁辨讀。
- 保持比例。不要非等比拉伸、改色、移動數據點、改 CI 或刪掉不利結果。不能用 generative fill 或 AI upscale 補不存在的細節。
- 允許透明重點框、箭頭或文字說明，但保持原圖檔完整，標註放在簡報獨立圖層。文字不能暗示圖中沒有的顯著性或因果關係。
- 對掃描來源，OCR 僅協助找文字，最終證據仍是原圖。解析度不足時找正式原檔、放大局部或說明限制。

## 引用與去向

每張圖旁或頁腳列「Author, journal, year, Fig./Table/panel」，完整引用與 DOI 放 references，詳細定位可放 notes。多來源頁分別標來源，不用一個模糊頁腳涵蓋所有圖片。

工作用 figure ledger 把每張 slide 的每個圖片對到來源與裁切紀錄；報告者示意圖另標類別，記下依據的來源與頁碼。交付前逐一核對實際使用的圖片與 ledger，包含封面、背景、master 和隱藏頁；引用存在不代表圖片內容已核實。

paper 的授權與軟體 MIT 授權分開處理。引用不自動等於公開散布許可。除非另有授權，不把使用者論文、原簡報、抽出的 figures、病人照片或 notes 隨 skill 發到公開 repository。保留製作規則與必要的書目／圖號對照即可。
