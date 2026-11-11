# 範例到製作規則的推導

這是本 skill 的設計依據，不是新的臨床 guideline。原檔由使用者於 2026-11-11 提供；本 repository 只保存歸納、書目與定位，不附原文、原簡報、圖片、報告者資料或 notes。

## 1. 觀察範圍

五份簡報合計 274 張／PDF 頁。PPTX 數字是原始 slide index（包含 hidden slide）；PDF 數字是檔案的實際頁次，不是頁面印出的頁碼。

| 參考簡報 | 長度與格式 | 實際呈現的教學結構 |
|---|---|---|
| `20250107 Journal Reading.pptx` | 65 slides，16:9，Aptos theme | s2–6 臨床試驗挑戰；s7–14 Bayesian 與 interim analysis 先備概念；s15–43 分類解釋 adaptive 方法；s44–59 以 ASTIN、SWIFT PRIME、DAWN、ENRICH 回扣方法；s60–65 限制與 take-home |
| `Journal-club-20260609-Large-core-EVT.pptx` | 36 slides，16:9，Cambria theme；s12 hidden | s1–5 論文身分、預覽與背景；s6–13 方法與跨 trial 比較；s14–16 研究族群；s17–21 主要、次要、安全性；s22–30 亞組與敏感度；s31–35 討論、限制與總結；s36 致謝 |
| `Journal-Club-0922_DoC-and-the-CRS-R.pdf` | 64 PDF 頁，16:9 | p2 學習目標；p3–14 構念、分類與舊工具限制；p15–27 結構與施測前提；p28–50 分項示範；p51–58 評分有效性與診斷整合；p59–62 限制與 FAQ；p63 回訪目標；p64 參考資源 |
| `20250610 Impaired Consciousness and Automatisms in Temporal Lobe Seizure.pdf` | 58 PDF 頁，16:9 | p2–7 臨床現象；p8–14 定義與 network hypothesis；p15–32 第一篇原始研究帶讀；p33–36 機轉整合與下一題；p37–49 其他研究回答 hand／oroalimentary automatisms；p50–57 整合與回到問題；p58 致謝 |
| `20240514 Journal reading - re1.pdf` | 51 PDF 頁，16:9 | p2 outline；p3–4 臨床缺口；p5–8 方法；p9–20 分母、診斷分布與 WGS 新增貢獻；p21–39 漏診機制與 illustrative cases；p40–49 資源、外推與剩餘缺口；p50 結論；p51 致謝 |

隱藏頁處理實例：ATLAS 的 s12 是另一份 trial 比較表。預設 PowerPoint PDF 匯出略過它，得到 35 頁，因此從該處開始 PDF 頁次不等於 slide index。歸納時另外查看原始 hidden slide，未把 35 頁誤當成全 deck。

## 2. 可重用的教學動作

| 觀察到的動作 | 範例定位 | 轉成 skill 的規則 |
|---|---|---|
| 先教讀圖需要的概念 | Adaptive s7–14；seizure p8–14；CRS-R p3–17 | 插入必要的定義與方法橋接，教完立即回到 evidence |
| 臨床問題引導研究閱讀 | CMT p3–8；ATLAS s4–9 | 開場交代缺口，再介紹研究問題與設計 |
| 全圖、局部與標註連續帶讀 | Seizure p16–18、p19–22、p23–28；ATLAS s22–24 | 同一原圖可重用、裁 panel 放大，不強制一圖只出現一次 |
| 先整體，再解釋特定群體／例外 | CMT p9–20 後接 p21–39；ATLAS s17–21 後接 s22–30 | 先主要結果，後亞組與機制，不讓探索性結果搶走主結論 |
| 原表分區，逐次增加解釋 | CRS-R p28–37、p38–45、p52–56 | 固定定位的逐步揭露，讓單項反應連回分類 |
| 概念後用真實論文檢驗 | Adaptive s44–59；seizure p15、p37、p44 | 每個案例交代設計、原文證據、能回答與不能回答的部分 |
| 數字必須與分母一起教 | CMT p17–20；ATLAS s16–18 | 區分整體診斷率、新增 yield、特定檢查 cohort；區分總 N 與 outcome N |
| 區段小結與最後回答開場 | Adaptive s29、37、41、64–65；seizure p32、43、49、56–57；CRS-R p63 | 單元結束停一下，再接下一個問題，最後對回目的 |
| 臨床意義含邊界 | CMT p41–49；ATLAS s33–35；CRS-R p59–62 | 結論同時說適用對象、限制與未解問題 |

## 3. 論文與範例的配對程度

| 提供的來源 | 可核實內容與角色 | 不能假定的部分 |
|---|---|---|
| Reeves et al. 2024, *Changing Landscape of Randomized Clinical Trials in Stroke*, DOI `10.1161/STROKEAHA.124.046129`，5 頁 | 系列導論，對應 adaptive deck 開場與整體背景 | deck s15 起另引 *Adaptive Clinical Trials in Stroke*，並引其他方法與 trial；不能把它們全算成這篇 5 頁導論的內容或圖片 |
| `1-s2.0-S0140673626008767-main.pdf`，12 頁 | Sarraj et al. ATLAS 主文；對應 large-core EVT deck | deck 含自行製作的示意圖片與摘要圖，不能當作主文原圖 |
| `1-s2.0-S0140673626008767-mmc1.pdf`，115 頁 | ATLAS supplement，含計畫／SAP、trial 表格、流程、trial-level 與探索分析 | 目錄／印刷頁碼相對實際 PDF 頁次有偏移；計畫中的圖號不等於發表圖號 |
| `awae064.pdf`，13 頁 | Record et al. 2024, *Whole genome sequencing increases the diagnostic rate in Charcot-Marie-Tooth disease*, DOI `10.1093/brain/awae064`；對應 CMT deck | 簡報使用的舊版圖面與正式版可能外觀不同，需核對 caption 與版本 |
| `awae064_supplementary_data.zip` | `brain-2023-02335-File008.xlsx` 含 Whole cohort、CMT1、CMT2、CMTi、HMN、HSN、SAN、Complex；`File009.pdf` 是 2 頁診斷率／遺傳型態補充圖表 | 補充資料需先盤點內容，不能只處理主 PDF |
| `1-s2.0-S2590109526000856-main.pdf`，10 頁 | Penrod et al., *Disorders of Consciousness in Acute Care: Application of the CRS-R and Respiratory, Swallowing, and Discharge Outcomes at a Level 1 Trauma Hospital*，是 acute-care cohort 應用來源 | CRS-R 教學 deck 引用 Bodien、Fischer & Edlow 等文獻與其他資源，這篇 cohort 不是該 deck 所有評分細則與圖片的單一來源 |
| Seizure 與 CRS-R deck 內其他引用 | 提供尋找原始文獻的線索 | 未提供的原論文／原圖不能宣稱已核實；僅能從 deck 歸納教學順序 |

## 4. 兩個具體「論文 → 投影片」對照

### CMT：從整體診斷到漏診原因

| 原文證據（實際 PDF 頁次） | 範例用法 | 重用的製作邏輯 |
|---|---|---|
| p3 Fig. 1 testing algorithm | deck p8 | 先理解 testing pathway，後面才知道新增診斷從哪來 |
| p3 Fig. 2 phenotype distribution；p4 Fig. 3A solved rate | deck p9–10 | 先看樣本組成，再看各 phenotype 的結果 |
| p5 Fig. 4 各 panel | deck p12–16 | 分別解釋 phenotype 與 testing method，不把整張密集圖縮小塞一頁 |
| p4 Fig. 3B 100KGP 結果 | deck p19–20 | 先全貌再標明不同分母與真正來自 WGS 的貢獻 |
| p7 Fig. 5B–E 與 5A | deck p23–24 | 臨床表型／影像後接檢測證據，再解釋漏診原因 |
| p7 Fig. 5G–J 與 5K | deck p35–36 | 外表／功能和分子證據分頁，最後回到家族判讀 |

具體核對提醒：CMT deck p30 的某個 variant 寫作 `PMP22`，對應正式論文 p7 寫作 `PMP2`。這個差異說明「學教法」與「核實醫學內容」必須分開，不能把原簡報當無誤的資料表。本 skill 未對所有舊投影片做完整醫學正誤審查。

### ATLAS：從 trial 差異到主要結果與不確定性

| 原文證據（實際 PDF 頁次） | 範例用法 | 重用的製作邏輯 |
|---|---|---|
| Supplement p28–29，Table 1 | deck s10–11 | 原表分兩頁解釋 eligibility 與 trial outcomes |
| Main p5，Table 1 | deck s16 | baseline 原表加影響外推的少數觀察 |
| Main p6，Figure 1 與 Table 2 | deck s17–21 | functional shift、secondary outcomes、safety 依序解讀 |
| Main p7，Figure 2 | deck s22–24 | 大型 forest plot 分區，再聚焦不確定的 subgroup |
| Supplement p73，Figure 6 | deck s29 上方 | 將探索分析標明，不和主要分析混為同等證據 |

ATLAS deck s17 圖下編號與提供的主文 caption 不一致；新簡報使用實際主文的 Figure 1，不複製舊圖號。原 deck 的 s4–5、s15、s19、s25–28、s30 含示意／重製成分，不列入本 skill 可直接沿用的原圖資產。

## 5. 與原 academic-pptx 的差異

來源：[Gabberflast/academic-pptx-skill](https://github.com/Gabberflast/academic-pptx-skill)，基準 commit `9f2b703ffe8d1449851617665ab1ffb3516d54ac`。

| 原版規則 | 本版處理與原因 |
|---|---|
| 所有學術簡報使用同一論證導向流程 | 改成三種 journal reading 路徑，符合五份範例的不同用途 |
| 每頁必須是完整結論句 | 改成依頁面角色使用主題、問題或有證據的 takeaway |
| 不直接複製 PDF 圖，要重畫 | 改為原文圖表優先的強限制，直接符合使用者要求 |
| 結果固定圖左字右、一頁一圖 | 改為一頁一個教學問題，可全頁原圖、相關 panel 對照、連續放大 |
| 方法限一到兩頁、正文約 40 字 | 改依理解需求與可讀性調整，不犧牲必要方法與定義 |
| 超過十頁必須先核准大綱 | 保留規劃，移除無條件的等待關卡 |
| 固定 sans-serif、禁止致謝、必須聯絡資訊／QR | 尊重參考樣式與當次需求，移除無關通用限制 |
| 依賴指定 PPTX skill 路徑與工具 | 改使用實際可用的簡報實作能力，本 skill 專注內容與證據 |

保留：先規劃再製作、每頁有用途、來源註記、閱讀負擔控制、實際渲染與修正。修改：以 journal reading 的理解順序和原文證據取代泛用 conference pitch 規則。

## 6. 使用者指定的固定頁面：Graphical Abstract

2026-11-11 使用者另外指定：每份簡報在 Take-home message 之前固定加一頁 Graphical Abstract，以 AJKD 的 visual abstract 為版型。這條**不是**從五份範例歸納的，所以獨立記在這裡。

| 項目 | 處理 |
|---|---|
| 版型依據 | 使用者提供的一張 AJKD visual abstract（Ruggenenti et al.，DOI `10.1053/j.ajkd.2023.10.013`）。量測其標題區、欄名色帶、三欄寬度、CONCLUSION 框、頁尾色帶的比例與色碼，換算成 16:9 座標，並實際排版渲染確認 |
| 與原圖規則的關係 | 版面框架是可編輯物件；Results 欄仍只用原圖／原表裁切。AJKD 官方版會重繪圖表與加圖示，本 skill 不跟 |
| 不放 logo 的理由 | 這頁由報告者製作。貼上期刊 logo 或社群帳號會被誤認為期刊官方產物，也涉及第三方商標 |
| 與 Take-home 的分工 | Graphical Abstract 呈現作者層次的設計、結果與結論；Take-home 呈現報告者的評讀。延續「作者結論、實際結果、報告者評讀」分開的原則 |

該參考圖未放入 repository。完整規格見 [graphical_abstract.md](graphical_abstract.md)。
