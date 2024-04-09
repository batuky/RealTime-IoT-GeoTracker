import requests
import json
import os
import pika

class RabbitMQConsumer:
    def __init__(self, queue_name, rabbitmq_url, fastapi_url):
        self.queue_name = queue_name
        self.rabbitmq_url = rabbitmq_url
        self.fastapi_url = fastapi_url
        self.params = pika.URLParameters(self.rabbitmq_url)
        self.connection = pika.BlockingConnection(self.params)
        self.channel = self.connection.channel()

    def send_to_fastapi(self, data_dict):
        response = requests.post(
            self.fastapi_url,
            json=data_dict,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
        )
        print(f"Data sent to FastAPI, response status: {response.status_code}")

    def consume_message(self):
        self.channel.queue_declare(queue=self.queue_name, durable=True)
        
        print("Consumer started, waiting for messages...")

        for method_frame, properties, body in self.channel.consume(self.queue_name, inactivity_timeout=1, auto_ack=False):
            if method_frame:
                try:
                    data_dict = json.loads(body.decode())
                    print(f"Received message: {body.decode()}")
                    self.send_to_fastapi(data_dict)
                    self.channel.basic_ack(delivery_tag=method_frame.delivery_tag)
                except json.JSONDecodeError as e:
                    print(f"JSON decoding error: {e}")
            else:
                print("No messages received. Consumer is idle...")
                break

        self.connection.close()

if __name__ == "__main__":
    queue_name = 'iot_locations_queue'
    rabbitmq_url = 'amqp://guest:guest@host:5672/'
    fastapi_url = 'http://localhost:8000/device_data/'

    consumer = RabbitMQConsumer(queue_name, rabbitmq_url, fastapi_url)
    consumer.consume_message()