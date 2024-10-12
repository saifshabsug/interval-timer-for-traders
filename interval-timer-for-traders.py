import tkinter as tk
import time
import threading
from datetime import datetime, timedelta
import os  # For playing sound
from tkinter import messagebox  # For showing alerts

# Timer intervals in seconds
intervals = {
    "1 Minute": 60,
    "5 Minutes": 5 * 60,
    "15 Minutes": 15 * 60,
    "30 Minutes": 30 * 60,
    "1 Hour": 60 * 60
}

# Track active toggles and their next trigger times
active_intervals = {}
next_trigger_times = {}

# Function to toggle an interval on/off with visual feedback (foreground color)
def toggle_interval(interval_name):
    now = datetime.now()
    
    if interval_name in active_intervals:
        del active_intervals[interval_name]
        del next_trigger_times[interval_name]
        toggle_buttons[interval_name].config(relief=tk.RAISED, fg="black")
        countdown_labels[interval_name].config(text="Not Active")
    else:
        active_intervals[interval_name] = True
        next_trigger_times[interval_name] = get_next_trigger_time(now, intervals[interval_name])
        toggle_buttons[interval_name].config(relief=tk.SUNKEN, fg="green")
        update_countdown(interval_name)

# Function to check the time and play sound if interval matches
def check_time():
    while True:
        now = datetime.now()
        for interval_name, interval_sec in intervals.items():
            if interval_name in active_intervals:
                if now >= next_trigger_times[interval_name]:
                    play_sound()
                    show_alert(interval_name, now)
                    next_trigger_times[interval_name] = get_next_trigger_time(now, interval_sec)
                update_countdown(interval_name)
        time.sleep(1)

# Function to get the next trigger time based on the current time and interval
def get_next_trigger_time(current_time, interval_seconds):
    # Calculate the next trigger time aligned with the system time
    current_minute = current_time.minute
    current_second = current_time.second

    interval_minutes = interval_seconds // 60
    # Find the next minute that is a multiple of the interval
    next_minute = (current_minute // interval_minutes + 1) * interval_minutes
    next_time = current_time.replace(minute=next_minute % 60, second=0, microsecond=0)

    # If next_minute exceeds 60, handle the hour change
    if next_minute >= 60:
        next_time = next_time + timedelta(hours=1)

    return next_time

# Function to update the countdown timer next to each button
def update_countdown(interval_name):
    now = datetime.now()
    time_left = next_trigger_times[interval_name] - now
    minutes, seconds = divmod(time_left.total_seconds(), 60)
    countdown_labels[interval_name].config(text=f"{int(minutes):02}:{int(seconds):02}")

# Function to play sound on both macOS and Windows
def play_sound():
    if os.name == 'posix':  # For macOS/Linux
        os.system('afplay /System/Library/Sounds/Glass.aiff')
    elif os.name == 'nt':  # For Windows
        import winsound
        winsound.Beep(3000, 2000)  # Frequency, duration

# Function to show an alert dialog in the app
def show_alert(interval_name, now):
    message = f"Interval {interval_name} hit at {now.strftime('%H:%M:%S')}"
    messagebox.showinfo("Interval Timer", message)
    print(message)

# Function to run the time checker in a separate thread
def start_time_checker():
    threading.Thread(target=check_time, daemon=True).start()

# Initialize main window
root = tk.Tk()
root.title("Interval Timer")
root.geometry("400x400")

# Create buttons for each interval with default appearance and countdown labels
toggle_buttons = {}
countdown_labels = {}

for interval_name in intervals:
    frame = tk.Frame(root)
    frame.pack(pady=5)

    # Button for each interval
    btn = tk.Button(frame, text=interval_name, width=15, font=("Arial", 12), relief=tk.RAISED, fg="black",
                    command=lambda name=interval_name: toggle_interval(name))
    btn.pack(side=tk.LEFT, padx=5)
    toggle_buttons[interval_name] = btn

    # Countdown label for each interval
    label = tk.Label(frame, text="Not Active", font=("Arial", 12))
    label.pack(side=tk.LEFT, padx=5)
    countdown_labels[interval_name] = label

# Start the timer check loop
start_time_checker()

# Start the Tkinter event loop
root.mainloop()