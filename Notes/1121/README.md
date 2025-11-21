### 11/21 meeting minutes
1. 用 Slim.bat 環境變數設定
+ 1.1  使用 Windows command line 視窗 (Powershell X)
    -  Step1  slim.bat
    -  Step2  slim.bat -c
    -  Step3  slim.bat -a
    
  1.2  如何自動判別 Visual studio 版本的方式，並帶入對應路徑?
    
  1.3  @chcp 65001 ?
    
2. VBT設定
+ 2.1  MultiVBT使用?
    
+ 2.2  VbtImageId如何對應到Fsp? Fsp如何取用?
    
+ 2.3  DDI setting，重新review HPD/DDC/AUX/DATA/CLK。
    
3. GPE
+ 3.1  CRB 所用的 GPIO 發 GPE，是否有相關 ASL code? Porting 前需要 review，避免 side effect。
    
+ 3.2  6884A2V105_1 預計導入 GPE 設定。
    
4. Slim Bootloader platform override 方法? RaptorlakeBoardPkg vs AlderlakeBoardPkg
    
5. 更新 feature list，下周目標 EC porting/OC# pin porting/Generic IO decode
    