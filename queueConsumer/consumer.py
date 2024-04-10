import logging
import re
import requests
import json
import pika
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("worker_consumer")

class RabbitMQConsumer:
    def __init__(self, queue_name, rabbitmq_url, fastapi_url):
        self.queue_name = queue_name
        self.rabbitmq_url = rabbitmq_url
        self.fastapi_url = fastapi_url
        self.params = pika.URLParameters(self.rabbitmq_url)
        self.connection = pika.BlockingConnection(self.params)
        self.channel = self.connection.channel()

    def send_to_fastapi(self, json_data):
        response = requests.post(
            self.fastapi_url,
            json=json_data,
            headers={
                "Accept": "*/*",
            }
        )
        logger.info(f"Data sent to FastAPI, response status: {response.status_code}")
        print(f"Data sent to FastAPI, response status: {response.status_code}")

    def consume_message(self):
        self.channel.queue_declare(queue=self.queue_name)
        
        logger.info("Consumer started, waiting for messages...")
        print("Consumer started, waiting for messages...")
        while True:
            for method_frame, properties, body in self.channel.consume(self.queue_name, inactivity_timeout=1, auto_ack=False):
                if method_frame:
                    try:
                        decoded_body = body.decode()
                        json_data = self.parse_message_to_json(decoded_body)
                        print(json_data)
                        logger.info(f"Received message: {decoded_body}")
                        time.sleep(5)
                        self.send_to_fastapi(json_data)
                        self.channel.basic_ack(delivery_tag=method_frame.delivery_tag)
                    except json.JSONDecodeError as e:
                        logger.error(f"JSON decoding error: {e}")
                else:
                    logger.info("No messages received. Consumer is idle...")
                    break

            self.connection.close()


    def parse_message_to_json(self, message):
        # Regular expression to match the desired pattern
        pattern = r'Device (\d+) - Time: ([\d-]+\s[\d:]+), Location: \((-?\d+\.\d+),\s*(-?\d+\.\d+)\)'
        
        # Use regular expression to find the matching groups
        match = re.match(pattern, message)
        
        if not match:
            raise ValueError("Message format is incorrect")
        
        # Extract the device id, time, and location from the message
        device_id, time, latitude, longitude = match.groups()
        
        # Construct the dictionary
        message_dict = {
            "device_id": int(device_id),
            "time": time,
            "location": {
                "latitude": float(latitude),
                "longitude": float(longitude)
            }
        }
        
        # Convert the dictionary to a JSON string
        return message_dict

if __name__ == "__main__":
    queue_name = 'iot_location_queue'
    rabbitmq_url = r'amqp://guest:guest@127.0.0.1:5672/%2F'
    fastapi_url = 'http://127.0.0.1:8000/iot_data/'

    consumer = RabbitMQConsumer(queue_name, rabbitmq_url, fastapi_url)
    consumer.consume_message()