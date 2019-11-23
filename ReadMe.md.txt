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

套件安裝command:
	pip install -r PackageInstall.txt

程式執行:
	python FileConvert.py

Note:
	1.對話框内輸入要轉的folder位置(絕對路徑)
	2.會自動Backup所有檔案，新檔案名稱會加上postfix: _backup
	3.以防萬一，還有zip的備份
	4.最後會顯示哪些檔案轉檔失敗

若檔案不慎損毀 可至github重新下載：
https://github.com/Nickie-Li/FileConvert