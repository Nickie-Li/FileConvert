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


# In[2]:


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

    flag1 = True
    flag2 = True
    flag3 = True
    content = codecs.open(filename, 'rb').read()
    source_encoding = chardet.detect(content)['encoding']
    total_cnt+=1
    
    filename_trans = HanziConv.toTraditional(filename)
    if(filename_trans == filename):
        flag1 = False
        
        
    if source_encoding != 'utf-8' and source_encoding != 'UTF-8-SIG':
        content = content.decode(source_encoding, 'ignore') #.encode(source_encoding)
    else:
        flag2 = False
        
    content_trans = HanziConv.toTraditional(content)
    if(content_trans == content):
        flag3 = False
    
    if(flag1 or flag2 or flag3):
        backup(filename)
        os.rename(filename, filename_trans)
    
        with open(filename_trans, 'w', encoding='UTF-8-SIG') as file:
            file.write(content_trans)
        success_cnt+=1


# In[5]:


def convert_dir(root_dir):
    if os.path.exists(root_dir) == False:
        print("[error] dir:",root_dir,"do not exit")
        return
    print("work in", root_dir)
    for root, dirs, files in os.walk(root_dir):
        root_trans = HanziConv.toTraditional(root)
        if(root_trans != root):
            os.rename(root, root_trans)
        for f in files:
            filename = os.path.join(root_trans, f)
            try:
                convert_encoding_to_utf_8(filename)
            except:
                print("Fail Convert",filename)
    print("finish total:",total_cnt,"success:",success_cnt)


# In[6]:


if __name__ == '__main__':
    path = easygui.enterbox("Please enter the path of file that you want to convert:")
    total_cnt = 0
    success_cnt = 0
    backup_to_zip(path)
    convert_dir(path)


# In[ ]:




