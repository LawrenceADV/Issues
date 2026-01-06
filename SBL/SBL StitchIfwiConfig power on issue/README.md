# SBL StitchIfwiConfig power on issue

## Root caused

原始設定如下，此設定無法開機

```python
('./FlashSettings/FlashConfiguration/QuadOutReadEnable',             'Yes'),
('./FlashSettings/FlashConfiguration/QuadIoReadEnable',              'Yes'),
```

修改成如下設定可以開機

```python
('./FlashSettings/FlashConfiguration/QuadOutReadEnable',             'No'),
('./FlashSettings/FlashConfiguration/QuadIoReadEnable',              'No'),
```

PS:
同時或單獨槓掉這兩個設定也都可以開機，避免設定為floating，所以設定一固定值'No'

```python
#// ('./FlashSettings/FlashConfiguration/QuadOutReadEnable',         'No'),
#// ('./FlashSettings/FlashConfiguration/QuadIoReadEnable',          'No'),
```

## SPI flash 能否支援 QUAD mode?

## 在COM-HPC設計下，上板 SPI flash，與下版 SPI flash 周邊pin腳設計與用途會有不同 嗎? (以專案為例)