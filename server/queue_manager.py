import pika
from pika.exceptions import AMQPConnectionError, ChannelError

class QueueManager:
    def __init__(self, host='localhost', queue_name='iot_location_queue'):
        self.host = host
        self.queue_name = queue_name
        self.connection = None
        self.channel = None
        self.connect()

    def connect(self):
        try:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=self.host)
            )
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queue_name)
            print(f"Connected to RabbitMQ on {self.host}, declared queue '{self.queue_name}'")
        except AMQPConnectionError as error:
            print(f"Failed to connect to RabbitMQ: {error}")
            self.channel = None
            raise

    def send_message(self, message):
        if self.channel is None:
            print("Channel is not available. Attempting to reconnect...")
            self.connect()

        # After attempting to reconnect, if self.channel is still None, raise an exception.
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
            # If an error occurs at this point, it might be a good idea to set self.channel to None
            # and handle reconnection attempts the next time send_message is called.
            self.channel = None
            raise

    def close(self):
        if self.channel and self.channel.is_open:
            self.channel.close()
        if self.connection and self.connection.is_open:
            self.connection.close()
        print("RabbitMQ connection closed.")

if __name__ == "__main__":
    queue_manager = QueueManager()
    try:
        queue_manager.send_message("Test Message")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        queue_manager.close()