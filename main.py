#file  -- common.py --
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
import sub_main

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

app = sub_main.Main()
app.mainloop()