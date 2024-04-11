# evreka-iot-gps

evreka-iot-gps is an application designed to solve a case study. The application generates random location data from 20 simulated IoT devices. The data is sent to a TCP server, where it is validated. The validated data is then sent to a queue, where it is consumed by a consumer. Finally, CRUD operations are performed on the consumed data using FASTAPI.

## Features

IoT Device Simulation: Generates random location data from simulated IoT devices.
Logging: Comprehensive logging of activities and errors for troubleshooting and monitoring purposes.
TCP Server for Data Collection: Collects location data from IoT devices using TCP.
Data Validation: Validates data on the server to ensure its integrity and consistency.
Queue System: Uses a message queue before writing incoming data to the database.
CRUD Operations via RESTful API: Performs crud operations on consumed data using RESTful API.


Note: IOT device mock client, tcp server and queue consumer are working, but fastAPI is not working as intended. Problem: The data coming to FastAPI and the data in the return value do not match.

## Getting Started

### Prerequisites
- Python 3.8+
- FastAPI
- Uvicorn for running FastAPI
- RabbitMQ
- PostgreSQL


### Installation
1. Clon the repository.
   ```sh
   git https://github.com/batuky/evreka-iot-gps.git
   ```

2. Navigate to the project directory.

   On different terminals
   
   - Navigate tcpServer directory ,and run the tcp server.
   ```sh
   cd .\tcpServer\
   ```
   ```sh
   python .\tcpServer.py
   ```
   
   - Navigate iotDeviceMockClient ,and run the iotSimulator

   ```sh
   cd .\iotDeviceMockClient\
   ```
   ```sh
   python .\iotSimulator.py
   ```
   
   - Navigate main project directory ,and run FastAPI on main directory
   ```sh
   uvicorn fastAPIApp.main:app --reload
   ```
   
   - Navigate queueConsumer ,and run the consumer

   ```sh
   cd .\queueConsumer\
   ```
   ```sh
   python .\consumer.py
   ```