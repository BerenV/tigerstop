import tkinter as tk
from tkinter import *
from tkinter.messagebox import showinfo
from tkinter.simpledialog import Dialog
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
unitFlag = 1 # gets set to 1 if someone switches units to in
# initialize to 1 so the first time of the day sets units to mm

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
#calipers = Serial('/dev/ttyUSB1', 9600)
#tigerstop = Serial('/dev/ttyUSB0',9600)
# I think this increments each time and can be tough to chase down
# TODO auto detect which serial port is which device

# Initiate serial ports
srl0 = Serial('/dev/ttyUSB0', 9600, timeout=1)
srl1 = Serial('/dev/ttyUSB1',9600, timeout=1)

srl0.write(b'M77') # try this on for kicks
rply = srl0.readline() # gets first line
if rply == 'Tigerstop serial interface 1.2': # expected reply from Tigerstop Uno
    calipers = srl1
    tigerstop = srl0
    print('Case 0')
else:
    calipers = srl0
    tigerstop = srl1
    print('Case 1')
# Yes I know this isn't a good solution but it's too late to be smart...
# Need to remember to make this more sophisticated if I increase the version number



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
        nextButton["text"]="end!"

def goTiger():
    global index
    global goFlag
    global seekFlag
    global unitFlag
    if unitFlag == 1:
        changeUnitsMm()
        time.sleep(2) # waits for unit change to happen
        unitFlag = 0 # set to indicate it's now in mm
    
    
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
            index += 1 # python doesn't have ++ increment operator
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
        backButton["text"]="end!"
        
def updateLb():
    Lb.selection_clear(0, tk.END)
    Lb.selection_set(index)
    Lb.see(index) #important, scrolls listbox when necessary
    #Lb.activate(index)
    print(Lb.get(Lb.curselection())) #not cutlist[index]

def goTo(loc):
    global unitFlag
    global lastPos
    lastPos = loc
    if unitFlag == 1:
        changeUnitsMm()
        time.sleep(2) # waits for unit change to happen
        unitFlag = 0 # set to indicate it's now in mm
    
    #gotta remove that pesky comma from the end
    #loc = loc.rstrip(loc[-1])
    print(loc)
    tigerstop.write(bytes(('X' + str(loc) + '\n'),encoding='utf-8'))
    #send command to move over serial
    
def getInput():
    while 1==1:
        scanNumber = tk.simpledialog.askfloat('Barcode entry window', 'Scan barcode')
        if not scanNumber: # 'Cancel'
            return
        else:
            goTo(scanNumber*25.4)
            
def changeUnitsIn():
    unitFlag = 1
    tigerstop.write(bytes(('G' + '20' + '\n'),encoding='utf-8'))
    print("Changing units to in")
    
def changeUnitsMm():
    unitFlag = 0
    tigerstop.write(bytes(('G' + '21' + '\n'),encoding='utf-8'))
    print("Changing units to mm")

def changeCalLong():
    tigerstop.write(bytes(('M' + '78' + '\n'),encoding='utf-8'))
    print("Changing calibration longer")

def changeCalShort():
    tigerstop.write(bytes(('M' + '79' + '\n'),encoding='utf-8'))
    print("Changing calibration shorter")
    
tch=tk.Tk() #"touch" window
tch.title("Tigerstop control")
tch.config(cursor="none") #uncomment for tchscreen operation (RPi only)
#DO NOT use on Mac since it causes the window to freeze
goButtonFont=tkinter.font.Font(family='Helvetica', size = 40, weight = "bold")
buttonFont=tkinter.font.Font(family='Helvetica', size = 36, weight = "bold")

goButton=tk.Button(tch, text='Go', font=goButtonFont, command=goTiger, bg='green', activebackground='green', height=3, width=12)
goButton.grid(row=0, column=0, columnspan=1, padx=14)
backButton=tk.Button(tch, text='Back', font=buttonFont, command=moveBack, bg='red', activebackground='red', height=3, width=12)
backButton.grid(row=1, column=0, padx=32)
nextButton=tk.Button(tch, text='Next', font=buttonFont, command=moveNext, bg='cyan', activebackground='cyan', height=3, width=12)
nextButton.grid(row=1, column=1, padx=32)

#scannerEntry=Entry(tch)
#scannerEntry.grid(row=0, column=1, padx=0)
scannerButton = tk.Button(tch, text='Barcode', font=goButtonFont, command=getInput, bg='yellow', activebackground='yellow', height=3, width=12)
scannerButton.grid(row=0, column=1, padx=0)

# attempt to add menu
menubar = Menu(tch)
options = Menu(menubar, tearoff = 0)
menubar.add_cascade(label ='Options', font = ("", 20), menu = options) 
options.add_command(label='Change units to in', font = ("", 30), command = changeUnitsIn)
options.add_command(label='Change units to mm', font = ("", 30), command = changeUnitsMm)
options.add_separator()
options.add_command(label='Bump calibration LONGER', font = ("", 30), command = changeCalLong)
options.add_command(label='Bump calibration SHORTER', font = ("", 30), command = changeCalShort)
options.add_separator()
options.add_command(label ='Quit', font = ("", 30), command = tch.destroy) 


# # for scrolling vertically
# yscrollbar = Scrollbar(window)
# yscrollbar.pack(side = RIGHT, fill = Y)
# yscrollbar.config(command = list.yview)
listFont=tkinter.font.Font(size = 28)
# var=tk.Variable(value=cutlist)
var=tk.Variable()
Lb=tk.Listbox(tch, listvariable=var, font=listFont, height=11, width=8, selectmode=tk.SINGLE)
Lb.grid(row=0, column=3, rowspan=2, padx=0, pady=10)
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
lastDel = 0
def updateLabelData(data):
    global lastDel
    time.sleep(0.1) # apparantly it needs a little time to receive all digits
    data = data.decode("utf-8")
    print(data)
    if re.search('[a-zA-Z]', data) and lastDel == 0: #maybe??
        Lb.delete(END)
        lastDel = 1
        print("deleting last line")
    else:
        lastDel = 0
    
    l = []
    for t in data.split():
        try:
            l.append(round((float(t)*25.4), 2)) # convert to mm here for now I guess
        except ValueError:
            pass
    if bool(l):
        print(l[0])
        if l[0] < 25.0:
            Lb.insert(END, "---------")
            # TODO make this include number of measurements above
        else:
            Lb.insert(END, l[0])
        lasDel = 0

    tch.update_idletasks()

# Initiate ReaderThread
reader = ReaderThread(calipers, SerialReaderProtocolRaw)
# Start reader
reader.start()

#launch GUI window
tch.config(menu = menubar)
tk.mainloop()


