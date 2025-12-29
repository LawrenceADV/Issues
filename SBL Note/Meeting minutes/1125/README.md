### 11/25 meeting minutes

### 📄 Windows BIOS Capsule Update 系統識別整理

以下是關於 Windows Capsule Update 中 **SMBIOS** 和 **CHIDs** 的關鍵資訊彙整。

#### 摘要
Windows BIOS Capsule Update 機制依賴系統韌體（BIOS/UEFI）提供的 **SMBIOS** 資訊來生成唯一的系統識別碼 **CHIDs**。這些 CHIDs 用於確保 Windows Update 服務能為特定的電腦型號推送正確的韌體更新包。

---

#### 一、核心概念：CHIDs (Computer Hardware IDs)

CHIDs 是一組複合的、分層次的系統識別碼，用於唯一標識一台電腦的**特定型號和配置**。

* **目的：** 供 Windows Update 或 OEM 驅動程式包使用，作為韌體更新的**匹配鍵 (Matching Key)**。
* **生成方式：** Windows 作業系統會讀取系統韌體中的特定 **SMBIOS** 資訊來生成這組 CHIDs。
* **在 Capsule Update 中的作用：** 韌體更新的 `.inf` 檔案中會指定一組 CHIDs；只有當系統的 CHIDs 與之匹配時，更新才會被執行。

---

#### 二、必須正確填充的 SMBIOS 結構

為了生成準確的 CHIDs 並正確識別系統，以下 SMBIOS Types 必須由 BIOS/UEFI 韌體開發者正確填寫：

| SMBIOS Type | 類型名稱 | 必須填寫的關鍵資訊 | 在 CHIDs 中的作用 |
| :--- | :--- | :--- | :--- |
| **Type 0** | BIOS Information | **BIOS 供應商**、**BIOS 版本**。 | 韌體版本匹配、系統穩定性識別。 |
| **Type 1** | System Information | **製造商 (Manufacturer)**、**產品名稱 (Product Name)**、**版本 (Version)**、**SKU**。 | 識別系統型號，是 CHIDs 的核心。 |
| **Type 2** | Baseboard Information | **基板製造商**、**基板產品名稱**。 | 識別主機板層級資訊。 |
| **Type 3** | System Enclosure | **機箱類型 (Type)**。 | 識別系統外形因素 (Form Factor)。 |

---

#### 三、關鍵設定：機箱類型 (Type 3 Enclosure)

| 欄位 | 設定值 | 含義 | 重要性 |
| :--- | :--- | :--- | :--- |
| **Type 3 - 機箱類型** | **`0x03`** (十進制 3) | **Desktop (桌上型電腦)** | 確保 Windows Update 將系統視為桌上型電腦，避免錯誤推送筆記型電腦專用的韌體更新。 |

---

#### 四、更新流程的關鍵環節

1.  **SMBIOS 準備：** 韌體確保 Type 0, 1, 2, 3 欄位準確無誤。
2.  **CHIDs 匹配：** Windows 透過 SMBIOS 資訊生成 CHIDs，並與 Windows Update 上的韌體包進行匹配。
3.  **下載與傳遞：** 匹配成功後，Windows 下載韌體膠囊包 (`.cap`)，並透過 **UEFI ESRT (EFI System Resource Table)** 介面將其傳遞給韌體。
4.  **UEFI 執行：** 系統重啟，UEFI 韌體在引導前執行膠囊更新。

