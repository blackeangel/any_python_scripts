# -*- coding: utf-8 -*-
import os
import ntpath
import tkinter
import tkinter.filedialog
from tkinter import messagebox
def selectdir():
        options = {}
        fsconfig=[]
        options['initialdir'] = os.path.abspath(__file__)
        options['title'] = "Выберите папку"
        options['mustexist'] = False
        selectdir = tkinter.filedialog.askdirectory(**options)
        if selectdir == "":
            exit()
        else:
            namefolder=ntpath.basename(selectdir)
            messagebox.showinfo("Выбор папки","Выбрана папка:\n"+selectdir)
        fs_config_file=os.path.dirname(os.path.abspath(selectdir))+os.sep+"fs_config_" + namefolder + ".txt"
        for top, dirs, files in os.walk(selectdir):
            fsconfig.append(top.replace(os.sep,"/").replace((os.path.dirname(os.path.abspath(selectdir)) + os.sep).replace(os.sep,"/"),'').replace(os.sep,"/") + " 0 0 755")
            for nm in files:
                fsconfig.append(os.path.join(top.replace(os.sep,"/").replace((os.path.dirname(os.path.abspath(selectdir)) + os.sep).replace(os.sep,"/"),''), nm).replace(os.sep,"/") + " 0 0 644")
        fsconfig.sort()
        del fsconfig[0]
        with open(fs_config_file, 'a', newline='\n') as file:
            print('\n'.join(fsconfig), file=file)
def main():
    selectdir()
if __name__ == '__main__':
    main()