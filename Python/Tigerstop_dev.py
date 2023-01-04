import tkinter as tk
from tkinter import *
from tkinter.messagebox import showinfo
from serial import Serial
from serial.threaded import ReaderThread, Protocol
import tkinter.font
import time
import serial



cutlist=[]
index = 0 # to keep track of place in cutlist
lastPos = 0.0
goFlag = 0
seekFlag = 0
# 
# calipers = serial.Serial('/dev/ttyUSB1',9600)
# time.sleep(1)
# calipers.readline() #get that zero out of the buffer!
#                     #(for imaginary calipers only)
# 
# reading = 2.1
# while reading > 1.0:
#     raw = calipers.readline()
#     reading = float(raw[1:8])
#     cutlist.append(reading)
# 
# del cutlist[-1] #removes last reading which is a zero

#cutlist=[52.376, 164.006, 22.261, 44.884, 81.290, 17.283] #hardcode cutlist for testing
#print(cutlist) #debugging
#successfully removed all dependency on cutlist

# Initiate serial ports
calipers = Serial('/dev/ttyUSB0', 9600)
tigerstop = Serial('/dev/ttyUSB1',9600)
# I think this increments each time and can be tough to chase down
# TODO auto detect which serial port is which device


#start GUI
#for i in range(len(cutlist)):
#   Lb.insert(i, cutlist[i])
#Lb.pack(expand=True, fill=tk.BOTH)

def moveNext():
    global index
    global goFlag
    global seekFlag
    seekFlag = 1
    #Lb.insert(7, 88.888)
    if goFlag== 0:
        goFlag = 1
        # don't increment this first time
        updateLb()
        #goButton["text"]="Next" # say "Next" after the first time
        backButton["text"]="Back"
    elif index < (Lb.size()-1):
        index += 1 # silly python doesn't have increment ++
        updateLb()
        backButton["text"]="Back"
    else:
        #error
        print("error")
        updateLb()
        goButton["text"]="Done!"
        nextButton["text"]="error"

def goTiger():
    global index
    global goFlag
    global seekFlag
    if goFlag == 0:
        goFlag = 1
        # don't increment this first time
        updateLb()
        goTo(Lb.get(Lb.curselection()))
        seekFlag = 0
        #tigerstop.write(bytes(('X' + str(cutlist[index]) + '\n'),encoding='utf-8'))
        #goButton["text"]="Next" # say "Next" after the first time
        backButton["text"]="Back"
    elif index < (Lb.size()-1): #index < (len(cutlist)-1):
        if not bool(seekFlag):
            index += 1 # silly python doesn't have ++ increment operator
        updateLb()
        goTo(Lb.get(Lb.curselection()))
#         if lasLoc != Lb.get(Lb.curselection()):
#             goTo(Lb.get(Lb.curselection()))
        #tigerstop.write(bytes(('X' + str(cutlist[index]) + '\n'),encoding='utf-8'))
        backButton["text"]="Back"
        seekFlag = 0
    else:
        #error
        print("error")
        goButton["text"]="Done!"
        seekFlag = 0

def moveBack():
    global index
    global seekFlag
    seekFlag = 1
    if index > 0:
        index -=1
        #goTo(cutlist[index])
        #tigerstop.write(bytes(('X' + str(cutlist[index]) + '\n'),encoding='utf-8'))
        updateLb()
        goButton["text"]="Go"
        backButton["text"]="Back"
        nextButton["text"]="Next"
    else:
        #display error?
        print("error")
        backButton["text"]="error"
        
def updateLb():
    Lb.selection_clear(0, tk.END)
    Lb.selection_set(index)
    Lb.see(index) #important, scrolls listbox when necessary
    #Lb.activate(index)
    print(Lb.get(Lb.curselection())) #not cutlist[index]

def goTo(loc):
    global lastPos
    lastPos = loc
    #gotta remove that pesky comma from the end
    #loc = loc.rstrip(loc[-1])
    #print(loc)
    tigerstop.write(bytes(('X' + str(loc) + '\n'),encoding='utf-8'))
    #send command to move over serial

tch=tk.Tk() #"touch" window
tch.title("Tigerstop beta control")
tch.config(cursor="none") #uncomment for tchscreen operation (RPi only)
#DO NOT use on Mac since it causes the window to freeze
buttonFont=tkinter.font.Font(family='Helvetica', size = 44, weight = "bold")

goButton=tk.Button(tch, text='Go', font=buttonFont, command=goTiger, bg='green', activebackground='green', height=3, width=24)
goButton.grid(row=0, column=0, columnspan=2)
backButton=tk.Button(tch, text='Back', font=buttonFont, command=moveBack, bg='red', activebackground='red', height=3, width=12)
backButton.grid(row=1, column=0)
nextButton=tk.Button(tch, text='Next', font=buttonFont, command=moveNext, bg='cyan', activebackground='cyan', height=3, width=12)
nextButton.grid(row=1, column=1)

# # for scrolling vertically
# yscrollbar = Scrollbar(window)
# yscrollbar.pack(side = RIGHT, fill = Y)
# yscrollbar.config(command = list.yview)
listFont=tkinter.font.Font(size = 14)
# var=tk.Variable(value=cutlist)
var=tk.Variable()
Lb=tk.Listbox(tch, listvariable=var, font=listFont, height=18, width=10, selectmode=tk.SINGLE)
Lb.grid(row=0, column=3, rowspan=2)
#Lb.pack(padx = 10, pady = 10, expand = YES, fill = "both")
# lst=tk.Tk() #"list" window
# lst.title("Current cutlist contents")
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

#lst.mainloop()
class SerialReaderProtocolRaw(Protocol):
    port = None

    def connection_made(self, transport):
        """Called when reader thread is started"""
        print("Connected, ready to receive data...")

    def data_received(self, data):
        """Called with snippets received from the serial port"""
        updateLabelData(data)

def updateLabelData(data):
    data = data.decode("utf-8")
    l = []
    for t in data.split():
        try:
              l.append(float(t))
        except ValueError:
            pass
    if bool(l):
        Lb.insert(END, float(l[0]))
        print(float(l[0]))
    tch.update_idletasks()

# Initiate ReaderThread
reader = ReaderThread(calipers, SerialReaderProtocolRaw)
# Start reader
reader.start()
tk.mainloop()

