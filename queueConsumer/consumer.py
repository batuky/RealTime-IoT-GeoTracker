import logging
import re
import requests
import json
import pika
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("consumer_logger")

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
            headers={"Content-Type": "application/json"}
        )

        print("sended data : ", response)
        logger.info(f"Data sent to FastAPI, response status: {response.status_code}")

    def consume_message(self):
        self.channel.queue_declare(queue=self.queue_name)

        logger.info("Consumer started, waiting for messages...")
        while True:
            for method_frame, properties, body in self.channel.consume(self.queue_name, inactivity_timeout=1, auto_ack=False):
                if method_frame:
                    try:
                        decoded_body = body.decode()
                        json_data = self.parse_message_to_json(decoded_body)
                        if json_data:
                            self.send_to_fastapi(json_data)
                            self.channel.basic_ack(delivery_tag=method_frame.delivery_tag)
                    except json.JSONDecodeError as e:
                        logger.error(f"JSON decoding error: {e}")
                    except Exception as e:
                        logger.error(f"Error processing message: {e}")
                else:
                    logger.info("No messages received. Consumer is idle...")
                    break

        self.connection.close()

    def parse_message_to_json(self, message):
        pattern = re.compile(r'Device (\d+) - Time: ([\d-]+\s[\d:]+) - Latitude: (-?\d+\.\d+) - Longitude: (-?\d+\.\d+)')
        match = pattern.match(message)
        if not match:
            logger.error("Message format is incorrect")
            return None
        
        device, time, latitude, longitude = match.groups()
        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except ValueError as e:
            logger.error(f"Error converting latitude or longitude to float: {e}")
        return {
            "device": device,
            "time": time,
            "latitude": latitude,
            "longitude": longitude
        }

if __name__ == "__main__":
    queue_name = 'iot_location_queue'
    rabbitmq_url = 'amqp://guest:guest@127.0.0.1:5672/%2F'
    fastapi_url = 'http://127.0.0.1:8000/locations-data/'

    consumer = RabbitMQConsumer(queue_name, rabbitmq_url, fastapi_url)
    consumer.consume_message()