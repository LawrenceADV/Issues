# How to set SPI speed and mode default

**Platform: AMD SIENA**

**1. Modify the PSP EFS table**

**Chapter 3.4.16 (58289_1.20_NDA.pdf)**

***PSP firmware 
will configure SPI ReadMode and FastSpeed if the data of EFS offset 0x47/0x48/0x49 are valid 
values.***

Q: 什麼叫做Valid values?<br>

spec的定義是符合AMD datasheet定義的SpiReadMode/SpiFastSpeed值否則"do nothing"<br>

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


Change Rom Read mode/Speed:
1. Rom read is handled by old Spi engine first which running 16.7M without prefetch enabled.
2. Program FCH::LPCHOSTSPIREG::SPI_CNTRL0_REGISTER to set up Read mode.
3. Program dummy cycle in FCH::LPCHOSTSPIREG::SPI100_DUMMY_CYCLE_CONFIG_REGISTER to match
the dummy cycle number of SPI Rom.
4. Program speed for all operations in FCH::LPCHOSTSPIREG::SPI100ENABLE_REGISTER.
5. Program UseSpi100 to 1 in FCH::LPCHOSTSPIREG::SPI100ENABLE_REGISTER.
6. Program PrefetchEnSPIFromHost in FCH::LPCPCICFG::HOSTCONTROL to enable read prefetch.
