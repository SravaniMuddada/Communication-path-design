import socket
import threading
import psutil

# Store client sockets and their names in a list
clients = []
clients_lock = threading.Lock()  # To prevent race conditions

def handle_client(client_socket):
    try:
        cpu_before = psutil.cpu_percent()
        while True:
            data = client_socket.recv(1024)
            #print(data) #print data at master node
        
            if not data:
                print("Client disconnected")
                break
            
            # Send the received data to all other connected clients
            with clients_lock:
                for other_client, _ in clients:
                    if other_client != client_socket:
                        try:
                            other_client.send(data)
                        except Exception as e:
                            print(f"Error sending data to a client: {e}")
                            other_client.close()
                            clients.remove((other_client, _))
        cpu_after = psutil.cpu_percent()
        print(f"CPU Utilization (send): {cpu_after}%")

    except Exception as e:
        print(f"Error handling client: {e}")

    finally:
        # Remove the client socket from the list on disconnect
        with clients_lock:
            for i, (client, name) in enumerate(clients):
                if client == client_socket:
                    clients.pop(i)
                    break
        client_socket.close()
        print_all_clients()  # Print all clients after one disconnects

def print_all_clients():
    print("Connected clients:")
    with clients_lock:
        for _, name in clients:
            print(name)

def main():
    master_ip = '192.168.137.68'  # Bind to all available network interfaces
    master_port = 5001

    master_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    master_socket.bind((master_ip, master_port))
    master_socket.listen(2)  # Listen for up to 2 clients (you can adjust this as needed)

    print("Server listening on", master_ip, "port", master_port)

    while True:
        client_socket, client_address = master_socket.accept()
        client_ip = client_address[0]
        try:
            client_name = socket.gethostbyaddr(client_ip)[0]
        except socket.herror:
            client_name = "Unknown host"
        print(f"Connected to client at {client_address} (Hostname: {client_name})")

        # Add the client socket and name to the list
        with clients_lock:
            clients.append((client_socket, client_name))
        print_all_clients()  # Print all clients after a new one connects

        # Start a new thread to handle the client
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    main()
