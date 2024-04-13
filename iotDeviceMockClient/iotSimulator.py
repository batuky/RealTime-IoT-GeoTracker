import threading
import time
import random
import socket

class IoTDeviceSimulator:
    # Constants
    DEVICE_COUNT = 2
    MIN_LATITUDE = -90.0
    MAX_LATITUDE = 90.0
    MIN_LONGITUDE = -180.0
    MAX_LONGITUDE = 180.0
    MIN_SLEEP_SECONDS = 3
    MAX_SLEEP_SECONDS = 6
    TCP_IP = '127.0.0.1'
    TCP_PORT = 5005

    def __init__(self, device_id):
        self.device_id = device_id

    def generate_random_location(self):
        """Generate a random GPS location."""
        latitude = random.uniform(self.MIN_LATITUDE, self.MAX_LATITUDE)
        longitude = random.uniform(self.MIN_LONGITUDE, self.MAX_LONGITUDE)
        return latitude, longitude

    def simulate(self):
        """Simulate a device generating GPS location data at random intervals."""
        while True:
            latitude, longitude = self.generate_random_location()
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
            message = f"Device {self.device_id} - Time: {timestamp} - Latitude: {latitude} - Longitude: {longitude}"
            print(message)
            self.send_to_server(message)
            time.sleep(random.randint(self.MIN_SLEEP_SECONDS, self.MAX_SLEEP_SECONDS))

    def send_to_server(self, message):
        """Send data to the TCP server with a timeout."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(10)
            try:
                sock.connect((self.TCP_IP, self.TCP_PORT))
                sock.sendall(message.encode('utf-8'))
            except socket.timeout:
                print(f"Device {self.device_id} - Server timeout.")
            except ConnectionRefusedError:
                print(f"Device {self.device_id} - Server connection refused.")
            except Exception as e:
                print(f"Device {self.device_id} - An error occurred: {e}")

def start_simulation(device_count):
    """Start the simulation for a given number of devices."""
    threads = []
    for device_id in range(1, device_count + 1):  # Başlangıç değeri 1, bitiş değeri device_count + 1
        device_simulator = IoTDeviceSimulator(device_id)
        thread = threading.Thread(target=device_simulator.simulate)
        thread.daemon = True
        threads.append(thread)
        thread.start()
    return threads

if __name__ == "__main__":
    try:
        threads = start_simulation(IoTDeviceSimulator.DEVICE_COUNT)
        # Keep the main thread alive.
        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        print("\nSimulation stopped by the user.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")