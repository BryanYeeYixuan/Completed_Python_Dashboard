import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Style
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from datetime import datetime
import paho.mqtt.client as mqtt
from datetime import time
import time
import numpy as np
from time import strftime


# MQTT broker details
# broker_address = "broker.emqx.io"
broker_address = "broker.hivemq.com"
broker_port = 1883

# Create an MQTT client instance
client = mqtt.Client()

# Variables to store received messages
received_message_page1 = 0.0
received_message_page2 = 0.0

class Page1(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.data_counter = 0
        self.data_points = []
        self.timestamps = []

        # Create frames for graphs, current value, total data, and table
        self.create_frames()

        # Create plots
        self.create_plots()

        # Create labels for current value and total data
        self.create_labels()

        # Create Treeview for displaying data
        self.create_treeview()

    def create_frames(self):
        self.graphs_frame = tk.Frame(self, highlightbackground="black", highlightcolor="black", highlightthickness=2)
        self.graphs_frame.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.BOTH, expand=True)

        self.current_frame = tk.Frame(self, bg='white', padx=10, pady=10)
        self.current_frame.pack(pady=(20, 10), padx=20, side=tk.TOP, fill=tk.BOTH, expand=False)

        self.total_frame = tk.Frame(self, bg='white', padx=10, pady=10)
        self.total_frame.pack(pady=10, padx=20, side=tk.TOP, fill=tk.BOTH, expand=False)

        self.table_frame = ttk.Frame(self)
        self.table_frame.pack(pady=20, padx=20, side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def create_plots(self):
        # Add colored title above the graphs, aligned with the graph frame
        title_label = tk.Label(self.graphs_frame, text="Graphs Overview", font=('Arial', 14, 'bold'),
                               bg='SeaGreen3', fg='white', padx=10, pady=10)
        title_label.pack(fill=tk.X, padx=20, pady=(20, 0))

        self.fig = Figure(figsize=(10, 12), dpi=100)

        # Scatter plot (plot1)
        self.plot1 = self.fig.add_subplot(211)
        self.plot1.set_ylim(0, 250)
        self.plot1.set_xlim(0, 10)
        self.plot1.set_xlabel('Number of Data')
        self.plot1.set_ylabel('Distance (cm)')
        self.plot1.set_title('Scatter Plot', pad=10)
        self.plot1.grid(True)

        # Line plot (plot2)
        self.plot2 = self.fig.add_subplot(212)
        self.plot2.set_ylim(0, 250)
        self.plot2.set_xlim(0, 10)
        self.plot2.set_xlabel('Number of Data')
        self.plot2.set_ylabel('Value')
        self.plot2.set_title('Line Plot', pad=10)
        self.plot2.grid(True)

        self.fig.subplots_adjust(hspace=0.6)

        # Create line objects for plot2
        self.line2d_plot2, = self.plot2.plot([], [], marker='x', color='blue', linestyle='-', label='Value')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graphs_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(pady=20, padx=20, side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(self.canvas, self.graphs_frame)
        toolbar.update()
        toolbar.pack(pady=20, padx=20, side=tk.TOP, fill=tk.X)

    def create_labels(self):
        self.current_label = tk.Label(self.current_frame, text="Current Value: N/A", font=('Arial', 12), bg='white')
        self.current_label.pack()

        self.total_label = tk.Label(self.total_frame, text="Total Data: 0", font=('Arial', 12), bg='white')
        self.total_label.pack()

    def create_treeview(self):
        self.tree = ttk.Treeview(self.table_frame, style="Treeview")
        self.tree["columns"] = ("Data Number", "Time", "Value")
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("Data Number", anchor=tk.CENTER, width=100)
        self.tree.column("Time", anchor=tk.CENTER, width=200)
        self.tree.column("Value", anchor=tk.CENTER, width=200)
        self.tree.heading("Data Number", text="No.")
        self.tree.heading("Time", text="Time")
        self.tree.heading("Value", text="Data Value")

        tree_scroll = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        style = Style()
        style.configure("Treeview", rowheight=25, font=('Arial', 12), background="white", foreground="black", fieldbackground="white")
        style.configure("Treeview.Heading", font=('Arial', 12, 'bold'))
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

    def update_plot(self, data):
        try:
            self.data_counter += 1
            self.data_points.append(data)

            self.plot1.plot([self.data_counter], [data], marker='o', markersize=5, color="red")
            self.plot1.set_xlim(0, self.data_counter + 1)

            if self.data_counter > len(self.timestamps):
                self.timestamps.append(datetime.now().strftime('%H:%M:%S'))
                self.plot1.set_xticks(range(1, self.data_counter + 1))
                self.plot1.set_xticklabels(self.timestamps, rotation=30, ha='right')
            else:
                self.plot1.set_xticks(range(1, len(self.timestamps) + 1))
                self.plot1.set_xticklabels(self.timestamps, rotation=30, ha='right')

            x_data = list(self.line2d_plot2.get_xdata()) + [self.data_counter]
            y_data = list(self.line2d_plot2.get_ydata()) + [data]

            self.line2d_plot2.set_data(x_data, y_data)
            self.plot2.relim()
            self.plot2.autoscale_view(True, True, True)
            self.plot2.set_xlim(0, self.data_counter + 1)

            if self.data_counter > len(self.timestamps):
                self.timestamps.append(datetime.now().strftime('%H:%M:%S'))
                self.plot2.set_xticks(range(1, self.data_counter + 1))
                self.plot2.set_xticklabels(self.timestamps, rotation=30, ha='right')
            else:
                self.plot2.set_xticks(range(1, len(self.timestamps) + 1))
                self.plot2.set_xticklabels(self.timestamps, rotation=30, ha='right')

            self.canvas.draw()

            data_number = len(self.timestamps)
            self.tree.insert("", "end", values=(data_number, self.timestamps[-1], data))

            self.current_label.config(text=f"Current Value: {data}")
            self.total_label.config(text=f"Total Data: {self.data_counter}")

        except Exception as e:
            print("Error updating plot:", e)

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

class Page3(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.MainBox_frame = tk.Frame(self, highlightbackground="black", highlightcolor="black", highlightthickness=2)
        self.MainBox_frame.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.BOTH, expand=True)

        self.page3_title = tk.Label(self.MainBox_frame, text="Water Level Data", font=('Arial', 14, 'bold'), bg='mediumpurple3', fg='white', padx=10, pady=10)
        self.page3_title.pack(fill=tk.X, padx=50, pady=(20, 0))

        # Parent frame to hold the graphs and the dashboard bars
        self.main_frame = tk.Frame(self.MainBox_frame)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Parent frame to hold the graphs and the dashboard bars
        self.main2_frame = tk.Frame(self.MainBox_frame)
        self.main2_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Frame for the dashboard bars
        self.dashboard_frame = tk.Frame(self.main_frame)
        self.dashboard_frame.pack(side=tk.TOP, padx=0, pady=0, anchor='n')

        # Frame for the first circular progress bar, value, and arrow
        self.circular_frame1 = tk.Frame(self.dashboard_frame, bg='white', padx=0, pady=0, borderwidth=2, relief='groove')
        self.circular_frame1.pack(side=tk.LEFT, padx=(30,40), pady=(10, 20), anchor='n')

        self.frame1_title = tk.Label(self.circular_frame1, text="WATER SENSOR 1", font=('Helvetica', 9, 'bold'), bg='white', fg='Grey')
        self.frame1_title.place(x=10, y=5)

        # Bottom strip in circular_frame1 using Canvas
        self.bottom_strip1 = tk.Canvas(self.circular_frame1, height=2, bg='DeepSkyBlue4', bd=0, highlightthickness=0)
        self.bottom_strip1.pack(side=tk.BOTTOM, fill=tk.X, pady=0)
        self.bottom_strip1.create_line(0, 0, 1000, 0, fill='DeepSkyBlue4')

        self.arrow_label1 = tk.Label(self.circular_frame1, text="▲", font=('Arial', 15, 'bold'), padx=0, fg='grey', bg='white')
        self.arrow_label1.pack(side=tk.LEFT, pady=(30, 0), padx=(20, 5))

        self.value_label1 = tk.Label(self.circular_frame1, text="0 cm", font=('Arial', 15, 'bold'), padx=0, bg='white')
        self.value_label1.pack(side=tk.LEFT, pady=(30, 0))

        self.circular_bar1 = CircularProgressBar(self.circular_frame1, size=80, thickness=8, color="DeepSkyBlue4")
        self.circular_bar1.pack(side=tk.RIGHT, padx=10)
        self.circular_bar1.set_value(0)

        # Frame for the second circular progress bar, value, and arrow
        self.circular_frame2 = tk.Frame(self.dashboard_frame, bg='white', padx=0, pady=0, borderwidth=2, relief='groove')
        self.circular_frame2.pack(side=tk.LEFT, padx=(0,40), pady=(10, 20), anchor='n')

        self.frame2_title = tk.Label(self.circular_frame2, text="WATER SENSOR 2", font=('Helvetica', 9, 'bold'), bg='white', fg='grey')
        self.frame2_title.place(x=10, y=5)

        # Bottom strip in circular_frame2 using Canvas
        self.bottom_strip2 = tk.Canvas(self.circular_frame2, height=2, bg='red', bd=0, highlightthickness=0)
        self.bottom_strip2.pack(side=tk.BOTTOM, fill=tk.X, pady=0)
        self.bottom_strip2.create_line(0, 0, 1000, 0, fill='red')

        self.arrow_label2 = tk.Label(self.circular_frame2, text="▲", font=('Arial', 15, 'bold'), padx=0, fg='gray', bg='white')
        self.arrow_label2.pack(side=tk.LEFT, pady=(30, 0), padx=(20, 5))

        self.value_label2 = tk.Label(self.circular_frame2, text="0 cm", font=('Arial', 15, 'bold'), padx=0, bg='white')
        self.value_label2.pack(side=tk.LEFT, pady=(30, 0))

        self.circular_bar2 = CircularProgressBar(self.circular_frame2, size=80, thickness=8, color="red")
        self.circular_bar2.pack(side=tk.RIGHT, padx=10)
        self.circular_bar2.set_value(0)

        # Frame for the total value of sensor 1 and sensor 2
        self.total_value_frame = tk.Frame(self.dashboard_frame, bg='white', padx=0, pady=0, borderwidth=2, relief='groove')
        self.total_value_frame.pack(side=tk.LEFT, padx=(0,40), pady=(10, 20), anchor='n')

        self.total_status_indicator = StatusIndicator(self.total_value_frame, size=15)
        self.total_status_indicator.place(x=5, y=5)

        self.total_frame_title = tk.Label(self.total_value_frame, text="TOTAL VALUE", font=('Helvetica', 9, 'bold'), bg='white', fg='Grey')
        self.total_frame_title.place(x=25, y=5)
        
        # Bottom strip in total_value_frame using Canvas
        self.bottom_strip_total = tk.Canvas(self.total_value_frame, height=2, bg='DeepSkyBlue4', bd=0, highlightthickness=0)
        self.bottom_strip_total.pack(side=tk.BOTTOM, fill=tk.X, pady=0)
        self.bottom_strip_total.create_line(0, 0, 1000, 0, fill='DeepSkyBlue4')


        self.total_arrow_label = tk.Label(self.total_value_frame, text="▲", font=('Arial', 15, 'bold'), fg='grey', bg='white')
        self.total_arrow_label.pack(side=tk.LEFT, pady=(45, 10), padx=(20, 5))

        self.total_value_label = tk.Label(self.total_value_frame, text="0.0 cm", font=('Helvetica', 15, 'bold'), bg='white', fg='grey')
        self.total_value_label.pack(pady=(45, 10), padx=(0, 25), side=tk.LEFT)

        self.total_status_label = tk.Label(self.total_value_frame, text="Unactivated", font=('Helvetica', 12, 'bold'), bg='white', fg='red')
        self.total_status_label.pack(pady=(45, 10), side=tk.RIGHT, padx=(10, 15))

        # Frame for the average value of sensor 1 and sensor 2
        self.average_value_frame = tk.Frame(self.dashboard_frame, bg='white', padx=0, pady=0, borderwidth=2, relief='groove')
        self.average_value_frame.pack(side=tk.LEFT, padx=(0,30), pady=(10, 20), anchor='n')

        self.average_status_indicator = StatusIndicator(self.average_value_frame, size=15)
        self.average_status_indicator.place(x=5, y=5)

        self.average_frame_title = tk.Label(self.average_value_frame, text="AVERAGE VALUE", font=('Helvetica', 9, 'bold'), bg='white', fg='Grey')
        self.average_frame_title.place(x=25, y=5)
        
        # Bottom strip in average_value_frame using Canvas
        self.bottom_strip_average = tk.Canvas(self.average_value_frame, height=2, bg='DeepSkyBlue4', bd=0, highlightthickness=0)
        self.bottom_strip_average.pack(side=tk.BOTTOM, fill=tk.X, pady=0)
        self.bottom_strip_average.create_line(0, 0, 1000, 0, fill='DeepSkyBlue4')

        self.average_arrow_label = tk.Label(self.average_value_frame, text="▲", font=('Arial', 15, 'bold'), fg='grey', bg='white')
        self.average_arrow_label.pack(side=tk.LEFT, pady=(45, 10), padx=(20, 5))

        self.average_value_label = tk.Label(self.average_value_frame, text="0.0 cm", font=('Helvetica', 15, 'bold'), bg='white', fg='grey')
        self.average_value_label.pack(pady=(45, 10), padx=(0, 25), side=tk.LEFT)

        self.average_status_label = tk.Label(self.average_value_frame, text="Unactivated", font=('Helvetica', 12, 'bold'), bg='white', fg='red')
        self.average_status_label.pack(pady=(45, 10), side=tk.RIGHT, padx=(10, 15))

        # Frame for the graphs
        self.graph_frame = tk.Frame(self.main_frame, bg='white', borderwidth=2, relief='groove')
        self.graph_frame.pack(side=tk.LEFT, padx=(40,40), pady=(5,0), anchor='n')
        
        # Title for the graph
        self.graph_title = tk.Label(self.graph_frame, text="Graph Data", font=('Helvetica', 12, 'bold'), bg='white', fg='grey')
        self.graph_title.pack(side=tk.TOP, anchor='nw', padx=(10,0), pady=10)

        # Add LineGraphs to the graph_frame
        self.graph1 = LineGraph(self.graph_frame)
        self.graph1.pack(side=tk.TOP, padx=(0,20), pady=10)

        # Frame for the bargraph
        self.bar_frame = tk.Frame(self.main_frame, bg='white', borderwidth=2, relief='groove')
        self.bar_frame.pack(side=tk.LEFT, padx=(0,40), pady=(5,5), anchor='n')

        # Title for the bar
        self.bar_title = tk.Label(self.bar_frame, text="The Water Level", font=('Helvetica', 12, 'bold'), bg='white', fg='grey')
        self.bar_title.pack(side=tk.TOP, anchor='nw', padx=(10,0), pady=(10,0))

        # Add BarGraph to the bar_frame
        self.bar_graph = BarGraph(self.bar_frame)
        self.bar_graph.pack(side=tk.TOP, padx=(10,20), pady=0)
        
        # Frame for the graphs
        self.sensorgraph_frame = tk.Frame(self.main2_frame, bg='', borderwidth=2, relief='groove')
        self.sensorgraph_frame.pack(side=tk.LEFT, padx=20, pady=20, anchor='n')

        # Frame for Sensor 1's line graph
        self.sensor1_graph_frame = tk.Frame(self.sensorgraph_frame, bg='white', borderwidth=2, relief='groove')
        self.sensor1_graph_frame.pack(side=tk.LEFT, padx=(15,10), pady=(0,0), anchor='n')

        # Thinner bottom strip
        self.bottom_strip = tk.Frame(self.sensor1_graph_frame, bg='blue', height=2)  # Changed height to 5
        self.bottom_strip.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Title for the graph
        self.graph_title = tk.Label(self.sensor1_graph_frame, text="Water Sensor 1", font=('Helvetica', 12, 'bold'), bg='white', fg='grey')
        self.graph_title.pack(side=tk.TOP, anchor='nw', padx=(15,0), pady=10)

        self.sensor1_value_label = tk.Label(self.sensor1_graph_frame, text="0 cm", font=('Helvetica', 35, 'bold'), bg='white')
        self.sensor1_value_label.pack(side=tk.TOP, pady=(15,0))

        self.sensor1_graph = LineGraph_Sensors(self.sensor1_graph_frame)
        self.sensor1_graph.pack(fill=tk.BOTH, expand=True)

        # Frame for Sensor 2's line graph
        self.sensor2_graph_frame = tk.Frame(self.sensorgraph_frame, bg='white', borderwidth=2, relief='groove')
        self.sensor2_graph_frame.pack(side=tk.LEFT, padx=(15,10), pady=(0,0), anchor='n')

        # Thinner bottom strip
        self.bottom_strip = tk.Frame(self.sensor2_graph_frame, bg='red', height=2)  # Changed height to 5
        self.bottom_strip.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Title for the graph
        self.graph_title = tk.Label(self.sensor2_graph_frame, text="Water Sensor 2", font=('Helvetica', 12, 'bold'), bg='white', fg='grey')
        self.graph_title.pack(side=tk.TOP, anchor='nw', padx=(15,0), pady=10)

        self.sensor2_value_label = tk.Label(self.sensor2_graph_frame, text="0 cm", font=('Helvetica', 35, 'bold'), bg='white')
        self.sensor2_value_label.pack(side=tk.TOP, pady=(15,0))

        self.sensor2_graph = LineGraph_Sensors(self.sensor2_graph_frame)
        self.sensor2_graph.pack(fill=tk.BOTH, expand=True)
        
        # Create the table frame with a border
        self.table_frame = tk.Frame(self.main2_frame, bg='white', borderwidth=2, relief='groove')
        self.table_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(3,35), pady=(23,25))

        self.table = ttk.Treeview(self.table_frame, columns=('No.', 'Time', 'Sensor 1', 'Sensor 2'), show='headings')
        self.table.heading('No.', text='No.')
        self.table.heading('Time', text='Time')
        self.table.heading('Sensor 1', text='Sensor 1')
        self.table.heading('Sensor 2', text='Sensor 2')

        # Optionally adjust column widths
        self.table.column('No.', width=50, anchor='center')
        self.table.column('Time', width=100, anchor='center')
        self.table.column('Sensor 1', width=100, anchor='center')
        self.table.column('Sensor 2', width=100, anchor='center')

        self.table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add a vertical scrollbar to the table
        self.scrollbar = ttk.Scrollbar(self.table_frame, orient='vertical', command=self.table.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.table.configure(yscrollcommand=self.scrollbar.set)
        

        # Initialize previous values for comparison
        self.prev_value1 = 0
        self.prev_value2 = 0

    def update_progress1(self, value):
        if value > self.prev_value1:
            arrow_text = "▲"
            arrow_color = "green"
        elif value < self.prev_value1:
            arrow_text = "▼"
            arrow_color = "red"
        else:
            arrow_text = self.arrow_label1.cget("text")
            arrow_color = self.arrow_label1.cget("fg")

        self.prev_value1 = value
        self.circular_bar1.set_value(value)
        self.value_label1.config(text=f"{value} cm")
        self.arrow_label1.config(text=arrow_text, fg=arrow_color)
        self.update_total_and_average()
        self.update_table()  # Update the table with new data
        self.graph1.update_graph(value, self.prev_value2)  # Update with current timestamp
        self.bar_graph.update_bar(value, self.prev_value2)  # Update bar graph
        self.sensor1_graph.update_graph2(value)  # Update with current timestamp
        self.sensor1_value_label.config(text=f"{value} cm")  # Update current value label

    def update_progress2(self, value):
        if value > self.prev_value2:
            arrow_text = "▲"
            arrow_color = "green"
        elif value < self.prev_value2:
            arrow_text = "▼"
            arrow_color = "red"
        else:
            arrow_text = self.arrow_label2.cget("text")
            arrow_color = self.arrow_label2.cget("fg")

        self.prev_value2 = value
        self.circular_bar2.set_value(value)
        self.value_label2.config(text=f"{value} cm")
        self.arrow_label2.config(text=arrow_text, fg=arrow_color)
        self.update_total_and_average()
        self.update_table()  # Update the table with new data
        self.graph1.update_graph(self.prev_value1, value)  # Update with current timestamp
        self.bar_graph.update_bar(self.prev_value1, value)  # Update bar graph
        self.sensor2_graph.update_graph3(value)  # Update with current timestamp
        self.sensor2_value_label.config(text=f"{value} cm")  # Update current value label

    def update_total_and_average(self):
        value1 = self.prev_value1
        value2 = self.prev_value2

        total = value1 + value2
        average = total / 2

        total_text = f"{total:.1f} cm"
        average_text = f"{average:.1f} cm"

        self.total_value_label.config(text=total_text)
        self.average_value_label.config(text=average_text)

        if total > 0:
            self.total_status_label.config(text="Activated", fg="green")
            self.total_status_indicator.set_status(True)
        else:
            self.total_status_label.config(text="Unactivated", fg="red")
            self.total_status_indicator.set_status(False)

        if average > 0:
            self.average_status_label.config(text="Activated", fg="green")
            self.average_status_indicator.set_status(True)
        else:
            self.average_status_label.config(text="Unactivated", fg="red")
            self.average_status_indicator.set_status(False)
            
    def update_table(self):
        # Get the current timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")  # Use datetime.now() for the current time
        no = self.table.get_children().__len__() + 1  # Get the current row number

        # Insert the data into the table
        self.table.insert('', 'end', values=(no, timestamp, self.prev_value1, self.prev_value2))

class CircularProgressBar(tk.Canvas):
    def __init__(self, parent, size=150, thickness=10, max_value=1000, color="DeepSkyBlue4", *args, **kwargs):
        super().__init__(parent, width=size, height=size, bg='white', *args, **kwargs, highlightbackground="white")
        self.size = size
        self.thickness = thickness
        self.max_value = max_value
        self.value = 0
        self.color = color

    def set_value(self, value):
        self.value = value
        self.draw_circle()

    def draw_circle(self):
        self.delete("all")
        angle = 360 * (self.value / self.max_value)
        extent = angle

        self.create_oval(self.thickness, self.thickness, self.size - self.thickness, self.size - self.thickness,
                         outline="#DDDDDD", width=self.thickness)
        self.create_arc(self.thickness, self.thickness, self.size - self.thickness, self.size - self.thickness,
                        start=90, extent=-extent, style=tk.ARC, outline=self.color, width=self.thickness)

        # Calculate and display the percentage in the middle of the circle
        percentage = (self.value / self.max_value) * 100
        self.create_text(self.size / 2, self.size / 2, text=f"{percentage:.1f}%", fill="black", font=('Arial', int(self.size/10), 'bold'))

class StatusIndicator(tk.Canvas):
    def __init__(self, parent, size=10, color='red', *args, **kwargs):
        super().__init__(parent, width=size, height=size, bg='white', *args, **kwargs, highlightthickness=0)
        self.size = size
        self.color = color
        self.draw_circle()

    def draw_circle(self):
        self.delete("all")
        self.create_oval(0, 0, self.size, self.size, fill=self.color, outline=self.color)

    def set_status(self, active):
        self.color = 'green' if active else 'red'
        self.draw_circle()

class LineGraph(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        # Create a figure and axis for the plot
        self.figure, self.ax = plt.subplots(figsize=(10.6, 3.8), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

        # Initialize data lists for two data sets
        self.timestamps = []  # Data for timestamps
        self.y_data1 = []  # Data for Sensor 1
        self.y_data2 = []  # Data for Sensor 2

        # Set axis labels and grid
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Value')
        self.ax.grid(True)

    def update_graph(self, y1, y2=None):
        # Get the current timestamp
        current_time = datetime.now().strftime('%H:%M:%S')
        
        # Append the current timestamp and data
        self.timestamps.append(current_time)
        self.y_data1.append(y1)
        if y2 is not None:
            self.y_data2.append(y2)

        # Clear the previous plot and plot the updated data
        self.ax.clear()
        self.ax.plot(self.timestamps, self.y_data1, marker='o', linestyle='-', label='Sensor 1')
        if y2 is not None:
            self.ax.plot(self.timestamps, self.y_data2, marker='x', linestyle='-', label='Sensor 2')

        # Format the x-axis to show timestamps clearly
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Value')
        self.ax.grid(True)
        self.ax.legend()
        self.figure.autofmt_xdate()  # Rotate the timestamps for better readability
        self.canvas.draw()  # Redraw the canvas
        
class LineGraph_Sensors(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        # Create a figure and axis for the plot
        self.figure, self.ax = plt.subplots(figsize=(5.28, 3), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

        # Initialize data lists for two data sets
        self.timestamps = []  # Data for timestamps
        self.y_data1 = []  # Data for Sensor 1
        self.y_data2 = []  # Data for Sensor 2

        # Set axis labels and grid
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Value')

        # Initialize the plot with empty data
        self.ax.plot([], [], marker='x', linestyle='-', color='orange', label='Sensor 1')
        self.ax.plot([], [], marker='x', linestyle='-', color='blue', label='Sensor 2')

        # Format x-axis
        self.figure.autofmt_xdate()  # Rotate the timestamps for better readability

        # Hide grid, axis labels, and borders initially
        self._hide_axes_details()
        self.canvas.draw()  # Draw the initial empty plot

    def _hide_axes_details(self):
        self.ax.set_xticks([])  # Hide x-axis ticks
        self.ax.set_yticks([])  # Hide y-axis ticks
        self.ax.spines['top'].set_visible(False)  # Hide top border
        self.ax.spines['right'].set_visible(False)  # Hide right border
        self.ax.spines['left'].set_visible(False)  # Hide left border
        self.ax.spines['bottom'].set_visible(False)  # Hide bottom border
        self.ax.set_xlabel('')
        self.ax.set_ylabel('')
        self.ax.grid(False)

    def update_graph2(self, y2):
        # Get the current timestamp
        current_time = datetime.now().strftime('%H:%M:%S')
        
        # Append the current timestamp and data
        self.timestamps.append(current_time)
        self.y_data2.append(y2)

        # Clear the previous plot and plot the updated data for Sensor 2
        self.ax.clear()
        self.ax.plot(self.timestamps, self.y_data2, marker='x', linestyle='-', color='blue', label='Sensor 1')

        # Format x-axis
        self.figure.autofmt_xdate()  # Rotate the timestamps for better readability

        # Hide grid, axis labels, and borders
        self._hide_axes_details()

        # Add legend if there's data
        if self.y_data2:
            self.ax.legend()

        self.canvas.draw()  # Redraw the canvas

    def update_graph3(self, y2):
        # Get the current timestamp
        current_time = datetime.now().strftime('%H:%M:%S')
        
        # Append the current timestamp and data
        self.timestamps.append(current_time)
        self.y_data2.append(y2)

        # Clear the previous plot and plot the updated data for Sensor 1
        self.ax.clear()
        self.ax.plot(self.timestamps, self.y_data2, marker='x', linestyle='-', color='orange', label='Sensor 2')

        # Format x-axis
        self.figure.autofmt_xdate()  # Rotate the timestamps for better readability

        # Hide grid, axis labels, and borders
        self._hide_axes_details()

        # Add legend if there's data
        if self.y_data2:
            self.ax.legend()

        self.canvas.draw()  # Redraw the canvas

class BarGraph(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.figure, self.ax = plt.subplots(figsize=(5, 3.5), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.ax.bar(['Sensor 1', 'Sensor 2'], [0, 0], color=['blue', 'red'])
        self.canvas.draw()

        # Frame for main for the bar
        self.mainbar_frame = tk.Frame(self, bg='white', padx=0, pady=0, relief='groove')
        self.mainbar_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(0, 0))
        
        self.combined_bar_label = tk.Label(self.mainbar_frame, text="0 %", font=('Helvetica', 18, 'bold'), bg='white', fg='blue')
        self.combined_bar_label.pack(side=tk.LEFT, padx=(10, 20),pady=(0, 20))
        
        # Frame for the combined bar
        self.combined_bar_frame = tk.Frame(self.mainbar_frame, bg='white', padx=0, pady=0, borderwidth=2, relief='groove')
        self.combined_bar_frame.pack(side=tk.LEFT, fill=tk.X, pady=(0, 20))

        self.combined_bar = tk.Canvas(self.combined_bar_frame, height=5, bg='white', bd=0, highlightthickness=0)
        self.combined_bar.pack(side=tk.LEFT, fill=tk.X, expand=False, padx=(0, 0))
        self.combined_bar.create_rectangle(0, 0, 0, 20, fill='blue', outline='')

    def update_bar(self, value1, value2):
        self.ax.clear()
        self.ax.bar(['Sensor 1', 'Sensor 2'], [value1, value2], color=['blue', 'orange'])
        self.ax.set_ylim(0, max(value1, value2) + 10)
        self.canvas.draw()

        combined_value = value1 + value2
        combined_percentage = min(combined_value / 2000, 1) * 100  # Calculate the combined percentage

        self.combined_bar.delete("all")
        self.combined_bar.create_rectangle(0, 0, (self.combined_bar.winfo_width() * combined_percentage / 100), 20, fill='blue', outline='')

        self.combined_bar_label.config(text=f"{combined_percentage:.1f} %")  # Update to show percentage       

class CircularProgressBarPage4(tk.Canvas):
    def __init__(self, parent, size=150, thickness=10, max_value=1000, color="DeepSkyBlue4", *args, **kwargs):
        super().__init__(parent, width=size, height=size, bg='white', *args, **kwargs, highlightbackground="white")
        self.size = size
        self.thickness = thickness
        self.max_value = max_value
        self.value = 0
        self.color = 'red'
        self.draw_circle()

    def set_value(self, value):
        self.value = value
        self.draw_circle()

    def draw_circle(self):
        self.delete("all")
        angle = 360 * (self.value / self.max_value)
        extent = angle

        self.create_oval(self.thickness, self.thickness, self.size - self.thickness, self.size - self.thickness,
                         outline="#DDDDDD", width=self.thickness)
        self.create_arc(self.thickness, self.thickness, self.size - self.thickness, self.size - self.thickness,
                        start=90, extent=-extent, style=tk.ARC, outline=self.color, width=self.thickness)

        # Calculate and display the percentage in the middle of the circle
        percentage = (self.value / self.max_value) * 100
        self.create_text(self.size / 2, self.size / 2, text=f"{percentage:.1f}%", fill="black", font=('Arial', int(self.size/10), 'bold'))

class CircularProgressBarTopic2(tk.Canvas):
    def __init__(self, parent, size=150, thickness=10, max_value=100, color="DeepSkyBlue4", *args, **kwargs):
        super().__init__(parent, width=size, height=size, bg='white', *args, **kwargs, highlightbackground="white")
        self.size = size
        self.thickness = thickness
        self.max_value = max_value
        self.value = 0
        self.color = 'orange'
        self.draw_circle()

    def set_value(self, value):
        self.value = value
        self.draw_circle()

    def draw_circle(self):
        self.delete("all")
        angle = 360 * (self.value / self.max_value)
        extent = angle

        # Draw background circle
        self.create_oval(self.thickness, self.thickness, self.size - self.thickness, self.size - self.thickness,
                         outline="#DDDDDD", width=self.thickness)
        # Draw progress arc
        self.create_arc(self.thickness, self.thickness, self.size - self.thickness, self.size - self.thickness,
                        start=90, extent=-extent, style=tk.ARC, outline=self.color, width=self.thickness)

        # Calculate and display the percentage in the middle of the circle
        percentage = (self.value / self.max_value) * 100
        self.create_text(self.size / 2, self.size / 2, text=f"{percentage:.1f}%", fill="black", font=('Arial', int(self.size/10), 'bold'))

class CircularProgressBarUltrasonics1(tk.Canvas):
    def __init__(self, parent, size=150, thickness=10, max_value=100, color="DeepSkyBlue4", *args, **kwargs):
        super().__init__(parent, width=size, height=size, bg='white', *args, **kwargs, highlightbackground="white")
        self.size = size
        self.thickness = thickness
        self.max_value = max_value
        self.value = 0
        self.color = 'blue'
        self.draw_circle()

    def set_value(self, value):
        self.value = value
        self.draw_circle()

    def draw_circle(self):
        self.delete("all")
        angle = 360 * (self.value / self.max_value)
        extent = angle

        # Draw background circle
        self.create_oval(self.thickness, self.thickness, self.size - self.thickness, self.size - self.thickness,
                         outline="#DDDDDD", width=self.thickness)
        # Draw progress arc
        self.create_arc(self.thickness, self.thickness, self.size - self.thickness, self.size - self.thickness,
                        start=90, extent=-extent, style=tk.ARC, outline=self.color, width=self.thickness)

        # Calculate and display the percentage in the middle of the circle
        percentage = (self.value / self.max_value) * 100
        self.create_text(self.size / 2, self.size / 2, text=f"{percentage:.1f}%", fill="black", font=('Arial', int(self.size/10), 'bold'))

class CircularProgressBarUltrasonics2(tk.Canvas):
    def __init__(self, parent, size=150, thickness=10, max_value=100, color="DeepSkyBlue4", *args, **kwargs):
        super().__init__(parent, width=size, height=size, bg='white', *args, **kwargs, highlightbackground="white")
        self.size = size
        self.thickness = thickness
        self.max_value = max_value
        self.value = 0
        self.color = 'orange'
        self.draw_circle()

    def set_value(self, value):
        self.value = value
        self.draw_circle()

    def draw_circle(self):
        self.delete("all")
        angle = 360 * (self.value / self.max_value)
        extent = angle

        # Draw background circle
        self.create_oval(self.thickness, self.thickness, self.size - self.thickness, self.size - self.thickness,
                         outline="#DDDDDD", width=self.thickness)
        # Draw progress arc
        self.create_arc(self.thickness, self.thickness, self.size - self.thickness, self.size - self.thickness,
                        start=90, extent=-extent, style=tk.ARC, outline=self.color, width=self.thickness)

        # Calculate and display the percentage in the middle of the circle
        percentage = (self.value / self.max_value) * 100
        self.create_text(self.size / 2, self.size / 2, text=f"{percentage:.1f}%", fill="black", font=('Arial', int(self.size/10), 'bold'))


class Page4(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        # Configure grid layout
        self.grid_columnconfigure(0, weight=2)  # MainBox3_frame will be wider
        self.grid_columnconfigure(1, weight=1)  # MainBox4_frame will be narrower
        self.grid_columnconfigure(2, weight=1)  # MainBox_frame and MainBox2_frame will have the same width
        self.grid_columnconfigure(3, weight=1)  # Same as above
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.MainBox_frame = tk.Frame(self)
        self.MainBox_frame.grid(row=0, column=0, columnspan=2, padx=(10,0), pady=(10,0), sticky="nsew")

        self.page4_title = tk.Label(self.MainBox_frame, text="Temperature Data", font=('Arial', 14, 'bold'), bg='red', fg='white', padx=10, pady=10)
        self.page4_title.pack(fill=tk.X, padx=10, pady=(10, 0))

        # Frame for current value and change value frames
        self.items_frame = tk.Frame(self.MainBox_frame)
        self.items_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=0)

       # Frame for current value
        self.current_value_frame = tk.Frame(self.items_frame, bg='white', highlightbackground="black", highlightcolor="black", highlightthickness=1)
        self.current_value_frame.pack(pady=(10, 0), fill=tk.BOTH, expand=True)

        # Title for the bar
        self.current_value_titlePage4 = tk.Label(self.current_value_frame, text="Current Value", font=('Helvetica', 12, 'bold'), bg='white', fg='grey')
        self.current_value_titlePage4.pack(side=tk.TOP, anchor='nw', padx=(10, 0), pady=(10, 0))

        # Frame to hold the arrow and the value
        self.value_display_frame = tk.Frame(self.current_value_frame, bg='white')
        self.value_display_frame.pack(pady=10, fill='x', padx=10)

        # Arrow label beside the current value
        self.arrow_labelTopic1 = tk.Label(self.value_display_frame, text="▲", font=('Arial', 25), bg='white', fg='grey')
        self.arrow_labelTopic1.pack(side=tk.LEFT, padx=(10, 5))

        # Frame to hold the value and the unit
        self.value_text_frame = tk.Frame(self.value_display_frame, bg='white')
        self.value_text_frame.pack(side=tk.LEFT)

        # Label to display the current value
        self.value_labelpage4 = tk.Label(self.value_text_frame, text="00", font=('Arial', 50), bg='white', fg='black')
        self.value_labelpage4.pack(side=tk.TOP, padx=(0, 50), pady=(20, 0),anchor='center')

        # Label to display the "Degree" with smaller font size
        self.value_value_unit = tk.Label(self.value_text_frame, text="Degree", font=('Helvetica', 15), bg='white', fg='grey')
        self.value_value_unit.pack(side=tk.TOP,padx=(0, 50), pady=(0, 10))
        
        # Frame for change value
        self.change_value_frame = tk.Frame(self.items_frame, bg='white', highlightbackground="black", highlightcolor="black", highlightthickness=1)
        self.change_value_frame.pack(pady=(10, 10), fill=tk.BOTH, expand=True)

        # Title for the bar
        self.change_value_titlePage4 = tk.Label(self.change_value_frame, text="Change Value", font=('Helvetica', 12, 'bold'), bg='white', fg='grey')
        self.change_value_titlePage4.pack(side=tk.TOP, anchor='nw', padx=(10,0), pady=(10,0))

        # Frame for the label
        self.change_label_frame = tk.Frame(self.change_value_frame, bg='white')
        self.change_label_frame.pack(pady=10, fill='both')

        # Label to display the "0" with larger font size
        self.change_label = tk.Label(self.change_label_frame, text="00", font=('Helvetica', 50), bg='white', fg='black')
        self.change_label.pack(side=tk.TOP,pady=(25,0),padx=(50,50))

        # Label to display the "Degree" with smaller font size
        self.change_value_unit = tk.Label(self.change_label_frame, text="Degree", font=('Helvetica', 15), bg='white', fg='grey')
        self.change_value_unit.pack(side=tk.TOP)

        # Main frame for progress bar, status, and graph
        self.progress_frame = tk.Frame(self.MainBox_frame)
        self.progress_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0,5), pady=5)

        # Sub-frame for circular progress bar and status frame
        self.circular_status_frame = tk.Frame(self.progress_frame)
        self.circular_status_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0,5), pady=5)
        
        # Frame for circular progress bar
        self.circular_progress_frame = tk.Frame(self.circular_status_frame, bg='white', highlightbackground="black", highlightcolor="black", highlightthickness=1)
        self.circular_progress_frame.pack(side=tk.TOP, fill=tk.BOTH)
        
        # Title for the bar
        self.Perenctage_titlePage4 = tk.Label(self.circular_progress_frame, text="Perenctage", font=('Helvetica', 12, 'bold'), bg='white', fg='grey')
        self.Perenctage_titlePage4.pack(side=tk.TOP, anchor='nw', padx=(10,0), pady=(10,0))

        # Create and configure circular progress bar
        self.circular_progress_barTopic1 = CircularProgressBarPage4(self.circular_progress_frame, size=175, thickness=10, max_value=100, color="DeepSkyBlue4")
        self.circular_progress_barTopic1.pack(padx=10, pady=10)

        # Frame for status
        self.status_frame = tk.Frame(self.circular_status_frame, bg='white', highlightbackground="black", highlightcolor="black", highlightthickness=1)
        self.status_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=(10,0))
        
        # Title for the bar
        self.status_titlePage4 = tk.Label(self.status_frame, text="Status", font=('Helvetica', 12, 'bold'), bg='white', fg='grey')
        self.status_titlePage4.pack(side=tk.TOP, anchor='nw', padx=(10,0), pady=(10,0))

        # Label to display status
        self.status_label = tk.Label(self.status_frame, text="Cooling", font=('Arial', 20), bg='white', fg='blue')
        self.status_label.pack(side=tk.LEFT,anchor='center',pady=(0,0),padx=(50,0))

        # Frame for the graph
        self.graph_frame_Topic1 = tk.Frame(self.progress_frame, bg='white', highlightbackground="black", highlightcolor="black", highlightthickness=1)
        self.graph_frame_Topic1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=5, padx=(5, 5))
        
        # Title for the bar
        self.graph_titlePage4 = tk.Label(self.graph_frame_Topic1, text="Temperature Over Time", font=('Helvetica', 12, 'bold'), bg='white', fg='grey')
        self.graph_titlePage4.pack(side=tk.TOP, anchor='nw', padx=(10, 0), pady=(10, 0))
        
        self.timestamps = []
        self.data = []
        self.x_data1 =[]
        self.y_data1 =[]
        self.previous_value = 0  # Initialize previous_value here
        
        self.create_plot1()
        
    def create_plot1(self):
        # Create the Matplotlib figure and embed it in Tkinter
        self.fig1 = Figure(figsize=(7,3), dpi=85)
        self.ax1 = self.fig1.add_subplot(111)
        
        self.ax1.set_xlabel("Time")
        self.ax1.set_ylabel("Temperature")
        self.ax1.grid(True)
        self.line1, = self.ax1.plot([], [], 'r-', marker = 'x', linestyle = '-')
        
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=self.graph_frame_Topic1)
        self.canvas1.draw()
        self.canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        

    
        
        



        # Main container frame
        self.MainBox2_frame = tk.Frame(self)
        self.MainBox2_frame.grid(row=0, column=2, columnspan=2, padx=(0,10), pady=(10,0), sticky="nsew")

        # Title for Page 4
        self.page4_title2 = tk.Label(self.MainBox2_frame, text="humidity", font=('Arial', 14, 'bold'), bg='orange', fg='white', padx=10, pady=10)
        self.page4_title2.pack(fill=tk.X, padx=10, pady=(10, 0))
        
        # Container for items
        self.itemsmain_frame = tk.Frame(self.MainBox2_frame)
        self.itemsmain_frame.pack(fill=tk.BOTH, padx=10, pady=5)

        # Container for items
        self.items2_frame = tk.Frame(self.itemsmain_frame, bg='white', highlightbackground="black", highlightcolor="black", highlightthickness=1)
        self.items2_frame.pack(side=tk.LEFT,fill=tk.BOTH, padx=(0,10), pady=5,expand=True)
        
        # Title for the bar
        self.Humidity_Title_value = tk.Label(self.items2_frame, text="Humidity Data", font=('Helvetica', 12, 'bold'), bg='white', fg='grey')
        self.Humidity_Title_value.pack(side=tk.TOP, anchor='nw', padx=(10,0), pady=(10,0))
        
        # Container for items
        self.items2_frame2 = tk.Frame(self.itemsmain_frame,bg='white', highlightbackground="black", highlightcolor="black", highlightthickness=1)
        self.items2_frame2.pack(side=tk.LEFT,fill=tk.BOTH, padx=(0,0), pady=5,expand=True)
        
        # Title for the bar
        self.Humidity_Title_percentage = tk.Label(self.items2_frame2, text="Percentage", font=('Helvetica', 12, 'bold'), bg='white', fg='grey')
        self.Humidity_Title_percentage.pack(side=tk.TOP, anchor='nw', padx=(10,0), pady=(10,0))
        
        # Frame for current value and arrow
        self.current_value_frame = tk.Frame(self.items2_frame, bg='white')
        self.current_value_frame.pack(side=tk.LEFT, padx=10,expand=True)

        # Frame for circular progress bar
        self.progress_frame = tk.Frame(self.items2_frame2, bg='white')
        self.progress_frame.pack(side=tk.LEFT, padx=10,expand=True)

        # Frame for the graph
        self.graph_frame_Topic2 = tk.Frame(self.MainBox2_frame, bg='white',highlightbackground="black", highlightcolor="black", highlightthickness=1)
        self.graph_frame_Topic2.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0,10))
        
        # Title for the bar
        self.Graphs_Title_value = tk.Label(self.graph_frame_Topic2, text="Humidity Graph Over Time", font=('Helvetica', 12, 'bold'), bg='white', fg='grey')
        self.Graphs_Title_value.pack(side=tk.TOP, anchor='nw', padx=(10,0), pady=(10,0))

        # Arrow Label to show the direction of change
        self.arrow_labelTopic2 = tk.Label(self.current_value_frame, text="▲", font=('Arial', 30, 'bold'), bg='white', fg='grey')
        self.arrow_labelTopic2.pack(side=tk.LEFT)

        # Label to display the current value
        self.value_labelTopic2 = tk.Label(self.current_value_frame, text="0 %", font=('Arial', 30, 'bold'), bg='white', fg='black')
        self.value_labelTopic2.pack(side=tk.LEFT, pady=10)

        # Add the circular progress bar to the progress_frame
        self.circular_progress_bar = CircularProgressBarTopic2(self.progress_frame, size=135, thickness=10, max_value=100, color="DeepSkyBlue4")
        self.circular_progress_bar.pack()
        
        self.timestamps = []
        self.data = []
        self.previous_value = 0  # Initialize previous_value here
        self.last_value = None  # Initialize last_value here
        self.x_data2 = []
        self.y_data2 = []
        
        self.create_plot2()
        
    def create_plot2(self):
        # Create the Matplotlib figure and embed it in Tkinter
        self.fig2 = Figure(figsize=(3, 3), dpi=85)
        self.ax2 = self.fig2.add_subplot(111)
        
        self.ax2.set_xlabel("Time")
        self.ax2.set_ylabel("Value")
        self.ax2.grid(True)
        
        self.line2, = self.ax2.plot([], [], 'r-', marker='x', linestyle='-')
        
        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=self.graph_frame_Topic2)
        self.canvas2.draw()
        self.canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.MainBox3_frame = tk.Frame(self)
        self.MainBox3_frame.grid(row=1, column=0, columnspan=3, padx=(10,0), pady=(0,10), sticky="nsew")

        self.page4_title3 = tk.Label(self.MainBox3_frame, text="Ultrasonic Data", font=('Arial', 14, 'bold'), bg='lightblue4', fg='white', padx=10, pady=10)
        self.page4_title3.pack(fill=tk.X, padx=10, pady=(10, 0))

        # Container for items
        self.items3main_frame = tk.Frame(self.MainBox3_frame)
        self.items3main_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(10,5), pady=5)

        self.items3_frame1 = tk.Frame(self.items3main_frame, bg='white', highlightbackground="black", highlightcolor="black", highlightthickness=1)
        self.items3_frame1.pack(fill=tk.BOTH, expand=True, padx=0, pady=5)
        
        # Title for the bar
        self.FrameTitle_value = tk.Label(self.items3_frame1, text="Distance Data 1", font=('Helvetica', 12, 'bold'), bg='white', fg='grey')
        self.FrameTitle_value.pack(side=tk.TOP, anchor='nw', padx=(10,0), pady=(10,0))

        self.items3_frame2 = tk.Frame(self.items3main_frame, bg='white', highlightbackground="black", highlightcolor="black", highlightthickness=1)
        self.items3_frame2.pack(fill=tk.BOTH, expand=True, padx=0, pady=5)
        
        # Title for the bar
        self.FrameTitle2_value = tk.Label(self.items3_frame2, text="Distance Data 2", font=('Helvetica', 12, 'bold'), bg='white', fg='grey')
        self.FrameTitle2_value.pack(side=tk.TOP, anchor='nw', padx=(10,0), pady=(10,0))
        
        self.radar_chart_frame = tk.Frame(self.MainBox3_frame,highlightbackground="black", highlightcolor="black", highlightthickness=1,bg = 'white')
        self.radar_chart_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5,5), pady=10)
        
        # Title for the bar
        self.Radar_Title_value = tk.Label(self.radar_chart_frame, text="Radar Chart On Density", font=('Helvetica', 12, 'bold'), bg='white', fg='grey')
        self.Radar_Title_value.pack(side=tk.TOP, anchor='nw', padx=(10,0), pady=(10,0))

        self.graph_frame_Topic3 = tk.Frame(self.MainBox3_frame, highlightbackground="black", highlightcolor="black", highlightthickness=1, bg='white')
        self.graph_frame_Topic3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5,10), pady=10)
        
        # Title for the bar
        self.DistanceGraph_Title_value = tk.Label(self.graph_frame_Topic3, text="Distance Graph Over Time", font=('Helvetica', 12, 'bold'), bg='white', fg='grey')
        self.DistanceGraph_Title_value.pack(side=tk.TOP, anchor='nw', padx=(10,0), pady=(10,0))

        # Add labels and circular progress bars to show current values and arrows
        self.arrow_label1 = tk.Label(self.items3_frame1, text="▲", font=('Arial', 20, 'bold'), bg='white', fg='grey')
        self.arrow_label1.pack(side=tk.LEFT, padx=(20,0), pady=10)
        self.value_label1 = tk.Label(self.items3_frame1, text="0.0 cm", font=('Arial', 20, 'bold'), bg='white', fg='black')
        self.value_label1.pack(side=tk.LEFT, padx=(0,10), pady=10)
        self.circular_progress1 = CircularProgressBarUltrasonics1(self.items3_frame1, size=135, thickness=10, max_value=250)
        self.circular_progress1.pack(side=tk.RIGHT, padx=10, pady=10)
        
        self.arrow_label2 = tk.Label(self.items3_frame2, text="▲", font=('Arial', 20, 'bold'), bg='white', fg='grey')
        self.arrow_label2.pack(side=tk.LEFT, padx=(20,0), pady=10)
        self.value_label2 = tk.Label(self.items3_frame2, text="0.0 cm", font=('Arial', 20, 'bold'), bg='white', fg='black')
        self.value_label2.pack(side=tk.LEFT, padx=(0,10), pady=10)
        self.circular_progress2 = CircularProgressBarUltrasonics2(self.items3_frame2, size=135, thickness=10, max_value=250)
        self.circular_progress2.pack(side=tk.RIGHT, padx=10, pady=10)

        # Initialize previous values and x-axis counter
        self.prev_value1 = 0
        self.prev_value2 = 0
        self.x_data_third = []
        self.y_data1_third = []
        self.y_data2_third = []

        # Create the plot for line graph
        self.figure = Figure(figsize=(5, 1), dpi=85)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Value')
        self.line1, = self.ax.plot(self.x_data_third, self.y_data1_third, label='Sensor 1')
        self.line2, = self.ax.plot(self.x_data_third, self.y_data2_third, label='Sensor 2')
        self.ax.legend()

        # Embed the line graph in Tkinter
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.graph_frame_Topic3)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Create the Radar chart
        self.radar_figure = Figure(figsize=(3.9, 3.9), dpi=90)
        self.radar_ax = self.radar_figure.add_subplot(111, polar=True)
        self.radar_ax.set_ylim(0, 250)  # Adjust based on your data

        # Embed the Radar chart in Tkinter
        self.radar_canvas = FigureCanvasTkAgg(self.radar_figure, master=self.radar_chart_frame)
        self.radar_canvas.draw()
        self.radar_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        
        
        
        
        
        # Create the main frame Part 4
        self.MainBox4_frame = tk.Frame(self)
        self.MainBox4_frame.grid(row=1, column=3, padx=(0,10), pady=(0,10), sticky="nsew")

        # Title for the page
        self.page4_title4 = tk.Label(self.MainBox4_frame, text="Weight Data", font=('Arial', 14, 'bold'), bg='green', fg='white', padx=10, pady=10)
        self.page4_title4.pack(fill=tk.X, padx=10, pady=(10, 5))  # Reduced bottom padding

        # Frame for average value
        self.items4_frame = tk.Frame(self.MainBox4_frame, bg='white', highlightbackground="black", highlightcolor="black", highlightthickness=1)
        self.items4_frame.pack(fill=tk.X, padx=10, pady=5)

        # Title for average value
        self.average_frame_title = tk.Label(self.items4_frame, text="Average Value", font=('Helvetica', 12, 'bold'), bg='white', fg='Grey')
        self.average_frame_title.pack(side=tk.TOP, anchor='w', padx=15, pady=(15, 2))
        
        # Frame for value and arrow
        self.TotalText_Frame = tk.Frame(self.items4_frame, bg='white')
        self.TotalText_Frame.pack(side=tk.TOP,padx=10, pady=(30, 2), fill=tk.X, anchor='center')  # Reduced vertical padding

        # Frame for value and arrow
        self.value_arrow_frame = tk.Frame(self.TotalText_Frame, bg='white')
        self.value_arrow_frame.pack(side=tk.TOP,padx=10, pady=(5, 2))  # Reduced vertical padding

        # Label for arrow
        self.arrow_label = tk.Label(self.value_arrow_frame, text="▲", font=('Arial', 28), bg='white', fg='grey')
        self.arrow_label.pack(side=tk.LEFT, padx=(0, 0),anchor='center')

        # Label for displaying value
        self.value_label = tk.Label(self.value_arrow_frame, text="0 Kg", font=('Arial', 28), bg='white', fg='grey')
        self.value_label.pack(side=tk.LEFT, padx=(5, 0))

        # Frame for displaying values and change indicator
        self.values_frame = tk.Frame(self.MainBox4_frame, bg='white',highlightbackground="black", highlightcolor="black", highlightthickness=1)
        self.values_frame.pack(fill=tk.X, padx=10, pady=(5, 5))  # Reduced bottom padding

        # Configure grid columns for equal separation
        self.values_frame.grid_columnconfigure(0, weight=1)
        self.values_frame.grid_columnconfigure(1, weight=1)
        self.values_frame.grid_columnconfigure(2, weight=1)

        # Value labels and descriptions in one frame using grid
        self.Change_value_label = tk.Label(self.values_frame, text="0 Kg", font=('Arial', 15), bg='white', fg='grey')
        self.Change_value_label.grid(row=0, column=0, padx=10, pady=(5, 2), sticky="ew")  # Reduced bottom padding

        self.percentage_change_label = tk.Label(self.values_frame, text="0 %", font=('Arial', 15), bg='white', fg='grey')
        self.percentage_change_label.grid(row=0, column=1, padx=10, pady=(5, 2), sticky="ew")  # Reduced bottom padding

        self.change_indicator_label = tk.Label(self.values_frame, text="No Change", font=('Arial', 15), bg='white', fg='grey')
        self.change_indicator_label.grid(row=0, column=2, padx=10, pady=(5, 2), sticky="ew")  # Reduced bottom padding

        self.current_value_desc_label = tk.Label(self.values_frame, text="Value Change", font=('Arial', 10), bg='white', fg='Blue')
        self.current_value_desc_label.grid(row=1, column=0, padx=10, pady=(0, 5), sticky="ew")  # Reduced bottom padding

        self.percentage_change_desc_label = tk.Label(self.values_frame, text="Percentage Change", font=('Arial', 10), bg='white', fg='orange')
        self.percentage_change_desc_label.grid(row=1, column=1, padx=10, pady=(0, 5), sticky="ew")  # Reduced bottom padding

        self.change_indicator_desc_label = tk.Label(self.values_frame, text="Change Indicator", font=('Arial', 10), bg='white', fg='red')
        self.change_indicator_desc_label.grid(row=1, column=2, padx=10, pady=(0, 5), sticky="ew")  # Reduced bottom padding

        self.create_plot4()

        # Initialize lists to store data
        self.x_data4 = []
        self.y_data4 = []
        self.last_value4 = None

    def create_plot4(self):
        # Create a Matplotlib figure and axis
        self.fig4 = Figure(figsize=(2.5, 1.5), dpi=100)
        self.ax4 = self.fig4.add_subplot(111)

        # Initial plot (empty data)
        self.line4, = self.ax4.plot([], [], 'r-', marker='x', linestyle='-')  # Line with markers

        # Hide the axes
        self.ax4.spines['top'].set_color('none')
        self.ax4.spines['bottom'].set_color('none')
        self.ax4.spines['left'].set_color('none')
        self.ax4.spines['right'].set_color('none')
        self.ax4.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)

        # Embed the figure in the Tkinter frame
        self.canvas4 = FigureCanvasTkAgg(self.fig4, master=self.items4_frame)
        self.canvas4.draw()
        self.canvas4.get_tk_widget().pack(fill=tk.X, pady=(5, 5))  # Adjusted padding
        
    def update_progress4(self, value):
        current_time = time.time()
        self.x_data4.append(current_time)
        self.y_data4.append(value)

        self.line4.set_data(self.x_data4, self.y_data4)

        # Clear previous annotations
        self.ax4.clear()

        # Plot the line and markers
        self.ax4.plot(self.x_data4, self.y_data4, 'r-', marker='x') 

        # Hide the axes again
        self.ax4.spines['top'].set_color('none')
        self.ax4.spines['bottom'].set_color('none')
        self.ax4.spines['left'].set_color('none')
        self.ax4.spines['right'].set_color('none')
        self.ax4.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)

        # Rescale the plot to fit the data
        self.ax4.relim()
        self.ax4.autoscale_view()
        self.canvas4.draw()

        # Update value and arrow
        if self.last_value4 is not None:
            change = value - self.last_value4
            percentage_change = (change / self.last_value4) * 100 if self.last_value4 != 0 else 0

            if value > self.last_value4:
                arrow_text = "▲"
                arrow_color = "green"
                change_text = f"Increase"
            elif value < self.last_value4:
                arrow_text = "▼"
                arrow_color = "red"
                change_text = f"Decrease"
            else:
                arrow_text = self.arrow_label.cget("text")
                arrow_color = self.arrow_label.cget("fg")
                change_text = "No Change"

            self.value_label.config(text=f"{value:.0f} Kg")
            self.arrow_label.config(text=arrow_text, fg=arrow_color)
            self.Change_value_label.config(text=f"{change:.0f} Kg")
            self.percentage_change_label.config(text=f"{percentage_change:.0f} %")
            self.change_indicator_label.config(text=change_text, fg=arrow_color)

        self.last_value4 = value



    def update_progress1(self, value):
        # Get the current time as a formatted string
        current_time1 = time.strftime('%H:%M:%S')

        # Append the formatted time and the value
        self.x_data1.append(current_time1)
        self.y_data1.append(value)
        
        # Ensure the value is within the range of 0 to 100
        value = max(0, min(100, value))

        # Print the value to debug
        print(f"Updating value to: {value}")

        # Update the circular progress bar and value label
        self.circular_progress_barTopic1.set_value(value)  # Update circular progress bar value
        self.value_labelpage4.config(text=f"{value:.0f}")

        # Calculate the value change
        value_change = value - self.previous_value
        self.change_label.config(text=f"{value_change:.0f}")

        # Debug prints for arrow update logic
        print(f"Previous Value: {self.previous_value}")
        print(f"Value Change: {value_change}")

        # Update the arrow direction and color based on the value change
        if value_change > 0:
            arrow_text_T1 = "▲"
            arrow_color_T1 = "green"
        elif value_change < 0:
            arrow_text_T1 = "▼"
            arrow_color_T1 = "red"
        else:
            arrow_text_T1 = "▲"
            arrow_color_T1 = "grey"
            
        self.arrow_labelTopic1.config(text= arrow_text_T1, fg= arrow_color_T1)
        # Update previous value
        self.previous_value = value

        # Update cooling status based on value
        if value <= 25:
            status_text = "Cooling"
            status_color = 'blue'
        elif 26 <= value <= 36:
            status_text = "Normal"
            status_color = 'green'
        else:
            status_text = "Too Hot"
            status_color = 'red'

        self.status_label.config(text=status_text, fg=status_color)

        # Limit the number of data points to 10
        max_points = 7
        if len(self.x_data1) > max_points:
            self.x_data1 = self.x_data1[-max_points:]
            self.y_data1 = self.y_data1[-max_points:]

        # Update the plot
        self.ax1.clear()  # Clear the previous plot
        self.ax1.set_xlabel("Time")
        self.ax1.set_ylabel("Temperature")
        self.ax1.grid(True)

        # Update the plot with new data
        self.ax1.plot(self.x_data1, self.y_data1, 'r-', marker='x', linestyle='-')

        # Redraw the canvas with updated plot
        self.canvas1.draw()
            
    def update_time_Topic1(self):
        from time import strftime
        time_string = strftime('%H:%M:%S')
        self.time_label.config(text=time_string)
        self.after(1000, self.update_time_Topic1)  # Update the time every second
        
    def update_progress2(self, value):
        # Get the current time as a formatted string
        current_time2 = time.strftime('%H:%M:%S')
        self.x_data2.append(current_time2)
        self.y_data2.append(value)
        
        # Keep the last 20 data points for better visualization
        if len(self.x_data2) > 20:
            self.x_data2 = self.x_data2[-20:]
            self.y_data2 = self.y_data2[-20:]
        
        # Update the line plot data
        self.line2.set_data(self.x_data2, self.y_data2)
        
        # Adjust the plot limits to include new data
        self.ax2.relim()
        self.ax2.autoscale_view()
        
        # Redraw the canvas with updated data
        self.canvas2.draw()

        # Update the arrow label based on value change
        if self.last_value is not None:
            if value > self.last_value:
                self.arrow_labelTopic2.config(text="▲", fg="green")
            elif value < self.last_value:
                self.arrow_labelTopic2.config(text="▼", fg="red")
            else:
                self.arrow_labelTopic2.config(text="▲", fg="grey")  # No arrow if unchanged
        else:
            self.arrow_labelTopic2.config(text="▲", fg="green")  # No arrow if first update

        # Update the value label with the new value
        self.value_labelTopic2.config(text=f"{value} %")  

        # Update the circular progress bar value
        self.circular_progress_bar.set_value(value)

        # Update last_value for the next comparison
        self.last_value = value

        # Clear the previous plot and update it with new data
        self.ax2.clear()
        self.ax2.set_xlabel("Time")
        self.ax2.set_ylabel("Value")
        self.ax2.grid(True)

        # Plot the updated data
        self.ax2.plot(self.x_data2, self.y_data2, 'r-', marker='x', linestyle='-')

        # Redraw the canvas with updated plot
        self.canvas2.draw()
    
    def update_time_Topic2(self):
        from time import strftime
        time_string = strftime('%H:%M:%S')
        self.time_label.config(text=time_string)
        self.after(1000, self.update_time_Topic2)  # Update the time every second
    #   self.after(1000, self.update_time_Topic2)  # Update the time every second

    def update_progress3(self, value):
        # Update the frame and value label with the received data
        self.items3_frame1.configure(bg='white')
        self.value_label1.config(text=f"{value} cm")

        # Update the circular progress bar value
        self.circular_progress1.set_value(value)

        # Update the arrow based on the value change
        if value > self.prev_value1:
            Arrow_Shape1 = "▲"
            Arrow_color1 = 'green'
        elif value < self.prev_value1:
            Arrow_Shape1 = "▼"
            Arrow_color1 = 'red'
        else:
            Arrow_Shape1 = self.arrow_label1.cget('text')
            Arrow_color1 = self.arrow_label1.cget('fg')

        self.arrow_label1.config(text=Arrow_Shape1, fg=Arrow_color1)
        # Update the previous value
        self.prev_value1 = value

        # Update the plot data
        if len(self.x_data_third) == 0 or len(self.x_data_third) == len(self.y_data1_third):
            self.x_data_third.append(len(self.x_data_third))
            self.y_data1_third.append(value)
            self.y_data2_third.append(self.y_data2_third[-1] if self.y_data2_third else 0)
        else:
            self.y_data1_third[-1] = value

        self.line1.set_data(self.x_data_third, self.y_data1_third)
        self.line2.set_data(self.x_data_third, self.y_data2_third)
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw()

        # Update Radar chart
        self.update_radar_chart([self.y_data1_third[-1], self.y_data2_third[-1], self.y_data1_third[-1], self.y_data2_third[-1]])

    def update_progress5(self, value):
        # Update the frame and value label with the received data
        self.items3_frame2.configure(bg='white')
        self.value_label2.config(text=f"{value} cm")

        # Update the circular progress bar value
        self.circular_progress2.set_value(value)

        # Update the arrow based on the value change
        if value > self.prev_value2:
            Arrow_Shape2 = "▲"
            Arrow_color2 = 'green'
        elif value < self.prev_value2:
            Arrow_Shape2 = "▼"
            Arrow_color2 = 'red'
        else:
            Arrow_Shape2 = self.arrow_label2.cget('text')
            Arrow_color2 = self.arrow_label2.cget('fg')

        self.arrow_label2.config(text=Arrow_Shape2, fg=Arrow_color2)
        # Update the previous value
        self.prev_value2 = value

        # Update the plot data
        if len(self.x_data_third) == 0 or len(self.x_data_third) == len(self.y_data2_third):
            self.x_data_third.append(len(self.x_data_third))
            self.y_data2_third.append(value)
            self.y_data1_third.append(self.y_data1_third[-1] if self.y_data1_third else 0)
        else:
            self.y_data2_third[-1] = value

        self.line1.set_data(self.x_data_third, self.y_data1_third)
        self.line2.set_data(self.x_data_third, self.y_data2_third)
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw()

        # Update Radar chart
        self.update_radar_chart([self.y_data1_third[-1], self.y_data2_third[-1], self.y_data1_third[-1], self.y_data2_third[-1]])

    def update_radar_chart(self, data):
        # Radar chart configuration
        categories = ['Sensor 1', 'Sensor 2', 'Sensor 1', 'Sensor 2']
        num_vars = len(categories)
        
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        angles += angles[:1]
        data += data[:1]
        
        self.radar_ax.clear()
        self.radar_ax.set_ylim(0, 250)  # Adjust based on your data
        
        self.radar_ax.plot(angles, data, color='b', linewidth=2, linestyle='solid')
        self.radar_ax.fill(angles, data, color='b', alpha=0.25)
        self.radar_ax.set_yticklabels([])
        self.radar_ax.set_xticks(angles[:-1])
        self.radar_ax.set_xticklabels(categories)
        
        self.radar_canvas.draw()
    



class Main(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('MQTT and Plotting in Tkinter')
        self.geometry("1200x1000")

        self.sidebar_frame = tk.Frame(self, width=200, bg='brown')
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        dashboard_label = tk.Label(self.sidebar_frame, text="Dashboard", font=('Arial', 14, 'bold'), bg='brown', padx=10, pady=10)
        dashboard_label.pack(fill=tk.X)

        separator = ttk.Separator(self.sidebar_frame, orient=tk.HORIZONTAL)
        separator.pack(fill=tk.X, padx=5, pady=5)

        self.page1 = Page1(self)
        self.page2 = Page2(self)
        self.page3 = Page3(self)
        self.page4 = Page4(self)

        page1_button = tk.Button(self.sidebar_frame, text="Page 1", font=('Arial', 12), command=self.show_page1)
        page1_button.pack(fill=tk.X, padx=10, pady=10)

        page2_button = tk.Button(self.sidebar_frame, text="Page 2", font=('Arial', 12), command=self.show_page2)
        page2_button.pack(fill=tk.X, padx=10, pady=10)

        page3_button = tk.Button(self.sidebar_frame, text="Page 3", font=('Arial', 12), command=self.show_page3)
        page3_button.pack(fill=tk.X, padx=10, pady=10)

        page4_button = tk.Button(self.sidebar_frame, text="Page 4", font=('Arial', 12), command=self.show_page4)
        page4_button.pack(fill=tk.X, padx=10, pady=10)

        self.show_page1()

    def show_page1(self):
        self.page2.pack_forget()
        self.page3.pack_forget()
        self.page4.pack_forget()
        self.page1.pack(fill=tk.BOTH, expand=True)

    def show_page2(self):
        self.page1.pack_forget()
        self.page3.pack_forget()
        self.page4.pack_forget()
        self.page2.pack(fill=tk.BOTH, expand=True)

    def show_page3(self):
        self.page1.pack_forget()
        self.page2.pack_forget()
        self.page4.pack_forget()
        self.page3.pack(fill=tk.BOTH, expand=True)

    def show_page4(self):
        self.page1.pack_forget()
        self.page2.pack_forget()
        self.page3.pack_forget()
        self.page4.pack(fill=tk.BOTH, expand=True)

def on_message_page1(client, userdata, message):
    try:
        payload = message.payload.decode('utf-8')
        data = float(payload)
        app.page1.update_plot(data)
    except Exception as e:
        print("Error in on_message_page1:", e)

def on_message_page2(client, userdata, message):
    try:
        payload = message.payload.decode('utf-8')
        data = float(payload)
        print(f"Received data: {data}")  # Debug print
        app.page2.update_light_sensor_value(data)
    except Exception as e:
        print("Error in on_message_page2:", e)

def on_message_page3(client, userdata, message):
    try:
        payload = message.payload.decode('utf-8')
        data = float(payload)
        print(f"Received data for Page 3: {data}")  # Debug print
        app.page3.update_progress1(data)
    except Exception as e:
        print("Error in on_message_page3:", e)

def on_message_page3_new(client, userdata, message):
    try:
        payload = message.payload.decode('utf-8')
        data = float(payload)
        print(f"Received new data for Page 3: {data}")  # Debug print
        app.page3.update_progress2(data)
    except Exception as e:
        print("Error in on_message_page3_new:", e)

def on_message_page4_topic1(client, userdata, message):
    try:
        payload = message.payload.decode('utf-8')
        data = float(payload)
        print(f"Received data for Page 4 Topic 1: {data}")  # Debug print
        app.page4.update_progress1(data)
    except Exception as e:
        print("Error in on_message_page4_topic1:", e)

def on_message_page4_topic2(client, userdata, message):
    try:
        payload = message.payload.decode('utf-8')
        data = float(payload)
        print(f"Received data for Page 4 Topic 2: {data}")  # Debug print
        app.page4.update_progress2(data)
    except Exception as e:
        print("Error in on_message_page4_topic2:", e)

def on_message_page4_topic3(client, userdata, message):
    try:
        payload = message.payload.decode('utf-8')
        data = float(payload)
        print(f"Received data for Page 4 Topic 3: {data}")  # Debug print
        app.page4.update_progress3(data)
    except Exception as e:
        print("Error in on_message_page4_topic3:", e)

def on_message_page4_topic4(client, userdata, message):
    try:
        payload = message.payload.decode('utf-8')
        data = float(payload)
        print(f"Received data for Page 4 Topic 4: {data}")  # Debug print
        app.page4.update_progress4(data)
    except Exception as e:
        print("Error in on_message_page4_topic4:", e)

def on_message_page4_topic5(client, userdata, message):
    try:
        payload = message.payload.decode('utf-8')
        data = float(payload)
        print(f"Received data for Page 4 Topic 5: {data}")  # Debug print
        app.page4.update_progress5(data)
    except Exception as e:
        print("Error in on_message_page4_topic5:", e)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe("topic/test")
        client.subscribe("topic/lightsensor")
        client.subscribe("topic/waterlevel1")
        client.subscribe("topic/waterlevel2")  # New topic for the second circular progress bar
        client.subscribe("topic/temperature")
        client.subscribe("topic/humidity")
        client.subscribe("topic/ultrasonic1")
        client.subscribe("topic/weight")
        client.subscribe("topic/ultrasonic2")  # New topic for Page 4
    else:
        print("Failed to connect, return code %d\n", rc)

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed to topic!")

client = mqtt.Client()
client.on_connect = on_connect
client.on_subscribe = on_subscribe
client.message_callback_add("topic/test", on_message_page1)
client.message_callback_add("topic/lightsensor", on_message_page2)
client.message_callback_add("topic/waterlevel1", on_message_page3)
client.message_callback_add("topic/waterlevel2", on_message_page3_new)  # New callback for the second circular progress bar
client.message_callback_add("topic/temperature", on_message_page4_topic1)
client.message_callback_add("topic/humidity", on_message_page4_topic2)
client.message_callback_add("topic/ultrasonic1", on_message_page4_topic3)
client.message_callback_add("topic/weight", on_message_page4_topic4)
client.message_callback_add("topic/ultrasonic2", on_message_page4_topic5)  # New callback for the fifth topic


# client.connect("broker.emqx.io", 1883, 60)  # Replace with your actual broker address
client.connect("broker.hivemq.com", 1883, 60)  # Replace with your actual broker address
client.loop_start()

app = Main()
app.mainloop()