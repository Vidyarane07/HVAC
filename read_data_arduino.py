import serial
import csv
import time
from datetime import datetime
import re


ser = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)  # Allow Arduino to reset

with open('sensor_log.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Timestamp', 'Distance (cm)', 'IR Status', 'Temperature'])  # Header

    print("Logging started... Press Ctrl+C to stop.")

    try:
        while True:
            line = ser.readline().decode('utf-8').strip()
            
            # Expected format: "Distance: 122.45 cm, IR: Object Detected"
            match = re.search(r'Distance:\s*([\d.]+)\s*cm,\s*IR:\s*(.*),\s*Temp:\s*([\d.]+)\s*C', line)
            if match:
                distance = float(match.group(1))
                ir_status = match.group(2).strip()
                temperature = float(match.group(3))
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                writer.writerow([timestamp, distance, ir_status, temperature])
                print(f"{timestamp} | Distance: {distance} cm | IR: {ir_status} | Temperature: {temperature}")
    except KeyboardInterrupt:
        print("Logging stopped.")
