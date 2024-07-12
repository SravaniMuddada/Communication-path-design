# Doppler Weather Radar Data Handling System
Welcome to the Doppler Weather Radar Data Handling System repository! This project presents an efficient and reliable data handling system for local area network (LAN) applications, specifically designed to meet the needs of Doppler weather radar systems. The system ensures optimal resource use, smooth data transfer, and complete data integrity.
## Table of Contents
- [Introduction](#introduction)
- [System Architecture](#system-architecture)
- [Features](#features)
  ## Introduction

The Raspberry Pi is an excellent platform for networking activities due to its small size, strong computing capability, and low power consumption. This project leverages the Raspberry Pi's dependable connectivity options to simplify network construction for Doppler weather radar systems. The proposed system ensures efficient data handling, reliable data transfer, and secure data storage.

## System Architecture

The suggested architecture consists of a main server, two slave nodes, and one master node connected in a star topology, as illustrated in Figure 3.2. Devices are connected through Wi-Fi, and the architecture is designed to manage data transit between nodes efficiently. There are three types of nodes in this architecture:

### Master Node

The master node serves as the central hub of the network, responsible for:
- **Data Transfer:** Ensures data packets are correctly routed from sender to receiver.
- **Network Monitoring:** Tracks important metrics like latency, resource utilization, and bandwidth usage to optimize network performance.
- **Task Management:** Assigns tasks to different nodes, coordinates their execution, and manages node connections for security and order.

Additionally, the master node facilitates the connection process for new client nodes, ensuring quick and easy integration into the network.

### Main Server Node

The main server node acts as a centralized repository for storing information gathered from various network sources. It provides crucial services such as maintaining a radar main station and a clients’ database. Each client’s information is stored in separate database tables or collections to enhance security and organization. The main server node also implements data retention policies to manage the lifecycle of stored data, ensuring compliance with legal and operational requirements.

### Client Nodes

Client nodes access data from the main server based on their specific needs and schedules. The master node coordinates these data transfer requests, ensuring that clients receive the data they need promptly and efficiently.

## Data Transfer Mechanism

The network supports both offline and real-time data processing modes.
### File Data Transfer

Socket communication is used to transfer variable-size files between clients through the server. This design minimizes overhead and transmission latency by avoiding intermediate file read/write operations.

### Real-Time Data Transfer

For real-time data transfer, Raspberry Pi clients continuously acquire data from the radar system. Data is pre-processed and converted to digital format before being sent to the main server, ensuring seamless and efficient data communication.

## Features

- **Efficient Data Handling:** Optimized resource use and smooth data transfer.
- **Reliable Connectivity:** Wi-Fi connection and TCP/IP protocol for dependable communication.
- **Secure Data Storage:** Database services on the main server ensure complete data integrity.
- **Robust Performance:** The system exhibits stable behavior even with minor delays and disturbances.


