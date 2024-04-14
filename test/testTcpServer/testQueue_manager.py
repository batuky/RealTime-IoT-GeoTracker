import datetime
import re
import pika
from pika.exceptions import AMQPConnectionError, ChannelError
from unittest.mock import MagicMock, patch

class MockQueueManager:
    def __init__(self, rabbitmq_url, queue_name='test_queue'):
        self.queue_name = queue_name
        self.rabbitmq_url = rabbitmq_url
        self.connection = None
        self.channel = None
        # Immediately attempt to connect
        self.connect()

    def is_valid_message(self, message):
        valid_pattern = re.compile(
            r"Device (\d+) - Time: (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - Latitude: (-?\d+\.\d+) - Longitude: (-?\d+\.\d+)"
        )
        return valid_pattern.fullmatch(message) is not None

    def connect(self):
        try:
            params = pika.URLParameters(self.rabbitmq_url)
            self.connection = pika.BlockingConnection(params)
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queue_name, durable=True)
        except (AMQPConnectionError, ChannelError) as e:
            print(f"Error connecting to RabbitMQ: {e}")
            self.connection = None  # Set connection to None on failure
            self.channel = None  # Set channel to None on failure

    def send_message(self, message):
        if not self.is_valid_message(message):
            print(f"Invalid message format, not sent: {message}")
            return

        if self.channel is None:
            print("Channel is not available. Attempting to reconnect...")
            self.connect()

        if self.channel is None:
            raise Exception("Could not establish a channel to RabbitMQ.")

        if self.channel:  # Check if channel is not None
            self.channel.basic_publish(
                exchange='',
                routing_key=self.queue_name,
                body=message
            )
            print(f"Message sent to queue '{self.queue_name}': {message}")

    def close(self):
        if self.connection:
            self.connection.close()

# Test function using the MockQueueManager
@patch('pika.URLParameters')
@patch('pika.BlockingConnection')
def test_send_valid_message(mock_blocking_connection):
    rabbitmq_url = "amqp://guest:guest@localhost/"
    queue_name = "test_queue"

    manager = MockQueueManager(rabbitmq_url, queue_name)

    # Mock the channel object and its basic_publish method
    mock_channel = mock_blocking_connection.return_value.channel.return_value
    mock_channel.basic_publish = MagicMock()

    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"Device 99 - Time: {current_time} - Latitude: 01.000000000000000 - Longitude: 01.000000000000000"
    manager.send_message(message)
    assert mock_channel.basic_publish.called
    manager.close()

if __name__ == "__main__":
    test_send_valid_message()