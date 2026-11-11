# Skill 情境檢查

用這些題目做內容層的 smoke test。它們不是已自動執行的模型評分，也不取代最終 deck 的視覺 QA。原始論文與簡報由測試者提供，本 repository 不附帶。

| 測試要求 | 應觀察的行為 | 失敗訊號 |
|---|---|---|
| 用 ATLAS 主文與 supplement，做含封面與文獻共 12 頁 | 選研究導讀；保留研究問題、方法、baseline、主要結果、安全性、不確定性、結語；總共 12 頁 | 為了章節模板偷偷多加頁；把所有篇幅用在背景；自己重畫 mRS 圖 |
| 用 CMT paper 講「WGS 到底增加什麼」 | 區分整體 cohort、proband、100KGP 與新增 yield；以原圖與原文核對分母 | 把整體診斷率直接當成 WGS 單獨診斷率 |
| 僅給 Reeves 系列導論，要求像 65 頁 adaptive 範例一樣深入 | 從參考 deck 辨識另有來源；繼續做已核實的背景與規劃，精準列缺件 | 聲稱導論含所有 trial figures；生成不存在的 adaptive 示意圖 |
| 用 CRS-R cohort paper 製作量表操作課 | 分清 cohort 應用與原始操作／驗證文獻；需要時找原始文獻，找不到就說明缺件 | 從 cohort 推出全部施測規則；複製範例裡的 AI 病人插圖 |
| 依 seizure 範例製作多篇機轉報告，某篇原圖缺失 | 保留臨床問題與跨篇證據主線；不假造 missing figure；已核實部分繼續 | 每篇摘要互不相關；把相關性寫成已證實的因果機轉 |
| 原圖字很小，但使用者要求都用 paper 圖 | 看完整圖後裁 panel 放大、保留軸線與圖例；引用追蹤到 paper | AI upscale 補字、重畫數據圖、裁掉反例或 CI |
| 提供含 hidden slides 的 PPTX 當參考 | 分清原 slide index 與 PDF 頁次，確認 hidden 內容的角色 | 直接用匯出 PDF 頁次對照原 slide index |
