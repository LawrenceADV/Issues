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

## Investigation

## AMITSE

BIOS在Disable Block SID [enable]後，會透過AMITSE提供的服務往螢幕與console端丟訊息!

"DisplayPostMessage"會判斷"stPostScreenActive"，決定文字面能否往螢幕與console端丟。

```cpp
    pAmiPostMgr->DisplayPostMessage( String );
```

PrintPostMessage (AmiTsePkg\EDK\MiniSetup\BootOnly\string.c)
```cpp
	if(stPostScreenActive)
	{
		FlushLines(stStartLine,stNextLine+LineCount);
		DoRealFlushLines();
        MouseRefresh();
	}
```

<br>

|                      | ConOut             | NO ConOut |
| :-----------------   | :-------------: | :--------------:
| BDS.ConnectVgaConOut | V    | 
| BDS.HandoffToTse     |      |   V



PS: 打V表示<br>
1. stPostScreenActive被設為1。<br>
2. gPostStatus被設為TSE_POST_STATUS_BEFORE_POST_SCREEN。<br>


<br>

## Root cause
"stPostScreenActive"的設定在ConOut vs NO ConOut的環境下，有設定時序的差異。

在NON-VGA環境下，AMITSE會在POST快結束時才將gPostStatus設為"TSE_POST_STATUS_BEFORE_POST_SCREEN"並且設定<br>
"stPostScreenActive"為1，當此條件滿足後，使用pAmiPostMgr->DisplayPostMessage()服務的文字，才能從console端輸出。<br>
相較於VGA環境，AMITSE在VGA driver start後，就會打開"stPostScreenActive"為1，pAmiPostMgr->DisplayPostMessage()就會啟動。<br>

## AMITSE的本意?
為什麼NON-VGA環境下，AMITSE會在POST快結束時才將"stPostScreenActive"設為1?<br>

推測是為了照顧到console redirection function，才將此flag設起來。


## 解決方式

NON-VGA環境下又要使用remote console丟字串，應該使用EDKII的服務。<br>

```cpp
gST->ConOut->OutputString(gST->ConOut, String);
```

MdePkg\Include\Uefi\UefiSpec.h<br>

```cpp
  ///
  /// A pointer to the EFI_SIMPLE_TEXT_OUTPUT_PROTOCOL interface
  /// that is associated with ConsoleOutHandle.
  ///
  EFI_SIMPLE_TEXT_OUTPUT_PROTOCOL    *ConOut;
```
MdePkg\Include\Protocol\SimpleTextOut.h<br>

```cpp
EFI_TEXT_STRING                 OutputString;
```
<br>

## 測試紀錄

## 1. F202測試結果+J103 [BMC VGA]<br>

<br>

|        | Console 畫面  | Console 按壓 F10 | Local 按壓 F10 |
|  ----  | ------------- | -------------- | ------------- |
| Result | AMI signon 訊息先出現，再出現F10| 進setup | System reset|

<br>

**測試畫面**<br>
![PASS_FAIL](./Pics/螢幕擷取畫面%202025-12-29%20094714.png)

## 2. XL01測試結果+J103 [BMC VGA]<br>

<br>

|        | Console 畫面  | Console 按壓 F10 | Local 按壓 F10 |
|  ----  | ------------- | -------------- | ------------- |
| Result | AMI signon 訊息先出現，再出現F10| 進setup | System reset|

<br>

![PASS_FAIL](./Pics/螢幕擷取畫面%202025-12-29%20111212.png)

<br>

結論:<br>
1. Console端按壓F10無效，是因直接按F10 hot key，遠端會送出ESC給系統端的serial buffer，所以按第一次會看到畫面重整，第二次會進BIOS setup；遠端使用者必須想辦法送出正確F10 hot key給系統端的serial buffer。<br>
2. AMI signon訊息與F10訊息出現順序和XL01不一致，且不會主動出現，此現象和是否有VGA device有關。(測試2)<br>

## 3. 為什麼系統有無VGA會影響remote端AMI signon和F10 message的行為?

已知: <br>
> AMI signon由commonoem.c輸出

<br>

### Debug message (XL01 debug log)

\\\biosserver.advantech.corp\upload\Lawrence.Guan\5993\debug\log\
> putty_XL01_VGA.log<br>
> putty_XL01_NON_VGA_NO_ESC.log<br>
> putty_XL01_NON_VGA_WITH_ESC.log<br>
> TSE debug\putty_NON_VGA_TSE.log<br>
> TSE debug\putty_VGA_TSE.log<br>

## Something need to know

1. pAmiPostMgr服務何時啟動?<br>
2. 為何上述現象，在按壓ESC重整畫面後，訊息可以出現?<br>