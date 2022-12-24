import tkinter as tk
import tkinter.font
import time


win=tk.Tk()
win.title ("Tigerstop control")
#win.config(cursor="none") #uncomment for touchscreen operation (RPi only)
#DO NOT use on Mac since it causes the window to freeze
myFont=tkinter.font.Font(family='Helvetica', size = 24, weight = "bold")

cutlist=[]
ledState=False

def ledToggle():
    global ledState
    if not ledState:
        ledState=True
        ledButton["text"]="Turn LED Off"
    else:
        ledState=False
        ledButton["text"]="Turn LED On"
ledState=False
def goButton():
    win.quit()

def stopButton():
    # probably don't need homing feature
    win.quit()


ledButton=tk.Button(win, text='Turn LED On', font=myFont, command=ledToggle, bg='green', activebackground='green', height=3, width=24)
ledButton.grid(row=0, sticky=tk.NSEW)
goButton=tk.Button(win, text='Go Set 1', font=myFont, command=goButton, bg='cyan', height=3, width=12)
goButton.grid(row=1, sticky=tk.E)
stopButton=tk.Button(win, text='Stop', font=myFont, command=stopButton, bg='red', activebackground='red', height=3, width=12)
stopButton.grid(row=1, sticky=tk.W)

tk.mainloop()

