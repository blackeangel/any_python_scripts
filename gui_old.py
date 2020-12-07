from tkinter import *
 
class Block:
    def __init__(self, master):
        self.e = Button(master, text="1")
        self.b = Button(master, text="2")
        self.l = Button(master, text="Выход")
        self.b.pack()
        self.l.pack()
        self.e['command'] = self.prints('1')	
		self.b['command'] = self.prints('2')
		self.l['command'] = self.exit()
	def prints(self,i)
		print(i)	   
root = Tk()
first_block = Block(root)
#first_block.setFunc('strToSortlist')
root.mainloop()