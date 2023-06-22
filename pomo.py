import tkinter as tk
import winsound
import time
from tkinter import ttk
from tkinter.messagebox import showinfo
import threading

WORK = 1
BREAK = 2
BILLION = 1000000000


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

def to_nseconds(s):
    m, s = s.split(":")
    return BILLION * (int(m)*60 + int(s))

def from_nseconds(s):
    s = round(s / BILLION)

    return "{:02d}:{:02d}".format(s//60, s%60)

def set_titel(s):
    root.wm_title(str(s))
    root.title = str(s)

root = tk.Tk()
root.geometry("300x300")
root.title("Pomo timer")
root.maxsize(300, 300)
root.minsize(300, 300)

tk.Label(root, text="Pomodoro timer", font=("Helvetica", 20)).grid(row=0, column=0,columnspan=2, padx=5, pady=5)
tk.Label(root, text="Work time", font=("Helvetica", 12)).grid(row=1, column=0, padx=5, pady=5)

break_work = tk.IntVar(value=WORK)

work_time_var = tk.StringVar()
work_time_var.set("25:00")
work_time_radio = ttk.Radiobutton(root, text="", value=WORK, variable=break_work, takefocus=False)
work_time_radio.grid(row=1, column=3)

break_time_radio = ttk.Radiobutton(root, text="", value=BREAK, variable=break_work, takefocus=False)
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


rseconds = None
running = False
gtime = None 

def after_check():
    global rseconds, running, gtime
    time_passed = time.time_ns() - gtime
    gtime = time.time_ns()

    if running:
        rseconds = rseconds - time_passed
        if rseconds < 0:
            winsound.Beep(440, 500)

            if break_work.get() == WORK:
                rseconds = to_nseconds(break_time_var.get())
                root.iconbitmap("walk.ico")
                break_work.set(BREAK)
                # playnotes("EEFGGFEDCCDEEDD")
            else:
                rseconds = to_nseconds(work_time_var.get())
                break_work.set(WORK)
                root.iconbitmap("work.ico")
                # playnotes("EEFGGFEDCCDEDCC")
        rtime.config(text=from_nseconds(rseconds), fg="red" if break_work.get() == WORK else "green")
        set_titel("{} / {}".format(from_nseconds(rseconds), "working" if break_work.get() == WORK else "break" ))
        
        root.after(100, after_check)


def start_pomo():
    global rseconds, running, gtime
    gtime = time.time_ns()
    wktime = work_time_var.get()
    bktime = break_time_var.get()
    winsound.Beep(440, 500)
    if break_work.get() == WORK:
        root.iconbitmap("work.ico")
        rseconds = to_nseconds(wktime)
    else:
        root.iconbitmap("walk.ico")
        rseconds = to_nseconds(bktime)

    print(rseconds)
    running = True
    root.after(100, after_check)


def stop_promo():
    global running
    running = False


start_button = ttk.Button(root, text="Start", command=start_pomo)
start_button.grid(row=3, column=0, padx=5, pady=5)

stop_button = ttk.Button(root, text="Stop", command=stop_promo)
stop_button.grid(row=3, column=1, padx=5, pady=5)




root.mainloop()


#playnotes("EEFGGFEDCCDEEDD")
#playnotes("EEFGGFEDCCDEDCC")
