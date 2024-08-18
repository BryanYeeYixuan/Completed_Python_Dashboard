#file  -- page1.py --
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
