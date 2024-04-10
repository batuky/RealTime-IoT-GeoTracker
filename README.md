# evreka-iot-gps

evreka-iot-gps is an application designed to solve a case study. The application generates random location data from 20 simulated IoT devices. The data is sent to a TCP server, where it is validated. The validated data is then sent to a queue, where it is consumed by a consumer. Finally, CRUD operations are performed on the consumed data using FASTAPI.

## Features

IoT Device Simulation: Generates random location data from simulated IoT devices.
Logging: Comprehensive logging of activities and errors for troubleshooting and monitoring purposes.
TCP Server for Data Collection: Collects location data from IoT devices using TCP.
Data Validation: Validates data on the server to ensure its integrity and consistency.
Queue System: Uses a message queue before writing incoming data to the database.
CRUD Operations via RESTful API: Performs crud operations on consumed data using RESTful API.
Testing: Comes with examples of unit and integration tests to ensure the reliability of the service.

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

change file names.
app - fastAPIApp
iotDevice - iotDeviceMockClient
server - TCPServer
worker - queueConsumer

sürekli port açmaması için 

