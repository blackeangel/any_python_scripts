# -*- coding: utf-8 -*-
import tkinter
from tkinter import ttk, Button, Label, Frame
from tkinter import *
import tkinter.filedialog
import os
import ntpath
from tkinter import messagebox

indir=os.path.abspath(__file__)
fsconfig=[]
selelem={}
fs_config_file=''

def selectfile():
    ftypes = [('Все файлы', '*')]
    dlg = tkinter.filedialog.Open(filetypes=ftypes, title='Выберите файл', initialdir=indir)
    filename=dlg.show()
    try:
        lbox.insert(END, filename + " 0 0 644")
    except:    
        return
        
def finish():
    exit()

def selectdir():
        selectdir = tkinter.filedialog.askdirectory(initialdir = indir, title= "Выберите папку", mustexist = False)
        try:
            namefolder=ntpath.basename(selectdir)
            messagebox.showinfo("Выбор папки","Выбрана папка:\n"+selectdir)
            #fs_config_file=os.path.dirname(os.path.abspath(selectdir))+os.sep+"fs_config_" + namefolder + ".txt"
            for top, dirs, files in os.walk(selectdir):
                fsconfig.append(top.replace(os.sep,"/").replace((os.path.dirname(os.path.abspath(selectdir)) + os.sep).replace(os.sep,"/"),'').replace(os.sep,"/") + " 0 0 755")
                for nm in files:
                    fsconfig.append(os.path.join(top.replace(os.sep,"/").replace((os.path.dirname(os.path.abspath(selectdir)) + os.sep).replace(os.sep,"/"),''), nm).replace(os.sep,"/") + " 0 0 644")
            fsconfig.sort()
            del fsconfig[0]
            for i in fsconfig:
                lbox.insert(0,i)
            #with open(fs_config_file, 'a', newline='\n') as file:
            #   print('\n'.join(fsconfig), file=file)
        except:
            return
                     
def selectfs():
    global fs_config_file
    ftypes = [('Текстовые файлы', '*fs_config*.txt')]
    dlg = tkinter.filedialog.Open(filetypes=ftypes,  title='Выберите файл', initialdir=indir)
    fs_config_file = dlg.show()
    try:
        label1.config(text="fs_config: " + fs_config_file)
        sen.config(state=NORMAL)
    except:
        return

def editListelement():
    try:
        global selelem
        selelem=list(lbox.curselection())
        entry.delete(0,END)
        entry.insert(0,lbox.get(list(lbox.curselection())))
    except:
        return

def saveelement():
    if entry.get()=="":
        return
    global selelem
    lbox.insert(selelem[0], entry.get())
    selelem[0]=selelem[0]+1
    lbox.delete(selelem)
    entry.delete(0, END)

def addItem():
    lbox.insert(END, entry.get())
    entry.delete(0, END)

def delList():
    select = list(lbox.curselection())
    select.reverse()
    for i in select:
        lbox.delete(i)

def saveList():
    global fs_config_file
    if fs_config_file=='':
        messagebox.showerror("Ошибка!", "Не выбран файл fs_config")
        return
    f = open(fs_config_file, 'a')
    f.writelines("\n".join(lbox.get(0, END)))
    f.close()


win = tkinter.Tk() 
win.title("Добавление файлов")
frame= tkinter.Frame(win,bd=15,width = 120)
frame.pack()

#столбцы
frame.columnconfigure(0, pad=4)

# строки
frame.rowconfigure(0, pad=4)

#ex = Button(frame, text="Выход", command=finish)
#ex.grid(row=1, column=0)  # 0 - это от левого края и так далее
bck = Button(frame, text="Добавить файл", command=selectfile)
bck.grid(row=1, column=1)
lbl = Button(frame,text="Добавить папку", command=selectdir)
lbl.grid(row=1, column=2)
sfs = Button(frame, text="Выбрать fs_config", command=selectfs)
sfs.grid(row=1, column=3)
sen=Button(frame, text="Закончить редактирование", command=saveList, state=DISABLED)
sen.grid(row=1, column=4)
label1 = Label(text="fs_config: " + fs_config_file)
label1.pack()

lbox = Listbox(selectmode=EXTENDED, width = 120)
lbox.pack(side=LEFT, fill=Y)
scroll = Scrollbar(command=lbox.yview)
scroll.pack(side=LEFT, fill=Y)
lbox.config(yscrollcommand=scroll.set)

f = Frame()
f.pack(side=LEFT, padx=10)
entry = Entry(f,width = 120)
entry.pack(anchor=N)
badd = Button(f, text="Добавить запись", command=addItem)
badd.pack(fill=X)
bdel = Button(f, text="Удалить запись", command=delList)
bdel.pack(fill=X)
bsave = Button(f, text="Редактировать запись", command=editListelement)
bsave.pack(fill=X)
bsave = Button(f, text="Сохранить запись", command=saveelement)
bsave.pack(fill=X)

win.mainloop()
