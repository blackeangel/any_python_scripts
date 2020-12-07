# -*- coding: utf-8 -*-

from tkinter import Tk, W, E
from tkinter.ttk import Frame, Button, Label
import tkinter.filedialog


class Example(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.title("UAA")
        # столбцы
        self.columnconfigure(0, pad=3)
        self.columnconfigure(1, pad=3)
        self.columnconfigure(2, pad=3)
        self.columnconfigure(3, pad=3)

        # строки
        self.rowconfigure(0, pad=3)
        self.rowconfigure(1, pad=3)
        self.rowconfigure(2, pad=3)
        self.rowconfigure(3, pad=3)
        self.rowconfigure(4, pad=3)

        entry = Label(self, text="Program UAA v.0000001").grid(row=0, columnspan=4)  # , sticky=W + E)
        ex = Button(self, text="Exit", command=self.finish).grid(row=1, column=0)  # 0 - это от левого края и так далее
        bck = Button(self, text="Select file", command=self.selectfile).grid(row=1, column=1)
        lbl = Button(self).grid(row=1, column=2)
        clo = Button(self, text="Close").grid(row=1, column=3)
        sev = Button(self, text="7").grid(row=2, column=0)
        eig = Button(self, text="8").grid(row=2, column=1)
        nin = Button(self, text="9").grid(row=2, column=2)
        div = Button(self, text="/").grid(row=2, column=3)

        fou = Button(self, text="4").grid(row=3, column=0)
        fiv = Button(self, text="5").grid(row=3, column=1)
        six = Button(self, text="6").grid(row=3, column=2)
        mul = Button(self, text="*").grid(row=3, column=3)

        one = Button(self, text="1").grid(row=4, column=0)
        two = Button(self, text="2").grid(row=4, column=1)
        thr = Button(self, text="3").grid(row=4, column=2)
        mns = Button(self, text="-").grid(row=4, column=3)

        zer = Button(self, text="0").grid(row=5, column=0)
        dot = Button(self, text=".").grid(row=5, column=1)
        equ = Button(self, text="=").grid(row=5, column=2)
        pls = Button(self, text="+").grid(row=5, column=3)

        self.pack()

    def selectfile(self):
        ftypes = [('All files', '*')]
        dlg = tkinter.filedialog.Open(self, filetypes=ftypes)
        fl = dlg.show()
        print(fl)
        #fileselect = tkinter.filedialog.askopenfilename()

    def finish(self):
        exit()


def main():
    root = Tk()
    app = Example(root)
    root.mainloop()


if __name__ == '__main__':
    main()
