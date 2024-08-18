#file  -- main.py --
import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Style
#from matplotlib import pyplot as plt
#from matplotlib.figure import Figure
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from datetime import datetime
import paho.mqtt.client as mqtt
from datetime import time
import time
#import numpy as np
from time import strftime
import page1, page2, page3, page4


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

        self.page1 = page1.Page1(self)
        self.page2 = page2.Page2(self)
        self.page3 = page3.Page3(self)
        self.page4 = page4.Page4(self)

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