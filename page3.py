#file  -- page3.py --
import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Style
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from datetime import datetime
#import paho.mqtt.client as mqtt
from datetime import time
import time
#import numpy as np
from time import strftime


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

class CircularProgressBar(tk.Canvas): #3
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

class StatusIndicator(tk.Canvas): #3
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

class LineGraph(tk.Frame): #3
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
        
class LineGraph_Sensors(tk.Frame): #3
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

class BarGraph(tk.Frame): #3
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
