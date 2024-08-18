#file  -- page4.py --
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
import numpy as np
from time import strftime

class CircularProgressBarPage4(tk.Canvas): #4
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

class CircularProgressBarTopic2(tk.Canvas): #4
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

class CircularProgressBarUltrasonics1(tk.Canvas): #4
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

class CircularProgressBarUltrasonics2(tk.Canvas): #4
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

class Page4(tk.Frame): #4
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
