import tkinter as tk
from tkinter import ttk
import math
import matplotlib.pyplot as plt
import unittest
import time

class TestingGUI:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ABS | BatteryPack Tests GUI")
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # Variables
        self.event_log = []
        self.current_speed = 0
        self.battery_current_level = tk.IntVar(value=50)
        self.style = ttk.Style()
        self.style_configuration()

        #Check states

        self.battery_animation_in_progress = False  # Flag for battery level animation
        self.speed_animation_in_progress = False  # Flag for speedometer animation
        self.btn_test_battery_clicked = False  # Flag for battery test button
        self.btn_test_speed_clicked = False  # Flag for speed test button

        # Frames
        self.frame_charge_discharge = ttk.Frame(self.root, padding="10", style='TFrame')
        self.frame_charge_discharge.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.frame_speedometer = ttk.Frame(self.root, padding="10", style='TFrame')
        self.frame_speedometer.grid(column=1, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Battery Level
        self.battery_level = ttk.Progressbar(self.frame_charge_discharge, orient="horizontal", length=200, mode="determinate", variable=self.battery_current_level)
        self.battery_level.grid(column=0, row=1, sticky=(tk.W, tk.E))
        
        self.battery_level_label = ttk.Label(self.frame_charge_discharge, textvariable=self.battery_current_level, font=('Arial', 12))
        self.battery_level_label.grid(column=0, row=2, sticky=(tk.W, tk.E))

        # Buttons
        self.btn_test_charge_discharge = ttk.Button(self.frame_charge_discharge, text="Test", command=self.perform_test_battery_level)
        self.btn_test_charge_discharge.grid(column=0, row=3, sticky=(tk.W, tk.E))

        # Speedometer Canvas
        self.speedometer_canvas = tk.Canvas(self.frame_speedometer, width=300, height=300, bg='white')
        self.speedometer_canvas.grid(column=0, row=1, sticky=(tk.W, tk.E))
        self.speedometer_canvas.create_arc(10, 10, 290, 290, start=-60, extent=300, style=tk.ARC)

        # Digital Speedometer
        self.digital_speedometer = ttk.Label(self.frame_speedometer, text="Speed: 0 km/h", font=("Arial", 16))
        self.digital_speedometer.grid(column=0, row=2, sticky=(tk.W, tk.E))

        # Speedometer Test Buttons
        self.btn_speedometer_increase_test = ttk.Button(self.frame_speedometer, text="Increase Speed", command=lambda: self.perform_test_speed(True))
        self.btn_speedometer_increase_test.grid(column=0, row=3, sticky=(tk.W, tk.E))

        self.btn_speedometer_decrease_test = ttk.Button(self.frame_speedometer, text="Decrease Speed", command=lambda: self.perform_test_speed(False))
        self.btn_speedometer_decrease_test.grid(column=0, row=4, sticky=(tk.W, tk.E))

        self.btn_speedometer_break = ttk.Button(self.frame_speedometer, text="Break", command=self.perform_test_break)
        self.btn_speedometer_break.grid(column=0, row=5, sticky=(tk.W, tk.E))

        # Plot Button
        self.btn_plot_data = ttk.Button(self.root, text="Plot Data", command=self.plot_event_log)
        self.btn_plot_data.grid(column=0, row=1, sticky=(tk.W, tk.E), columnspan=2)

        self.root.mainloop()
        
    #styles - with||without execution is possible 
    def style_configuration(self):
        self.style.configure('TFrame', background='light gray')
        self.style.configure('TLabel', background='light gray')
        self.style.configure('TButton', background='light blue', font=('Arial', 12))
        self.style.configure('TProgressbar', thickness=20, troughcolor='gray')
        self.style.configure('red.Horizontal.TProgressbar', background='red')
        self.style.configure('yellow.Horizontal.TProgressbar', background='yellow')
        self.style.configure('light green.Horizontal.TProgressbar', background='light green')
        
    # Function to animate battery level UI
    def perform_test_battery_level(self):
        updated_level = (self.battery_current_level.get() + 10) % 110
        if self.battery_animation_in_progress:
            # Battery test button is clicked while battery animation in progress
            self.btn_test_battery_clicked = True
            return
        self.animate_battery_level_change(updated_level)

    # Function to animate battery level on the backend
    def animate_battery_level_change(self, updated_level):
        self.battery_animation_in_progress = True  # Set the flag to indicate battery animation is in progress
        current_level = self.battery_current_level.get()
        if current_level < updated_level:
            self.battery_current_level.set(current_level + 1)
            
        elif current_level > updated_level:
            self.battery_current_level.set(current_level - 1)
        else:
            # Animation is complete, reset the flag
            self.battery_animation_in_progress = False

            # Check if the button was clicked during the animation
            if self.btn_test_battery_clicked:
                self.btn_test_battery_clicked = False
                self.perform_test_battery_level()
            return
        self.root.after(100, self.animate_battery_level_change, updated_level)

    # Function to animate speed UI
    def perform_test_speed(self, increase=True):
        target_speed = self.current_speed + 5 if increase else max(self.current_speed - 5, 0)

        if self.speed_animation_in_progress:
            # Speed test button is clicked while speedometer animation in progress
            self.btn_test_speed_clicked = True
            return

        self.animate_speed_change(target_speed)

    # Function to animate speedometer break
    def perform_test_break(self):
        self.animate_speed_change(0)

    # Function to animate speedometer needle
    def animate_speed_change(self, target_speed):
        self.speed_animation_in_progress = True  # Set the flag to indicate speedometer animation is in progress

        if self.current_speed < target_speed:
            self.current_speed += 1
        elif self.current_speed > target_speed:
            self.current_speed -= 1
        else:
            # Animation is complete, reset the flag
            self.speed_animation_in_progress = False

            # Check if the button was clicked during the animation
            if self.btn_test_speed_clicked:
                self.btn_test_speed_clicked = False
                self.perform_test_speed()
            #update speedometer and log data
            self.update_speed_indicator()
            self.log_event(speed=self.current_speed)
            return
        self.update_speed_indicator()
        self.log_event(speed=self.current_speed)
         # repeat after 100 ms
        self.root.after(100, self.animate_speed_change, target_speed)

    # Function to update the analog speedometer
    def update_speed_indicator(self):
        #clear canvas
        self.speedometer_canvas.delete("needle")
        #dimensions
        x, y, r = 150, 150, 100
        # Angle calculation
        angle = math.radians(self.current_speed * 1.8 - 90)
        x2 = x + r * math.cos(angle)
        y2 = y + r * math.sin(angle)
        # Draw the needle
        self.speedometer_canvas.create_line(x, y, x2, y2, width=5, fill="red", tags="needle")
        # Update digital speedometer
        self.digital_speedometer.config(text=f"Speed: {self.current_speed} km/h")

    # Function to log data
    def log_event(self, speed=0, gear=1, rpm=0, break_status=False, accelerator_status=False, engine_status=False):
        self.event_log.append({
            'speed': speed,
            'gear': gear,
            'rpm': rpm,
            'break_status': break_status,
            'accelerator_status': accelerator_status,
            'engine_status': engine_status
        })

    # Function to plot logged data
    def plot_event_log(self):
        speeds = [event['speed'] for event in self.event_log]
        plt.plot(speeds, label='Speed (km/h)')
        plt.xlabel('Time')
        plt.ylabel('Speed')
        plt.title('Speed over Time')
        plt.legend()
        plt.show()


if __name__ == '__main__':
    TestingGUI()



"""TEST WITH UNITTESTS


import unittest

class TestGUI(unittest.TestCase):
    def setUp(self):
        # Initialize variables and states
        self.current_speed = 0
        self.battery_current_level = {'value': 50}
    
    def test_perform_test_battery_level(self):
        # Perform the function
        perform_test_battery_level()
        # Assert that the battery_current_level has been updated
        self.assertNotEqual(self.battery_current_level['value'], 50)

    def test_perform_test_speed(self):
        # Perform the function
        perform_test_speed(True)
        # Assert that the current_speed has been updated
        self.assertNotEqual(self.current_speed, 0)

    def test_perform_test_break(self):
        # Perform the function
        perform_test_break()
        # Assert that the current_speed is now 0
        self.assertEqual(self.current_speed, 0)

# Run the tests
if __name__ == '__main__':
    unittest.main()



"""
