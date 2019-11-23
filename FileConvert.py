#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import zipfile
import chardet
import codecs
import sys
import shutil
import re
from hanziconv import HanziConv
import easygui
import mimetypes
from time import gmtime, strftime


# In[8]:


def backup_to_zip(path):
    fname = "backup" + '_' + strftime("%Y%m%d_%H%M", gmtime()) + '.zip'
    zipf = zipfile.ZipFile(fname, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(path):
        for file in files:
            zipf.write(os.path.join(root, file))
    zipf.close()


# In[3]:


def backup(file):
    name = (".").join(file.split(".")[:-1])
    filetype = file.split(".")[-1]
    shutil.copy(file, name + "_backup." + filetype)


# In[4]:


def convert_encoding_to_utf_8(filename):
    global total_cnt,success_cnt

    content = codecs.open(filename, 'rb').read()
    source_encoding = chardet.detect(content)['encoding']
    total_cnt+=1
    
    if source_encoding != 'utf-8' and source_encoding != 'UTF-8-SIG':
        content = content.decode(source_encoding, 'ignore') #.encode(source_encoding)
    content = HanziConv.toTraditional(content)
    os.remove(filename)
    filename = HanziConv.toTraditional(filename)
    with open(filename, 'w', encoding='UTF-8-SIG') as file:
        file.write(content)
    success_cnt+=1


# In[5]:


def convert_dir(root_dir):
    if os.path.exists(root_dir) == False:
        print("[error] dir:",root_dir,"do not exit")
        return
    print("work in", root_dir)
    for root, dirs, files in os.walk(root_dir):
        for f in files:
            filename = os.path.join(root, f)
            backup(filename)
            try:
                convert_encoding_to_utf_8(filename)
            except:
                print("Fail Convert",filename)
    print("finish total:",total_cnt,"success:",success_cnt)


# In[9]:


if __name__ == '__main__':
    path = easygui.enterbox("Please enter the path of file that you want to convert:")
    total_cnt = 0
    success_cnt = 0
    if len(sys.argv) == 1:
        raw_input("[error] need root dir")
        sys.exit(-1)
    convertdir = sys.argv[1]
    backup_to_zip(path)
    convert_dir(path)


# In[ ]:




