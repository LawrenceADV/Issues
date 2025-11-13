# Slim Bootloader 如何從 C code 找到 Platform Specific Configure Data？
## 以 SPD Data 為例，會透過 CDATA_MEMORY_TAG 取得記憶體設定資料：
### 取得 Memory Configuration Data
MEMORY_CFG_DATA *MemCfgData;MemCfgData = (MEMORY_CFG_DATA *)FindConfigDataByTag(CDATA_MEMORY_TAG);

## Memory Configure Data 會依什麼條件取得？

## 條件：
Platform ID + CDATA_MEMORY_TAG

## 對應的設定檔路徑範例：


Platform\RaptorlakeBoardPkg\CfgData\CfgDataInt_Rplp_Rvp_Ddr5_SOM_6884A2.dlt


## Test Result

![Test Result 1](Pics/2025-11-13_130353.JPG)

![Test Result 2](Pics/2025-11-13_130553.PNG)


