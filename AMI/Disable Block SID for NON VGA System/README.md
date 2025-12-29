# Disable Block SID of NON VGA System

## 測試條件與現象

- 硬體條件 : J103 [NON BMC VGA] + BIOS XL01
- 在遠端畫面觀察到，AMI signon string晚於F10 message出現。(參考底下測試畫面)<br>
  > 補述: <br>
  > 從遠端畫面上看到POST code 0x92，但未看到任何字串。<br>
  > 須按壓ESC key，畫面重整後，才會看到先看到F10 message，再看到AMI signon string。<br>
- Remote console端按壓F10**沒有作用**。<br>
- Local端按壓F10**行為正常**。<br>

**測試畫面**<br>
![PASS_FAIL](./Pics/螢幕擷取畫面%202025-12-29%20105033.png)

<br>
按壓ESC重整畫面後，訊息可以出現<br>

![PASS_FAIL](./Pics/螢幕擷取畫面%202025-12-29%20105213.png)

<br>

## 靈魂拷問系列

## 拷問一 : F202測試結果+J103 [BMC VGA]<br>

<br>

|        | Console 畫面  | Console 按壓 F10 | Local 按壓 F10 |
|  ----  | ------------- | -------------- | ------------- |
| Result | AMI signon 訊息先出現，再出現F10| 進setup | System reset|

<br>

**測試畫面**<br>
![PASS_FAIL](./Pics/螢幕擷取畫面%202025-12-29%20094714.png)

## 拷問二 : XL01測試結果+J103 [BMC VGA]<br>

<br>

|        | Console 畫面  | Console 按壓 F10 | Local 按壓 F10 |
|  ----  | ------------- | -------------- | ------------- |
| Result | AMI signon 訊息先出現，再出現F10| 進setup | System reset|

<br>

![PASS_FAIL](./Pics/螢幕擷取畫面%202025-12-29%20111212.png)

<br>

結論:<br>
1. Console端按壓F10無效，是因直接按F10 hot key，遠端會送出ESC給系統端的serial buffer，所以按第一次會看到畫面重整，第二次會進BIOS setup；遠端使用者必須想辦法送出正確F10 hot key給系統端的serial buffer。<br>
2. AMI signon訊息與F10訊息出現順序和XL01不一致，和J103設定有關(參考拷問二)。<br>


## 解決方式1 : 使用refresh來刷新putty畫面

測試結果: 失敗<br>
Compile不過

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

## 解決方式2：在 HandleSIDPpi() 加入 gST->ConOut->ClearScreen (gST->ConOut)

測試結果: 失敗<br>
現象: POST code 0x92以後，遠端畫面清空，但訊息沒有出現。<br>
