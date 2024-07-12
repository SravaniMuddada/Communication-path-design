import socket
import os
import time
import psutil

def get_cpu_utilization():
    # Get overall CPU utilization percentage
    return psutil.cpu_percent(percpu=False)

def send_file(client_socket, filename):
    try:
        filesize = os.path.getsize(filename)
        client_socket.send(f"send,{filename},{filesize}".encode())
        time.sleep(2)

        print(f"Sending file {filename}...")
        start_time = time.time()
        with open(filename, "rb") as file:
            while True:
                chunk = file.read(4096)
                if not chunk:
                    break
                client_socket.send(chunk)
        end_time = time.time()
        transmission_time = end_time-start_time
        print(f"File {filename} sent in {transmission_time:.2f} seconds")

    except Exception as e:
        print(f"Error sending file {filename}: {e}")

def receive_file(client_socket, output_filename):
    try:
        file_info = client_socket.recv(1024).decode()
        if not file_info:
            print(f"Server disconnected while receiving {filename}")
            return

        while file_info:
            filename, filesize = file_info.split(",")[1:]
            print(f"{filesize} bytes")
            filename = os.path.basename(filename)
            filesize = int(filesize)
            print(filename)

            print(f"Receiving file {filename}...")
            start_time = time.time()
            with open(output_filename, "ab") as file:
                remaining_bytes = filesize
                while remaining_bytes > 0:
                    chunk = client_socket.recv(min(4096, remaining_bytes))
                    if not chunk:
                        break
                    file.write(chunk)
                    remaining_bytes -= len(chunk)
            end_time = time.time()
            print(f"time at reached all data to server {end_time} seconds")
            
            receive_time = end_time-start_time
            print(f"File {filename} received in {receive_time:.2f} seconds")

            message = input("Enter 'C' to continue receiving, 'exit' to quit: ")
            if message.lower() != "c":
                break
            file_info = client_socket.recv(1024).decode()

    except Exception as e:
        print(f"Error receiving file {filename}: {e}")

def main():
    server_ip = '192.168.137.68'  # Replace with the server's IP
    server_port = 5001
    output_filename = "received_file.csv"

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    while True:
        cpu_utilization = get_cpu_utilization()
        print(f"Overall CPU Utilization: {cpu_utilization}%")
        message = input("Enter 'send' or 'receive': ")
        if message.lower() == "send":
            filename = input("Enter the filename to send (or 'exit' to quit): ")
            if filename.lower() == "exit":
                break
            send_file(client_socket, filename)
            time.sleep(2)
        elif message.lower() == "receive":
            client_socket.send("receive".encode())
            try:
                receive_file(client_socket, output_filename)
                time.sleep(2)
            except KeyboardInterrupt:
                print("Receive client terminated.")
                break
        else:
            print("Invalid command. Please enter 'send' or 'receive'.")

    client_socket.close()

if __name__ == "__main__":
    main()
