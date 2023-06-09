import tkinter as tk
import winsound
import time
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinterdnd2 import DND_FILES, TkinterDnD
import threading

WORK = 1
BREAK = 2

def to_seconds(s):
    m, s = s.split(":")
    return int(m)*60 + int(s)

def from_seconds(s):
    return "{:02d}:{:02d}".format(s//60, s%60)

# root = TkinterDnD.Tk()  # notice - use this instead of tk.Tk()
root = tk.Tk()
root.geometry("400x400")
root.title("Pomo timer")
root.maxsize(800, 400)


tk.Label(root, text="Pomodoro timer", font=("Helvetica", 20)).grid(row=0, column=0,columnspan=2, padx=5, pady=5)
tk.Label(root, text="Work time", font=("Helvetica", 12)).grid(row=1, column=0, padx=5, pady=5)

break_work = tk.IntVar(value=WORK)

work_time_var = tk.StringVar()
work_time_var.set("25:00")
work_time_radio = tk.Radiobutton(root, text="", value=WORK, variable=break_work)
work_time_radio.grid(row=1, column=3)

break_time_radio = tk.Radiobutton(root, text="", value=BREAK, variable=break_work)
break_time_radio.grid(row=2, column=3)


work_time_entry = tk.Entry(root, width=10, text=work_time_var )
work_time_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Break time", font=("Helvetica", 12)).grid(row=2, column=0, padx=5, pady=5)

break_time_var = tk.StringVar()
break_time_var.set("5:00")

break_time_entry = tk.Entry(root, width=10, text=break_time_var )
break_time_entry.grid(row=2, column=1, padx=5, pady=5)


rtime = tk.Label(root, text="--:--", font=("Helvetica", 30))
rtime.grid(row=4, column=0, columnspan=2, padx=5, pady=5)


event = threading.Event()

class Thread(threading.Thread):
    def __init__(self, rseconds):
        self.rseconds = rseconds
        rtime.config(text=from_seconds(self.rseconds))
        
        threading.Thread.__init__(self)
        
        # helper function to execute the threads
    def run(self):
        while(1):
            if event.is_set():
                event.clear()
                rtime.config(text="--:--")
                break

            time.sleep(1)
            # winsound.Beep(440, 500)
            self.rseconds = self.rseconds - 1
            rtime.config(text=from_seconds(self.rseconds))
            root.wm_title(str(from_seconds(self.rseconds)))
            root.title = str(from_seconds(self.rseconds))
            


def start_pomo():
    wktime = work_time_var.get()
    bktime = break_time_var.get()
    winsound.Beep(440, 500)
    rseconds = to_seconds(wktime)
    t = Thread(rseconds)
    t.start()
    root.iconbitmap("ico.ico")
    
    


def stop_promo():
    event.set()


start_button = ttk.Button(root, text="Start", command=start_pomo)
start_button.grid(row=3, column=0, padx=5, pady=5)

stop_button = ttk.Button(root, text="Stop", command=stop_promo)
stop_button.grid(row=3, column=1, padx=5, pady=5)




root.mainloop()

NOTE_FREQUENCIES = {
    "C": 262,
    "D": 294,
    "E": 330,
    "F": 349,
    "G": 392,
    "A": 440,
    "B": 494,
    "C#": 277,
    "D#": 311,
    "F#": 370,
    "G#": 415,
    "A#": 466,

}


def playnote(n, d):
    f = NOTE_FREQUENCIES[n]
    winsound.Beep(f, d)
    

def playnotes(notes):
    for n in notes:
        playnote(n[0], 200)

#playnotes("EEFGGFEDCCDEEDD")
#playnotes("EEFGGFEDCCDEDCC")