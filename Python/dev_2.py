import tkinter as tk
from tkinter import *
#from tkinter.messagebox import showinfo
import tkinter.font
import time
import serial



# Trying to get two windows running wasn't working too well



# def goTo(int loc):
#     global index
#     output = 'X'
#


# tch=tk.Tk() #"touch" window
# tch.title("Tigerstop beta control")
# tch.config(cursor="none") #uncomment for tchscreen operation (RPi only)
#DO NOT use on Mac since it causes the tchdow to freeze
# lst=tk.Tk() #"list" window
# lst.title("Current cutlist contents")
# myFont=tkinter.font.Font(family='Helvetica', size = 30, weight = "bold")

# nextButton=tk.Button(tch, text='Go', font=myFont, command=moveNext, bg='green', activebackground='green', height=3, width=24)
# nextButton.grid(row=0, sticky=tk.N)
# backButton=tk.Button(tch, text='Back', font=myFont, command=moveBack, bg='cyan', height=3, width=12)
# backButton.grid(row=1, sticky=tk.SE)
# restartButton=tk.Button(tch, text='Stop', font=myFont, command=stopGUI, bg='red', activebackground='red', height=3, width=12)
# restartButton.grid(row=1, sticky=tk.SW)

# var=tk.Variable(value=cutlist)
# Lb=tk.Listbox(lst, listvariable=var, height=10, selectmode=tk.EXTENDED)
# Lb.pack(expand=True, fill=tk.BOTH)

# langs = [52.37, 164.006, 22.26, 44.884]
# var = tk.Variable(value=langs)
# 
# listbox = tk.Listbox(
#     lst,
#     listvariable=var,
#     height=6,
#     selectmode=tk.EXTENDED
# )
# 
# listbox.pack(expand=True, fill=tk.BOTH)
# 
# lst.mainloop()
# 
# window = tk.Tk()
# window.title('My Window')
# 
# window.geometry('500x300')
# 
# var1 = tk.StringVar()
# l = tk.Label(window, bg='green', fg='yellow',font=('Arial', 12), width=10, textvariable=var1)
# l.pack()
# 
# def print_selection():
#     value = lb.get(lb.curselection())   
#     var1.set(value)  
# 
# b1 = tk.Button(window, text='print selection', width=15, height=2, command=print_selection)
# b1.pack()
# 
# var2 = tk.StringVar()
# var2.set((1,2,3,4))
# lb = tk.Listbox(window, listvariable=var2)
# 
# list_items = [11,22,33,44]
# for item in list_items:
#     lb.insert('end', item)
# lb.insert(1, 'first')
# lb.insert(2, 'second')
# lb.delete(2)
# lb.pack()
# tk.mainloop()

cutlist=[52.37, 164.006, 22.26, 44.884] #hardcode cutlist for testing

class tch: #touchscreen interface
    def __init__(self, master):
        self.master = master
        #self.master.geometry("400x300")
        self.master.config(cursor="none") #uncomment for tchscreen operation (RPi only)
        #DO NOT use on Mac since it causes the interface to freeze
        self.show_widgets()

    def show_widgets(self):
        self.frame = tk.Frame(self.master)
        self.master.title("Tigerstop beta control")
        #self.create_button("Click to open Window 2", lst)
        goFlag = 0
        def moveNext():
            global index
            global goFlag
            if goFlag== 0:
                goFlag = 1
                # don't increment this first time
                #goto cutlist[index]
                tigerstop.write(bytes(('X' + str(cutlist[index]) + '\n'),encoding='utf-8'))
                print(cutlist[index])
                nextButton["text"]="Next" # say "Next" after the first time
                backButton["text"]="Back"
            elif index < (len(cutlist)-1):
                index += 1 # silly python doesn't have increment ++
                #goto cutlist[index]
                tigerstop.write(bytes(('X' + str(cutlist[index]) + '\n'),encoding='utf-8'))
                print(cutlist[index])
                backButton["text"]="Back"
            else:
                #error
                print("error")
                nextButton["text"]="Done!"

        def moveBack():
            global index
            if index > 0:
                index -=1
                #goto cutlist[index]
                tigerstop.write(bytes(('X' + str(cutlist[index]) + '\n'),encoding='utf-8'))
                print(cutlist[index])
                nextButton["text"]="Next"
                backButton["text"]="Back"
            else:
                #display error?
                print("error")
                backButton["text"]="error"
            
        myFont=tkinter.font.Font(family='Helvetica', size = 30, weight = "bold")
        nextButton=tk.Button(tch, text='Go', font=myFont, command=moveNext, bg='green', activebackground='green', height=3, width=24)
        nextButton.grid(row=0, sticky=tk.N)
        backButton=tk.Button(tch, text='Back', font=myFont, command=moveBack, bg='cyan', height=3, width=12)
        backButton.grid(row=1, sticky=tk.SE)
        restartButton=tk.Button(tch, text='Stop', font=myFont, command=stopGUI, bg='red', activebackground='red', height=3, width=12)
        restartButton.grid(row=1, sticky=tk.SW)
        self.frame.pack()

    def create_button(self, text, _class):
        "Button that creates a new window"
        tk.Button(
            self.frame, text=text,
            command=lambda: self.new_window(_class)).pack()
    def new_window(self, _class):
        self.win = tk.Toplevel(self.master)
        _class(self.win)

    def close_window(self):
        self.master.destroy()
        
    def stopGUI():
        tch.quit()
        #os.execl(sys.executable, sys.executable, *sys.argv)
    

class lst(tch): #cutlist window

    def show_widgets(self):
        "A frame with a button to quit the window"
        self.title("Current cutlist contents")
        self.frame = tk.Frame(self.master, bg="red")
        var=tk.Variable(value=cutlist)
        Lb=tk.Listbox(lst, listvariable=var, height=10, selectmode=tk.EXTENDED)
        Lb.pack(expand=True, fill=tk.BOTH)

        self.quit_button = tk.Button(
            self.frame, text=f"Quit this window n. 2",
            command=self.close_window)
        self.quit_button.pack()
        self.frame.pack()

root = tk.Tk()
app = tch(root)
root.mainloop()
