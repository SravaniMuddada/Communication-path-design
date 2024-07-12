import socket
import RPi.GPIO as GPIO
import time

TRIG = 12
ECHO = 33

def get_distance():
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.output(TRIG, False)
    time.sleep(0.2)
    GPIO.output(TRIG, True)
    time.sleep(0.0001)
    GPIO.output(TRIG, False)
    
    pulse_start = time.time()
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
        
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
        
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # Speed of sound in cm/s
    return distance

def send_sensor_data(client_socket,duration):
    try:
        start_time = time.time()
        while True:
            current_time = time.time()
            elapsed_time = current_time - start_time

            if elapsed_time >= duration:
                print("sensor data reading completed.")
                break
            distance = get_distance()
            data = f"Distance: {distance:.2f} cm"
            print(data)
            client_socket.send(data.encode())
            time.sleep(2)  # Adjust the interval as needed

    except Exception as e:
        print(f"Error sending sensor data: {e}")

def main():
    server_ip = '192.168.137.111'  # Replace with the server's IP
    server_port = 5001

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    duration = 300

    while True:
        message = input("Enter 'send' to send sensor data or 'exit' to quit: ")
        if message.lower() == "send":
            send_sensor_data(client_socket,duration)
            client_socket.close()
        elif message.lower() == "exit":
            break

    client_socket.close()

if __name__ == "__main__":
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    
    try:
        main()
    finally:
        GPIO.cleanup()
