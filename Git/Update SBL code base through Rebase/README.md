# Update SBL code base through 'Rebase'

### 1.  同步 Advgcipc remote repository

```
git.exe fetch -v --progress -- "origin"
```

```
git.exe pull --progress -v --no-rebase -- "origin"
```

### Result

![CfgDataTool_Export_Help](./Pics/螢幕擷取畫面%202026-02-05%20101410.jpg)

![CfgDataTool_Export_Help](./Pics/螢幕擷取畫面%202026-02-05%20101440.jpg)

![CfgDataTool_Export_Help](./Pics/螢幕擷取畫面%202026-02-05%20101542.jpg)

### 2.  執行 Rebase

#### 條件與目的:

- 目前是 fork + upstream 的架構
- Branch：som-6884a2
- 舊版：1397f56093238ad67b9fb3391242005a39f10b33
- 新版：0576ef337442c2ba5758e6117a05ba03b6116a7b
- upstream 是官方 SBL repository
- fork 是Advgcipc repository
- 在 local 測試升版結果，不用 push 到 origin

#### 切換開發分支
```
git checkout SOM-6884A2
```

#### 建立備份
```
git branch som-6884A2-Backup
```

#### Rebase到要升級的版本
```
git rebase 0576ef337442c2ba5758e6117a05ba03b6116a7b
```

git會從SOM-6884A2一版一版導入(V101 -> V102 -> V103 ...)

會出現以下狀況循環:
- 開始 rebase → 出現衝突 → 解衝突 → git add → git rebase --continue
重複直到 rebase 完成。

#### 執行過程

![CfgDataTool_Export_Help](./Pics/螢幕擷取畫面%202026-02-05%20105928.jpg)

![CfgDataTool_Export_Help](./Pics/螢幕擷取畫面%202026-02-05%20110226.jpg)


選擇 ours vs theirs

![CfgDataTool_Export_Help](./Pics/螢幕擷取畫面%202026-02-05%20111239.jpg)

選擇ours

![CfgDataTool_Export_Help](./Pics/螢幕擷取畫面%202026-02-05%20134115.jpg)


### 3. 探討

#### 為什麼auto merge可以自動解決新版有差異的code?

AI:

在執行 git rebase 過程中，你會看到許多檔案顯示為 Auto-merging。這代表 Git 能夠在沒有人工介入的情況下處理這些差異，原因如下：
1. 非衝突性改動（Non-conflicting changes）： 當你在舊提交（如 V101）修改了 A 檔案，而新底版（Upstream）只修改了 B 檔案，或者兩者雖然修改了同一個檔案但修改的行數（Line number）完全不同且互不干涉時，Git 的合併演算法會自動將兩邊的改動整合在一起。
2. 檔案的新增與保留： 如果新版底版中加入了新的檔案（如 HdaVerbTable.h），或者你的提交中新增了檔案，這些非衝突的檔案改動會自動被帶入新版本中。
3. 策略的針對性： 即使你設定了「選 ours」的策略，這也只會影響到發生衝突（Conflict）的檔案；對於那些沒有衝突的改動，Git 依然會依照正常邏輯自動合併，並保留其他新增的檔案內容


### Final

