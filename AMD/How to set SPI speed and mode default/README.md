# How to set SPI speed and mode default

**Platform: AMD SIENA**

**1. Modify the PSP EFS table**

**Chapter 3.4.16 (58289_1.20_NDA.pdf)**

***PSP firmware 
will configure SPI ReadMode and FastSpeed if the data of EFS offset 0x47/0x48/0x49 are valid 
values.***

Q: 什麼叫做Valid values?<br>

spec的定義是**符合AMD datasheet定義的SpiReadMode/SpiFastSpeed值**否則"do nothing"<br>

![PASS_FAIL](./Pics/offset_47_48.jpg)

BIOS 的設定 token如下，default全為0xFF為do nothing的設定。
```cpp
TOKEN
    Name  = "SPI_MODE"
    Value  = "0xFFFFFFFF"
    Help  = "Byte3 (EFS offset 0x47) for SPI Mode"
    TokenType = Integer
    TargetEQU = Yes
    TargetMAK = Yes
    TargetH = Yes
End

TOKEN
    Name  = "SPI_SPEED"
    Value  = "0xFFFFFFFF"
    Help  = "Byte0 (EFS offset 0x48) for SPI Speed, Byte1 (EFS offset 0x49) for MicroDetectFlag"
    TokenType = Integer
    TargetEQU = Yes
    TargetMAK = Yes
    TargetH = Yes
End
```

Binary<br>

參考 Doc#57299 - AMD Platform Security 
Processor BIOS 
Implementation Guide for 
Server EPYC Processors<br>

- 0x55AA55AA是PSP用來識別EFS table的signature
- Family 19h Models 10h–1Fh onward: **Only one EFS is supported. It is at offset 0x20000.**
- PcdResetMode和PcdResetFastSpeed不用理會?<br>
From Chapter 3.4.16 (58289_1.20_NDA.pdf) :<br>
There are two PCD tokens related with SPI ReadMode and FastSpeedNew settings.<br> 
FCH code will not consume these tokens to configure SPI in PEI phase to avoid FCH override 
PSP firmware settings.<br>
gEfiAmdAgesaModulePkgTokenSpaceGuid.PcdResetMode<br>
gEfiAmdAgesaModulePkgTokenSpaceGuid.PcdResetFastSpeed<br>

![PASS_FAIL](./Pics/binary.jpg)

<br>
<br>

**2. 進入BIOS**

The SPI configuration registers are accessed through SPI base address specified by 
**FCH::LPCPCICFG::SPI_BASE_ADDR**.<br>

![PASS_FAIL](./Pics/螢幕擷取畫面%202026-01-06%20232240.jpg)

<br>
<br>
<br>
<br>

Change Rom Read mode/Speed:
1. Rom read is handled by old Spi engine first which running 16.7M without prefetch enabled.
2. Program FCH::LPCHOSTSPIREG::SPI_CNTRL0_REGISTER to set up Read mode.
3. Program dummy cycle in FCH::LPCHOSTSPIREG::SPI100_DUMMY_CYCLE_CONFIG_REGISTER to match
the dummy cycle number of SPI Rom.
4. Program speed for all operations in FCH::LPCHOSTSPIREG::SPI100ENABLE_REGISTER.
5. Program UseSpi100 to 1 in FCH::LPCHOSTSPIREG::SPI100ENABLE_REGISTER.
6. Program PrefetchEnSPIFromHost in FCH::LPCPCICFG::HOSTCONTROL to enable read prefetch.


BIOS會在 
1. PEI設定SPI speed
 FCH::LPCHOSTSPIREG::SPI100ENABLE_REGISTER
0x11310713

Lawrence::: FchInitResetSpi 116
AGESA_TP:[B000AF43]
Lawrence::: SPI_BASE=FEC10000
Lawrence::: REG22 SpiSpeed=1131
Lawrence::: REG20 WriteSpeed=713
Lawrence::: LocalCfgPtr->SpiTpmSpeed=0
Lawrence::: FchInitResetSpi 189
把new SPI100 speed設為33.33

#new SPI100 engine.
#old SPI100 engine.

Q: what's SPI100 engine? new vs old?

2. DxeSmmReadyToLockRaCallback，將SPI mmio configuration space鎖上

```
--- SPI_Flash_Ready_To_Lock callback ---
--- Spi settings start(89) ---
00 20 C8 0F 00 00 00 00 00 00 00 00 00 03 00 02 
00 01 00 00 B2 E2 00 00 03 0B 0A 02 00 98 00 00 
13 07 31 11 08 20 20 20 0C 14 06 0E C0 54 00 80 
C0 14 08 46 03 00 00 00 FC FC FC FC FC 88 00 00 
3B 6B BB EB 00 05 00 00 01 00 00 02 03 03 01 00 
01 12 13 0C 3C 6C BC EC 08 46 00 00 03 00 00 00 
00 00 00 00 FD 00 00 00 00 00 00 00 04 32 00 00 
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
00 00 00 F6 56 41 52 69 6D 75 6D 54 61 62 6C 65 
53 69 7A 65 00 04 43 72 61 74 63 68 42 75 66 66 
65 72 00 18 60 48 A5 00 00 00 00 00 00 00 00 00 
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
00 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00 
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
00 00 00 00 00 00 00 00 00 00 00 00 10 00 00 00 
--- Spi settings end ---

Installing R/A communication protocol
SmmInstallProtocolInterface: 346B138A-D825-4AC0-B919-46169ABADD4D ACD6B218
--- Spi settings start(Success 204) ---
FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 
FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 
FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 
FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 
FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 
FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 
FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 
FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 
FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 
FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 
FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 
FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 
FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 
FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 
FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 
FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 
--- Spi settings end ---
```