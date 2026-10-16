from Cube import Cube
from tkinter import *
from tkinter import ttk
import time
import threading

window = Tk()
window.title('ACube Timer')
window.geometry('800x600')

timer = ttk.Label(window, text='0', font=('Arial', 20))
timer.pack()

def changeTimer(start):
    timer.config(text=start)
    timer.after(100, lambda: timer.config(text=changeTimer(round(start + 0.1, 1))))
        


window.mainloop()