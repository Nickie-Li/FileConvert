#!/usr/bin/env python
# coding: utf-8

# In[ ]:


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

from tkinter import *

suffix = ["txt", "log", "m3u8", "m3u", "cue"]  # All the suffix of files that should be converted.


# In[ ]:


'''
Pop up window checkbox
'''

class Checkbox(Frame):
    def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
        Frame.__init__(self, parent)
        self.vars = []
        for pick in picks:
            var = IntVar()
            chk = Checkbutton(self, text=pick, variable=var)   # Add Options
            chk.pack(side=side, anchor=anchor, expand=YES)
            self.vars.append(var)
            
    ''' Map checkbox value'''
    def state(self):
        return map((lambda var: var.get()), self.vars)
    
    '''Get chosen options of checkbox'''
    def allstates(self): 
        global function_list
        function_list = list(self.state())
        root.destroy()
        
    '''Quit'''
    def quit(self): 
        global quit_flag
        quit_flag = True
        root.destroy()


# In[ ]:


'''
Back up the root folder into a zip file.
'''

def backup_to_zip(path):
    fname = "backup" + '_' + strftime("%Y%m%d_%H%M", gmtime()) + '.zip'
    zipf = zipfile.ZipFile(fname, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(path):
        for file in files:
            zipf.write(os.path.join(root, file))
    zipf.close()


# In[ ]:


'''
Back up file
'''

def backup(file):
    name = (".").join(file.split(".")[:-1])
    filetype = file.split(".")[-1]
    shutil.copy(file, name + "_backup." + filetype)


# In[ ]:


'''
Convert encoding format of file to utf8
'''

def convert_encoding_to_utf_8(filename, content):
    source_encoding = chardet.detect(content)['encoding']  # read file encoding
    if source_encoding != 'utf-8' and source_encoding != 'UTF-8-SIG':  # if encoding not utf8
        try:
            content = content.decode(source_encoding, 'ignore')    #ignore file encoding
        except: # if None
            content = content.decode('None', 'ignore')    #ignore file encoding
        
        # Write with utf8 encoding
        with open(filename, 'w', encoding='UTF-8-SIG') as file:
            file.write(content)
            
    return content


# In[ ]:


'''
Convert file to Traditional Chinese
'''
def toTraditional(filename, content):

    content_trans = HanziConv.toTraditional(content)
    
    if content_trans != content:
        # Write with utf8 encoding
        with open(filename, 'w', encoding='UTF-8-SIG') as file:
            file.write(content_trans)


# In[ ]:


def convert_dir(root_dir):
    global function_list
    
    # Check if root path is valid
    if os.path.exists(root_dir) == False:
        print("[error] dir:",root_dir,"do not exit")
        return
    
    print("work in", root_dir)
    
    for root, dirs, files in os.walk(root_dir):  # recursively work in folder
        '''Convert folder name'''
        ########################################### Function 檔名轉繁體 start ###########################################
        if(function_list[0] == 1):
            root_trans = HanziConv.toTraditional(root)
            if(root_trans != root):
                os.rename(root, root_trans)
        ########################################### Function 檔名轉繁體 end #############################################
    
    for root, dirs, files in os.walk(root_dir):  # recursively work in folder
        
        # Work with file
        for f in files:
            filename = os.path.join(root, f)
            
            ######################################### Function 檔名轉繁體 start #########################################
            if(function_list[0] == 1):
                filename_trans = HanziConv.toTraditional(filename)
                if(filename_trans != filename):
                    os.rename(filename, filename_trans)
            ######################################### Function 檔名轉繁體 end ###########################################
            
            # Read file once
            if(function_list[1] == 1 or function_list[2] == 1) and (any(suf in filename_trans for suf in suffix)):
                content = codecs.open(filename_trans, 'rb').read()
                backup(filename_trans)
            
            ######################################## Function 檔案編碼轉換 start ########################################
            if(function_list[1] == 1):
                try:
                    if(any(suf in filename_trans for suf in suffix)):
                        content = convert_encoding_to_utf_8(filename_trans, content)
                except:
                    print("Fail Convert utf-8",filename)
            ######################################## Function 檔案編碼轉換 end ##########################################
            
            ######################################### Function 檔案轉繁體 start #########################################
            if(function_list[2] == 1):
                try:
                    if(any(suf in filename_trans for suf in suffix)):
                        toTraditional(filename_trans, content)
                except:
                    print("Fail Convert",filename)
            ######################################### Function 檔案轉繁體 end ###########################################


# In[ ]:


if __name__ == '__main__':
    # Get path
    path = easygui.enterbox("請輸入轉檔的絕對路徑:")
    quit_flag = False  # check if user quit
    
    function_list = []   # Store 1 or 0, representing which funtion should be executed.
    ################################################# Pop up start #################################################
    root = Tk()
    root.geometry("500x50") #Width x Height
    root.title("請選擇需執行的功能")   # Dialog Title
    lng = Checkbox(root, ['檔名轉繁體', '檔案編碼轉換', '檔案轉繁體'])   # Add Options
    lng.pack(side=TOP,  fill=X)
    lng.config(relief=GROOVE, bd=2)
        
    Button(root, text='Cancel', command=lng.quit).pack(side=RIGHT)   # Cancel Button
    Button(root, text='Confirm', command=lng.allstates).pack(side=RIGHT)   # Confirm Button
    root.mainloop()   # Dialog pop up
    ################################################# Pop up end ###################################################
    
    if(not quit_flag):
        ############################################### Execution start ################################################
        backup_to_zip(path)
        convert_dir(path)
        ################################################ Execution end #################################################
        print("Execution done!")
    else:
        print("Cancel!")


# In[ ]:




