#from guizero import App, Text, PushButton, ListBox
import tkinter as tk
import tkinter.font
import time
import serial

win=tk.Tk()
win.title ("Tigerstop beta control")
win.config(cursor="none") #uncomment for touchscreen operation (RPi only)
#DO NOT use on Mac since it causes the window to freeze
myFont=tkinter.font.Font(family='Helvetica', size = 30, weight = "bold")

cutlist=[]
index = 0 # to keep track of place in cutlist

calipers = serial.Serial('/dev/ttyUSB1',9600)
time.sleep(2)
calipers.readline() #get that zero out of the buffer

reading = 2.1
while reading > 1.0:
    raw = calipers.readline()
    reading = float(raw[1:8])
    cutlist.append(reading)

del cutlist[-1] #removes last reading which is a zero
print(cutlist) #debugging

tigerstop = serial.Serial('/dev/ttyUSB0',9600)
# I think this increments each time and can be tough to chase down

#start GUI

def stopGUI():
    win.quit()
    #os.execl(sys.executable, sys.executable, *sys.argv)
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

# def goTo(int loc):
#     global index
#     output = 'X'
#     

nextButton=tk.Button(win, text='Go', font=myFont, command=moveNext, bg='green', activebackground='green', height=3, width=24)
nextButton.grid(row=0, sticky=tk.N)
backButton=tk.Button(win, text='Back', font=myFont, command=moveBack, bg='cyan', height=3, width=12)
backButton.grid(row=1, sticky=tk.SE)
restartButton=tk.Button(win, text='Stop', font=myFont, command=stopGUI, bg='red', activebackground='red', height=3, width=12)
restartButton.grid(row=1, sticky=tk.SW)

tk.mainloop()
# app = App(title="Tigerstop Beta")
# 
# message = Text(app, text="Some useful instructions")
# 
# nextButton = PushButton(app, text="Next", command=moveNext)
# nextButton.bg = "green"
# restartButton = PushButton(app, text="Restart", command=restartProgram)
# restartButton.bg = "red"
# 
# app.display()