import tkinter as tk
from tkinter import ttk
import math
import matplotlib.pyplot as plt
import time

# Logs
logs = []

# Function to animate battery level change
def handle_test_charge_discharge():
    target_value = (battery_level['value'] + 10) % 110
    animate_battery_charge_discharge(target_value)

# Function to animate battery level
def animate_battery_charge_discharge(target_value):
    current_value = battery_level['value']
    if current_value < target_value:
        battery_level['value'] += 1
    elif current_value > target_value:
        battery_level['value'] -= 1
    else:
        # update color
        update_battery_color()
        # update label
        battery_level_label.config(text=f"Battery Level: {battery_level['value']}%")
        return
    # update color
    update_battery_color()
    # update label
    battery_level_label.config(text=f"Battery Level: {battery_level['value']}%")
    # repeat after 100 ms
    root.after(100, animate_battery_charge_discharge, target_value)

# Function to animate speed change
def handle_speedometer_test(increase=True):
    global speed
    target_speed = speed + 5 if increase else speed - 5
    animate_speedometer_change(target_speed)

# Function to animate speedometer break
def handle_speedometer_break():
    global speed
    target_speed = 0
    animate_speedometer_change(target_speed)

# Function to animate speedometer needle
def animate_speedometer_change(target_speed):
    global speed
    if speed < target_speed:
        speed += 1
    elif speed > target_speed:
        speed -= 1
    else:
        # update speedometer
        update_speedometer(speed)
        # log data
        log_data(speed=speed)
        return
    # update speedometer
    update_speedometer(speed)
    # log data
    log_data(speed=speed)
    # repeat after 100 ms
    root.after(100, animate_speedometer_change, target_speed)

# Function to update battery color
def update_battery_color():
    value = battery_level['value']
    if value > 70:
        color = 'light green'
    elif value > 30:
        color = 'yellow'
    else:
        color = 'red'
    battery_level.config(style=f'{color}.Horizontal.TProgressbar')

# Function to update the analog speedometer
def update_speedometer(speed):
    # Clear the canvas
    speedometer_canvas.delete("needle")
    # Dimensions
    x, y, r = 150, 150, 100
    # Angle calculation
    angle = math.radians(speed * 1.8 - 90)
    x2 = x + r * math.cos(angle)
    y2 = y + r * math.sin(angle)
    # Draw the needle
    speedometer_canvas.create_line(x, y, x2, y2, width=5, fill="red", tags="needle")
    # Update digital speedometer
    digital_speedometer.config(text=f"Speed: {speed} km/h")

# Function to log data
def log_data(speed=0, gear=1, rpm=0, break_status=False, accelerator_status=False, engine_status=False):
    logs.append({
        'speed': speed,
        'gear': gear,
        'rpm': rpm,
        'break_status': break_status,
        'accelerator_status': accelerator_status,
        'engine_status': engine_status
    })

# Function to plot logged data
def plot_data():
    speeds = [log['speed'] for log in logs]
    plt.plot(speeds, label='Speed (km/h)')
    plt.xlabel('Time')
    plt.ylabel('Speed')
    plt.title('Speed over Time')
    plt.legend()
    plt.show()

# Create the main window
root = tk.Tk()
root.title("eBike Testing GUI")

# Set a grid weight to make the layout responsive
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

# Use different frame styles
style = ttk.Style()
style.configure('TFrame', background='light gray')
style.configure('TLabel', background='light gray')
style.configure('TButton', background='light blue', font=('Arial', 12))
style.configure('TProgressbar', thickness=20, troughcolor='gray')
style.configure('red.Horizontal.TProgressbar', background='red')
style.configure('yellow.Horizontal.TProgressbar', background='yellow')
style.configure('light green.Horizontal.TProgressbar', background='light green')


# Frames
frame_charge_discharge = ttk.Frame(root, padding="10", style='TFrame')
frame_charge_discharge.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

frame_speedometer = ttk.Frame(root, padding="10", style='TFrame')
frame_speedometer.grid(column=1, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Labels
label_charge_discharge = ttk.Label(frame_charge_discharge, text="Charge/Discharge Testing", font=('Arial', 14))
label_charge_discharge.grid(column=0, row=0, sticky=tk.W)

label_speedometer = ttk.Label(frame_speedometer, text="Speedometer Testing", font=('Arial', 14))
label_speedometer.grid(column=0, row=0, sticky=tk.W)

# Battery Level
battery_level = ttk.Progressbar(frame_charge_discharge, orient="horizontal", length=200, mode="determinate")
battery_level.grid(column=0, row=1, sticky=(tk.W, tk.E))
battery_level['value'] = 50
battery_level_label = ttk.Label(frame_charge_discharge, text=f"Battery Level: {battery_level['value']}%", font=('Arial', 12))
battery_level_label.grid(column=0, row=2, sticky=(tk.W, tk.E))

# Buttons
btn_test_charge_discharge = ttk.Button(frame_charge_discharge, text="Test", command=handle_test_charge_discharge)
btn_test_charge_discharge.grid(column=0, row=3, sticky=(tk.W, tk.E))

# Speedometer Canvas
speedometer_canvas = tk.Canvas(frame_speedometer, width=300, height=300, bg='white')
speedometer_canvas.grid(column=0, row=1, sticky=(tk.W, tk.E))
speedometer_canvas.create_arc(10, 10, 290, 290, start=-60, extent=300, style=tk.ARC)

# Digital Speedometer
digital_speedometer = ttk.Label(frame_speedometer, text="Speed: 0 km/h", font=("Arial", 16))
digital_speedometer.grid(column=0, row=2, sticky=(tk.W, tk.E))

# Speedometer Test Buttons
speed = 0
btn_speedometer_increase_test = ttk.Button(frame_speedometer, text="Increase Speed", command=lambda: handle_speedometer_test(True))
btn_speedometer_increase_test.grid(column=0, row=3, sticky=(tk.W, tk.E))

btn_speedometer_decrease_test = ttk.Button(frame_speedometer, text="Decrease Speed", command=lambda: handle_speedometer_test(False))
btn_speedometer_decrease_test.grid(column=0, row=4, sticky=(tk.W, tk.E))

btn_speedometer_break = ttk.Button(frame_speedometer, text="Break", command=handle_speedometer_break)
btn_speedometer_break.grid(column=0, row=5, sticky=(tk.W, tk.E))

# Plot Button
btn_plot_data = ttk.Button(root, text="Plot Data", command=plot_data)
btn_plot_data.grid(column=0, row=1, sticky=(tk.W, tk.E), columnspan=2)

# Set main loop
root.mainloop()
