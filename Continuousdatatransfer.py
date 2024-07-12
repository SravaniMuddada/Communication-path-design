import serial
import socket
import threading
import time
import psutil
cpu_utilization_list = []

# Function for serial communication with Arduino
def arduino_serial_communication():
    ser = serial.Serial('/dev/ttyACM0', 9600)  # Replace with the actual serial port
    time.sleep(1)  # Allow time for Arduino to initialize

    while True:
        data = ser.readline().decode('utf-8').strip()
        print(f"Received from Arduino: {data}")

        # Send the received data to another computer over network
        send_data_over_network(data)

# Function for network communication with another computer
def send_data_over_network(data):
    host = '192.168.137.72'  # Replace with the IP address of the other computer
    port = 5000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        data_bytes = data.encode('utf-8')
        s.send(data_bytes)
def measure_cpu_utilization():
    start_time =time.time()
    while time.time() - start_time <60:
        cpu_percent = psutil.cpu_percent(interval=1)  # Measure CPU utilization every 1 second
        cpu_utilization_list.append(cpu_percent)
        #print(f"CPU Utilization: {cpu_percent}%")
        time.sleep(1)
    average_cpu = sum(cpu_utilization_list)/ len(cpu_utilization_list)
    print(f"Average CPU Utilization: {average_cpu}%")
    
# Create a thread for serial communication with Arduino
serial_thread = threading.Thread(target=arduino_serial_communication)
cpu_thread = threading.Thread(target=measure_cpu_utilization)

# Start the serial thread
serial_thread.start()
cpu_thread.start()

# Wait for the serial thread to finish (you can also set up event handling for graceful termination)
serial_thread.join()
