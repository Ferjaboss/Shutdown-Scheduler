import tkinter as tk
from tkinter import ttk  
import os
import time
from threading import Thread


window = tk.Tk()
window.title("Shutdown Scheduler")
window.geometry("320x150")  
window.resizable(False, False)
icon_path = 'off.ico'  
if os.path.exists(icon_path):
    window.iconbitmap(icon_path)
custom_font = ('Helvetica', 16)

hour_spinbox = tk.Spinbox(window, from_=0, to=23, width=2, font=custom_font)
hour_spinbox.place(x=60, y=50)
hour_label = tk.Label(window, text="H", font=custom_font)
hour_label.place(x=105, y=50)
minute_spinbox = tk.Spinbox(window, from_=0, to=59, width=2, font=custom_font)
minute_spinbox.place(x=130, y=50)
minute_label = tk.Label(window, text="M", font=custom_font)
minute_label.place(x=175, y=50)
second_spinbox = tk.Spinbox(window, from_=0, to=59, width=2, font=custom_font)
second_spinbox.place(x=200, y=50)
second_label = tk.Label(window, text="S", font=custom_font)
second_label.place(x=245, y=50)
message_label = tk.Label(window, text="Shutdown the computer after:", font=custom_font)
message_label.place(x=20, y=10)

shutdown_button = ttk.Button(window, text="Shutdown", command=lambda: toggle_shutdown(), width=15)
shutdown_button.place(x=100, y=100)

shutdown_label = tk.Label(window, text="", font=custom_font)
shutdown_label.place(x=10, y=140)


shutting_down = False

def toggle_shutdown():
    global shutting_down
    if shutting_down:
        cancel_shutdown()
    else:
        start_shutdown()

def start_shutdown():
    global shutting_down
    shutting_down = True
    shutdown_button.config(text="Cancel")
    total_seconds = get_total_seconds()

    def update_timer():
        nonlocal total_seconds
        while total_seconds > 0 and shutting_down:
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            window.geometry("320x200")
            shutdown_label.config(text=f"Shutting down in: \n {hours} hours {minutes} minutes {seconds} seconds")
            time.sleep(1)
            total_seconds -= 1

        if total_seconds <= 0 and shutting_down:
            shutdown()
    
    timer_thread = Thread(target=update_timer)
    timer_thread.start()

def cancel_shutdown():
    global shutting_down
    shutting_down = False
    shutdown_button.config(text="Shutdown")
    shutdown_label.config(text="")

def get_total_seconds():
    hours = int(hour_spinbox.get())
    minutes = int(minute_spinbox.get())
    seconds = int(second_spinbox.get())
    total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds

def shutdown():
    shutdown_label.config(text="Shutting down...")
    time.sleep(1)  
    os.system("shutdown /s /t 1")

window.mainloop()
