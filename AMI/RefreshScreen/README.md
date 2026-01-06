# Refresh screen

## 測試1: 在HandleSIDPpi()加入gST->ConOut->ClearScreen(gST->ConOut)<br>

測試結果: 失敗<br>
現象: POST code 0x92以後，遠端畫面清空，但訊息沒有出現。<br>

## 測試2： 使用refresh來刷新putty畫面

測試結果: 尚未測試<br>
編譯中

AmiModulePkg\Terminal\Terminal.sdl<br>
```cpp
TOKEN
    Name  = "REFRESH_SCREEN_KEY"
    Value  = "0x0012"
    Help  = "Unicode Value of Key to Refresh the Screen.Default is set to Ctrl+r"
    TokenType = Integer
    TargetH = Yes
End
```

AmiModulePkg\Terminal\TerminalSimpleTextIn.c <br>

Check the Keyboard Data from Serial Port and Convert them 
into proper Keyboard data. Once the Keyboard data is found added into 
Keyboard Local buffer 
~~~cpp
EFI_STATUS
CheckKeyboardDataFromSerial (
    IN  TERMINAL_DEV *TerminalDev 
)
{
    ...
        // Refresh the Screen if CTRL + R or CTRL+ r key comes
    // If UnicodeChar(REFRESH_SCREEN_KEY) is 0, it would disable RefreshScreen functionality
    if((Status== EFI_SUCCESS) && (TerminalKey.Key.UnicodeChar != 0) && (TerminalKey.Key.UnicodeChar == RefreshScreenKey)) {
        RefreshScreen();
        // Don't report the CTRL+R or CTRL+r data.
        return EFI_NOT_READY;
    }
}
~~~
