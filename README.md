# RealTime-IoT-GeoTracker

RealTime-IoT-GeoTracker is an application designed to solve a case study. The app generates random locations data from the simulated IoT devices, depending on how many IoT devices you want. The data is sent to a TCP server, where it is validated. The validated data is then sent to a queue, where it is consumed by a consumer. Finally, CRUD operations are performed on the consumed data using FASTAPI.

## Features

- IoT Device Simulation: Generates random location data from your specified number of simulated IoT devices. Generates random location data from simulated IoT devices.
- Logging: Comprehensive logging of activities and errors for troubleshooting and monitoring purposes.
- TCP Server for Data Collection: Collects location data from IoT devices using TCP.
- Data Validation: Validates data on the server to ensure its integrity and consistency.
- Queue System: Uses a message queue before writing incoming data to the database.
- CRUD Operations via RESTful API: Performs crud operations on consumed data using RESTful API.
- Testing: Comes with examples of tests of the service.


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

2. Create env variables. You can see variables and example values on the example.
   ```sh
      rabbitmq_url = 'amqp://guest:guest@127.0.0.1:5672/%2F'
      queue_name = 'iot_location_queue'
      fastapi_url = 'http://127.0.0.1:8000/locations-data/'
      database_url = 'postgresql://postgres:admin@127.0.0.1/postgres'
      TCP_IP = '127.0.0.1'
   ```

3. Navigate to the project directory.

   On different terminals

   - Navigate main project directory ,and run FastAPI on main directory
   ```sh
   uvicorn fastAPIApp.main:app --reload
   ```

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
   
   - Navigate queueConsumer ,and run the consumer

   ```sh
   cd .\queueConsumer\
   ```
   ```sh
   python .\consumer.py
   ```

### API endpoints

   - POST/locations-data/: Create a new data.
   - GET/locations-data/: List all datas.
   - GET/locations-data/{location_data_id}: Get a specific location.
   - GET/devices/{device_id}/locations: Get locations history of a specific device.
   - PUT/locations-data/{location_data_id}: Update a specific data.
   - DELETE/locations-data/{location_data_id}: Delete a a specific data.


### Architecture

![Architecture draw](asset/Architecture.png)
