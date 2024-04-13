import pika
from pika.exceptions import AMQPConnectionError, ChannelError
import re

class QueueManager:
    def __init__(self, rabbitmq_url, queue_name='iot_location_queue'):
        self.queue_name = queue_name
        self.connection = None
        self.channel = None
        self.rabbitmq_url = rabbitmq_url
        self.connect()
        self.valid_pattern = re.compile(
            r"Device (\d) - Time: (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - Latitude: (-?\d+\.\d+) - Longitude: (-?\d+\.\d+)"
        )

    def is_valid_message(self, message):
        """Validate the format of the incoming message against the predefined pattern."""
        return self.valid_pattern.fullmatch(message) is not None

    def connect(self):
        try:
            self.params = pika.URLParameters(self.rabbitmq_url)
            self.connection = pika.BlockingConnection(self.params)
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queue_name)
            print(f"Connected to RabbitMQ on {self.rabbitmq_url}, declared queue '{self.queue_name}'")
        except AMQPConnectionError as error:
            print(f"Failed to connect to RabbitMQ: {error}")
            self.channel = None
            raise

    def send_message(self, message):
        if self.is_valid_message(message):
            if self.channel is None:
                print("Channel is not available. Attempting to reconnect...")
                self.connect()

            if self.channel is None:
                raise Exception("Could not establish a channel to RabbitMQ.")

            try:
                self.channel.basic_publish(
                    exchange='',
                    routing_key=self.queue_name,
                    body=message
                )
                print(f"Message sent to queue '{self.queue_name}': {message}")
            except (ChannelError, AMQPConnectionError) as error:
                print(f"Failed to send message: {error}")
                self.channel = None
                raise
        else:
            print(f"Invalid message format, not sent: {message}")

    def close(self):
        if self.channel and self.channel.is_open:
            self.channel.close()
        if self.connection and self.connection.is_open:
            self.connection.close()
        print("RabbitMQ connection closed.")

if __name__ == "__main__":
    rabbitmq_url = r'amqp://guest:guest@127.0.0.1:5672/%2F'
    queue_manager = QueueManager(rabbitmq_url)

    try:
        queue_manager.send_message("Test Message")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        queue_manager.close()