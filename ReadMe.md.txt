Python 3.8 安裝
	1.至https://www.python.org/downloads/release/python-380/ 下載mac版本
	2.執行下載的檔案，全部按continue
	3.執行terminal，輸入以下指令
	4.依照此篇文章設定環境變數 http://blog.ctrlxctrlv.net/mac-environment-path/
		a.vi ~/.bash_profile
		b.修改這一行 export PATH=$PATH:/Library/Frameworks/Python.framework/Versions/3.8/bin
		c.按esc,輸入:wq儲存
		4.在terminal輸入source ~/.bash_profile並執行


Enviroment: Python 3.5以上

Package:
	1.os
	2.zipfile
	3.chardet
	4.codecs
	5.sys
	6.shutil
	7.re
	8.hanziconv
	9.easygui
	10.mimetypes
	11.io
	12.tkinter

套件安裝command:
	pip3 install -r PackageInstall.txt

程式執行:
	python3 FileConvert.py

Note:
	1.對話框内輸入要轉的folder位置(絕對路徑)
	2.勾選選擇需要執行的功能
	2.若有轉編碼或轉繁體，會Backup所有檔案，新檔案名稱會加上postfix: _backup
	3.以防萬一，還有zip的備份
	4.最後會顯示哪些檔案轉檔失敗

若檔案不慎損毀 可至github重新下載：
https://github.com/Nickie-Li/FileConvert