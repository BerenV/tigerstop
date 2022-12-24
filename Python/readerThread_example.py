import tkinter as tk

from serial import Serial
from serial.threaded import ReaderThread, Protocol

app = tk.Tk()
label = tk.Label(text="A Label")
label.pack()

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
    label['text']=data
    app.update_idletasks()

# Initiate serial port
serial_port = Serial('/dev/ttyUSB1', 9600)

# Initiate ReaderThread
reader = ReaderThread(serial_port, SerialReaderProtocolRaw)
# Start reader
reader.start()

app.mainloop()