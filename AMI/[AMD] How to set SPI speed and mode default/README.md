# [AMD] How to set SPI speed and mode default

PSP phase

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