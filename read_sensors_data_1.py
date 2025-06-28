import serial
import csv
import time
from datetime import datetime
import re
import os

class SerialNumber:

    @classmethod
    def get_serial_port(cls):

        try:
            return serial.Serial('COM3', 9600, timeout=1)
        except Exception as e:
            return e

class PortVariables:

    @classmethod
    def get_port_variables(cls,serial_port):

        try:
            return re.search(r'Distance:\s*([\d.]+)\s*cm,\s*IR:\s*(.*),\s*Temp:\s*([\d.]+)\s*C', serial_port)
        except Exception as e:
            return e

class CSVWriter:

    def __init__(self):
        self.ser = SerialNumber.get_serial_port()
        if self.ser:
            time.sleep(2)  # Give Arduino time to reset

    def write_to_csv(self, filename: str):

        if not self.ser:
            print("Serial port not available.")
            return

        file_exists = os.path.exists(filename)

        print("Logging started... Press Ctrl+C to stop.")
        
        try:
            with open(filename, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)

                # Write header only if file does not exist
                if not file_exists:
                    writer.writerow(['Timestamp', 'Distance (cm)', 'IR Status', 'Temperature'])

                while True:
                    line = self.ser.readline().decode('utf-8').strip()
                    match = PortVariables.get_port_variables(serial_port=line)
                    if match:
                        distance = float(match.group(1))
                        ir_status = match.group(2).strip()
                        temperature = float(match.group(3))
                        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        writer.writerow([timestamp, distance, ir_status, temperature])
                        print(f"{timestamp} | Distance: {distance} cm | IR: {ir_status} | Temperature: {temperature}")
                    else:
                        print(f"Ignored line: {line}")  # Optional: for debugging

        except KeyboardInterrupt:
            print("Logging stopped.")
        except Exception as e:
            print(f"Error during logging: {e}")

if __name__ == "__main__":
    writer = CSVWriter()
    writer.write_to_csv(filename='sensors_data.csv')