import socket
import os
import time
import psutil
import mysql.connector

# Function to get CPU utilization
def get_cpu_utilization():
    return psutil.cpu_percent(percpu=False)

# Function to create the table if it does not exist
def create_table_if_not_exists(mycursor, column_names):
    try:
        columns = ', '.join([f"`{name}` DOUBLE NOT NULL" for name in column_names])
        create_table_query = f'''
        CREATE TABLE IF NOT EXISTS `sensor_data` (
            id INT AUTO_INCREMENT PRIMARY KEY,
            {columns}
        )
        '''
        mycursor.execute(create_table_query)
        print("Table `sensor_data` ensured to exist.")
    except mysql.connector.Error as e:
        print(f"MySQL error while creating table: {e}")

# Function to save data to the database
def save_to_database(column_names, values):
    try:
        print("Connecting to the database...")
        mydb = mysql.connector.connect(  #give database user name and Password here
            host="localhost",
            user="root",
            password="xxxxx",
            database="radar_data01"  #database name(Schemas)
        )
        print("Connected to the database.")
        
        mycursor = mydb.cursor()
        
        create_table_if_not_exists(mycursor, column_names)

        placeholders = ', '.join(['%s'] * len(values))
        columns = ', '.join([f"`{name}`" for name in column_names])
        sql = f'''
        INSERT INTO `sensor_data` ({columns})
        VALUES ({placeholders})
        '''
        print(f"Executing SQL: {sql} with values: {values}")
        mycursor.execute(sql, values)
        
        mydb.commit()
        print("Data committed to the database.")
        
        mycursor.close()
        mydb.close()
        print("Database connection closed.")
        
    except mysql.connector.Error as e:
        print(f"MySQL error: {e}")

# Function to send file to the server
def send_file(client_socket, filename):
    try:
        filesize = os.path.getsize(filename)
        client_socket.send(f"{filename},{filesize}".encode())
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
        transmission_time = end_time - start_time
        print(f"File {filename} sent in {transmission_time:.2f} seconds")

    except Exception as e:
        print(f"Error sending file {filename}: {e}")

# Function to receive data and save to the database
def receive_data_and_save(client_socket):
    buffer = ""
    first_data_received = False
    column_names = []

    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                print("No data received. Breaking the loop.")
                break
            
            buffer += data
            lines = buffer.split('\n')
            buffer = lines[-1]

            for line in lines[:-1]:
                line = line.strip()
                if not line:
                    continue

                try:
                    values = list(map(float, line.split(',')))
                    
                    if not first_data_received:
                        column_names = [f"column{i+1}" for i in range(len(values))]
                        first_data_received = True

                    if len(values) == len(column_names):
                        #print(f"Parsed values: {values}")
                        save_to_database(column_names, values)
                        #print(f"Received and saved data: {line}")
                    else:
                        print(f"Data length mismatch: expected {len(column_names)} values, got {len(values)}")
                except ValueError as ve:
                    print(f"ValueError: {ve} for data: {line}")
                    continue
        except socket.error as e:
            print(f"Socket error: {e}")
            break
    print("Finished receiving data.") 

# Main function to handle TCP client operations
def main():
    server_ip = '192.168.137.68'  #give master IP address here
    server_port = 5001

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    print(f"Connected to server at {server_ip}:{server_port}")

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
            try:
                receive_data_and_save(client_socket)
                time.sleep(2)
            except KeyboardInterrupt:
                print("Receive client terminated.")
                break

    client_socket.close()

if __name__ == "__main__":
    main()
