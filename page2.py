#file  -- page2.py --
import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Style
#from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from datetime import datetime
#import paho.mqtt.client as mqtt
from datetime import time
import time
#import numpy as np
from time import strftime


class Page2(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        # Create a parent frame to hold the border frame and table side by side
        self.side_frame = tk.Frame(self)
        self.side_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Create a frame for the border (current time and title)
        self.border_frame = tk.Frame(self.side_frame, padx=10, pady=10, highlightbackground="black", highlightthickness=2)
        self.border_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True,padx=(0,10))

        # Add title for Page 2
        self.page2_title = tk.Label(self.border_frame, text="Brightness Sensor", font=('Arial', 14, 'bold'), bg='DeepSkyBlue4', fg='white', padx=10, pady=10)
        self.page2_title.pack(fill=tk.X, pady=(10, 10))

        # Create a rectangle frame for current time with additional space
        self.time_frame = tk.Frame(self.border_frame, bg='MistyRose2', height=40, highlightbackground="black", highlightthickness=1)
        self.time_frame.pack(fill=tk.X, pady=(10, 10))

        # Label to display current time
        self.time_label = tk.Label(self.time_frame, text="", font=('Arial', 12), bg='MistyRose2')
        self.time_label.pack(pady=5, padx=10)

        # Create a frame for the table
        self.table_frame = tk.Frame(self.side_frame, padx=10, pady=10)
        self.table_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create the treeview table
        self.create_treeview()

        # Frame for the brightness range indicators
        self.range_frame = tk.Frame(self.border_frame)
        self.range_frame.pack(pady=10, fill=tk.X)

        # Brightness range frames
        self.dims_frame = tk.Frame(self.range_frame, bg='snow2', height=30, highlightbackground="black", highlightthickness=1)
        self.dims_frame.grid(row=0, column=0, padx=(0,5), pady=5, sticky="ew")
        self.dims_label = tk.Label(self.dims_frame, text="Dim (0-400)", bg='snow2')
        self.dims_label.pack(pady=5)

        self.normal_frame = tk.Frame(self.range_frame, bg='snow2', height=30, highlightbackground="black", highlightthickness=1)
        self.normal_frame.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.normal_label = tk.Label(self.normal_frame, text="Normal (401-800)", bg='snow2')
        self.normal_label.pack(pady=5)

        self.bright_frame = tk.Frame(self.range_frame, bg='snow2', height=30, highlightbackground="black", highlightthickness=1)
        self.bright_frame.grid(row=0, column=2, padx=(5,0), pady=5, sticky="ew")
        self.bright_label = tk.Label(self.bright_frame, text="Too Bright (801-1023)", bg='snow2')
        self.bright_label.pack(pady=5)

        # Configure grid weights to ensure equal column width
        self.range_frame.grid_columnconfigure(0, weight=1)
        self.range_frame.grid_columnconfigure(1, weight=1)
        self.range_frame.grid_columnconfigure(2, weight=1)


        # Create a frame for the bar meter and the color indicator/text info
        self.bar_color_frame = tk.Frame(self.border_frame)
        self.bar_color_frame.pack(pady=10, fill=tk.X)

        # Frame for the bar meter
        self.bar_meter_frame = tk.Frame(self.bar_color_frame, padx=10, pady=10, height=200)  # Adjust the height as needed
        self.bar_meter_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(100,10))

        self.bar_meter_label = tk.Label(self.bar_meter_frame, text="Brightness Level", font=('Arial', 12))
        self.bar_meter_label.pack()

        self.bar_meter = ttk.Progressbar(self.bar_meter_frame, orient="horizontal", length=900, mode="determinate")
        self.bar_meter.pack(pady=10)

        # Frame to hold min, max, and current labels
        self.labels_frame = tk.Frame(self.bar_meter_frame)
        self.labels_frame.pack(fill=tk.X)

        # Labels for min and max values
        self.brightness_min_label = tk.Label(self.labels_frame, text="Min: 0", font=('Arial', 10))
        self.brightness_min_label.pack(side=tk.LEFT, padx=10)

        self.brightness_max_label = tk.Label(self.labels_frame, text="Max: 1023", font=('Arial', 10))
        self.brightness_max_label.pack(side=tk.RIGHT, padx=10)

        # Label for the current brightness value
        self.brightness_current_label = tk.Label(self.bar_meter_frame, text="Current Brightness: N/A", font=('Arial', 10))
        self.brightness_current_label.pack(pady=5)

        # Set range for the bar meter
        self.bar_meter['maximum'] = 1024

        # Frame to hold the color indicator and text info
        self.color_text_frame = tk.Frame(self.bar_color_frame, padx=10, pady=10)
        self.color_text_frame.pack(side=tk.LEFT, padx=10)
        
        # Canvas to indicate brightness level with a circle
        self.canvas = tk.Canvas(self.color_text_frame, width=100, height=100)
        self.canvas.pack(pady=0)

        self.circle = self.canvas.create_oval(10, 10, 90, 90, fill='white', outline='black')

        # Box to show text information
        self.text_info_frame = tk.Frame(self.color_text_frame, width=100, height=100)
        self.text_info_frame.pack(pady=10)

        self.text_info_label = tk.Label(self.text_info_frame, text="N/A", font=('Arial', 10))
        self.text_info_label.pack(expand=True)

        # Add a Matplotlib figure for the graph
        self.fig = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Brightness Level Over Time\n")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Brightness Level")
        self.line, = self.ax.plot([], [], lw=2)
        self.ax.grid(True)

        self.graph_canvas = FigureCanvasTkAgg(self.fig, master=self.border_frame)
        self.graph_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Data list for storing brightness values over time
        self.data = []
        self.timestamps = []

        # Start updating the time display
        self.update_time()

    def create_treeview(self):
        self.tree = ttk.Treeview(self.table_frame, style="Treeview")
        self.tree["columns"] = ("Data Number", "Time", "Value")
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("Data Number", anchor=tk.CENTER, width=80)
        self.tree.column("Time", anchor=tk.CENTER, width=150)
        self.tree.column("Value", anchor=tk.CENTER, width=150)
        self.tree.heading("Data Number", text="No.")
        self.tree.heading("Time", text="Time")
        self.tree.heading("Value", text="Data Value")

        tree_scroll = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        style = ttk.Style()
        style.configure("Treeview", rowheight=25, font=('Arial', 12), background="azure", foreground="black", fieldbackground="white")
        style.configure("Treeview.Heading", font=('Arial', 12, 'bold'))
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

    def update_light_sensor_value(self, data):
        print(f"Updating light sensor value: {data}")  # Debug print statement

        # Update treeview with new data
        self.tree.insert("", tk.END, values=(int (len(self.data)/2)+1, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), data))

        # Update brightness level
        self.bar_meter['value'] = data
        self.brightness_current_label.config(text=f"Current Brightness: {data}")

        # Update color indicator
        color = 'snow2'  # Default color
        if data <= 400:
            color = 'blue'
            self.dims_frame.config(bg='lightblue')
            self.normal_frame.config(bg='snow2')
            self.bright_frame.config(bg='snow2')
        elif 401 <= data <= 800:
            color = 'green'
            self.dims_frame.config(bg='snow2')
            self.normal_frame.config(bg='lightgreen')
            self.bright_frame.config(bg='snow2')
        else:
            color = 'red'
            self.dims_frame.config(bg='snow2')
            self.normal_frame.config(bg='snow2')
            self.bright_frame.config(bg='lightcoral')

        self.canvas.itemconfig(self.circle, fill=color)

        # Update graph
        self.update_graph(data)

        # Update text info
        self.update_text_info(data)

    def update_graph(self, data):
        self.timestamps.append(datetime.now().strftime("%H:%M:%S"))
        self.data.append(data)

        if len(self.data) > 100:  # Limit the number of data points displayed
            self.data.pop(0)
            self.timestamps.pop(0)

        # Update graph with new data
        self.timestamps.append(datetime.now().strftime('%H:%M:%S'))
        self.data.append(data)
        self.ax.clear()
        self.ax.plot(self.timestamps, self.data, lw=2, marker='x')  # Add marker to visualize points
        self.ax.set_title("Brightness Level Over Time\n")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Brightness Level")
        self.ax.grid(True)
        self.graph_canvas.draw()

    def update_text_info(self, data):
        if data <= 400:
            text = "Dim"
        elif 401 <= data <= 800:
            text = "Normal"
        else:
            text = "Too Bright"
        self.text_info_label.config(text=text)

    def update_time(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=f"Current Time: {now}")
        self.after(1000, self.update_time)  # Update time every second
