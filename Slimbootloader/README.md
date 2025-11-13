# Slim Bootloader 如何從 C code 找到 Platform Specific Configure Data？
## 以 SPD Data 為例，會透過 CDATA_MEMORY_TAG 取得記憶體設定資料：
C// 取得 Memory Configuration DataMEMORY_CFG_DATA *MemCfgData;MemCfgData = (MEMORY_CFG_DATA *)FindConfigDataByTag(CDATA_MEMORY_TAG);顯示更多行

## Memory Configure Data 會依什麼條件取得？

## 條件：
Platform ID + CDATA_MEMORY_TAG

## 對應的設定檔路徑範例：


Platform\RaptorlakeBoardPkg\CfgData\CfgDataInt_Rplp_Rvp_Ddr5_SOM_6884A2.dlt

