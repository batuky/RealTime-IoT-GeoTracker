import socket
import threading
import re
from queue_manager import QueueManager

class TCPServer:
    # TCP Server Settings
    TCP_IP = '127.0.0.1'
    TCP_PORT = 5005
    BUFFER_SIZE = 1024  # Maximum amount of data to be received

    # Regex pattern to validate data
    MESSAGE_PATTERN = re.compile(
        r"Device (\d{1,2}) - Time: (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}), "
        r"Location: \((-?\d+\.\d+), (-?\d+\.\d+)\)"
    )

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        rabbitmq_url = r'amqp://guest:guest@127.0.0.1:5672/%2F'
        self.queue_manager = QueueManager(rabbitmq_url)
    
    def is_valid_message(self, message):
        """Validate the format of the incoming message."""
        return self.MESSAGE_PATTERN.fullmatch(message) is not None

    def client_thread(self, conn, ip, port):
        """Thread function for client connection."""
        with conn:
            print(f'Connected IP: {ip}, Port: {port}')
            try:
                while True:
                    data = conn.recv(self.BUFFER_SIZE)
                    if not data:
                        break
                    message = data.decode()
                    if self.is_valid_message(message):
                        print(f"Valid data received: {message}")
                        self.queue_manager.send_message(message)
                    else:
                        print(f"Invalid data: {message}")
            except ConnectionResetError:
                print(f"Connection lost: IP {ip}, Port {port}")
            finally:
                print(f"Connection terminated: IP {ip}, Port {port}")

    def start_server(self):
        """Start the TCP server and accept client connections."""
        self.socket.bind((self.TCP_IP, self.TCP_PORT))
        self.socket.listen()
        print(f"Server is listening on {self.TCP_IP} port {self.TCP_PORT}...")
        
        try:
            while True:
                conn, addr = self.socket.accept()
                threading.Thread(target=self.client_thread, args=(conn, addr[0], addr[1])).start()
        except KeyboardInterrupt:
            print("Server is shutting down...")
            self.socket.close()
        except Exception as e:
            print(f"Error: {e}")
            self.socket.close()

if __name__ == "__main__":
    server = TCPServer()
    server.start_server()