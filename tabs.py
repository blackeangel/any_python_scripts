import tkinter
from tkinter import ttk, Button, Label, Frame
import tkinter.filedialog
def selectfile():
    ftypes = [('All files', '*')]
    dlg = tkinter.filedialog.Open(filetypes=ftypes)
    fl = dlg.show()
    print(fl)
    #fileselect = tkinter.filedialog.askopenfilename()
    entry['text'] = str(fl)
    
def finish():
    exit()
    
def hide_me(event):
    event.pack_forget()

win = tkinter.Tk() 
win.title("Python GUI")
frame= tkinter.Frame(win,bd=15)
frame.pack(expand=1, fill="both")
tabControl = ttk.Notebook(frame)
tab1 = ttk.Frame(tabControl)
tab1.columnconfigure(0, pad=3)
tab1.columnconfigure(1, pad=3)
tab1.columnconfigure(2, pad=3)
tab1.columnconfigure(3, pad=3)

# строки
tab1.rowconfigure(0, pad=3)
tab1.rowconfigure(1, pad=3)
tab1.rowconfigure(2, pad=3)
tab1.rowconfigure(3, pad=3)
tab1.rowconfigure(4, pad=3)

entry = Label(tab1, text="Program UAA v.0000001").grid(row=0, columnspan=4)  # , sticky=W + E)
ex = Button(tab1, text="Exit", command=finish).grid(row=1, column=0)  # 0 - это от левого края и так далее
bck = Button(tab1, text="Select file", command=selectfile).grid(row=1, column=1)
lbl = Button(tab1).grid(row=1, column=2)
clo = Button(tab1, text="Close", command=hide_me).grid(row=1, column=3)
sev = Button(tab1, text="7").grid(row=2, column=0)
eig = Button(tab1, text="8").grid(row=2, column=1)
nin = Button(tab1, text="9").grid(row=2, column=2)
div = Button(tab1, text="/").grid(row=2, column=3)
 
fou = Button(tab1, text="4").grid(row=3, column=0)
fiv = Button(tab1, text="5").grid(row=3, column=1)
six = Button(tab1, text="6").grid(row=3, column=2)
mul = Button(tab1, text="*").grid(row=3, column=3)
 
one = Button(tab1, text="1").grid(row=4, column=0)
two = Button(tab1, text="2").grid(row=4, column=1)
thr = Button(tab1, text="3").grid(row=4, column=2)
mns = Button(tab1, text="-").grid(row=4, column=3)
 
zer = Button(tab1, text="0").grid(row=5, column=0)
dot = Button(tab1, text=".").grid(row=5, column=1)
equ = Button(tab1, text="=").grid(row=5, column=2)
pls = Button(tab1, text="+").grid(row=5, column=3)
 
#bt1 = Button(tab1,text='exit', command=exit).grid(row=1, column=0)
#bt1.pack()
tab2 = ttk.Frame(tabControl)
bt = Button(tab2, text = 'text test')
bt.pack()
tabControl.add(tab1, text='Tab 1')
tabControl.add(tab2, text='Tab 2')
tabControl.pack(expand=1, fill="both")
win.mainloop()
