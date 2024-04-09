import threading
import time
import random
import socket


# Constants
DEVICE_COUNT = 20
MIN_LATITUDE = -90.0
MAX_LATITUDE = 90.0
MIN_LONGITUDE = -180.0
MAX_LONGITUDE = 180.0
MIN_SLEEP_SECONDS = 1
MAX_SLEEP_SECONDS = 5
TCP_IP = '127.0.0.1'  
TCP_PORT = 5005       

def generate_random_location():
    """Generate a random GPS location."""
    latitude = random.uniform(MIN_LATITUDE, MAX_LATITUDE)
    longitude = random.uniform(MIN_LONGITUDE, MAX_LONGITUDE)
    return latitude, longitude

def simulate_device(device_id):
    """Simulate a device generating GPS location data at random intervals."""
    while True:
        latitude, longitude = generate_random_location()
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
        message = f"Device {device_id:02d} - Time: {timestamp}, Location: ({latitude:.6f}, {longitude:.6f})"
        print(message)
        send_to_server(device_id, message)
        time.sleep(random.randint(MIN_SLEEP_SECONDS, MAX_SLEEP_SECONDS))

def start_simulation(device_count):
    """Start the simulation for a given number of devices."""
    threads = []
    for device_id in range(device_count):
        thread = threading.Thread(target=simulate_device, args=(device_id,))
        thread.daemon = True
        threads.append(thread)
        thread.start()
    return threads

def send_to_server(device_id, message):
    """TCP sunucusuna veri gönder."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((TCP_IP, TCP_PORT))
            s.sendall(message.encode('utf-8'))
        except ConnectionRefusedError:
            print(f"Device {device_id:02d} - Sunucu bağlantıyı reddetti.")

if __name__ == "__main__":
    try:
        threads = start_simulation(DEVICE_COUNT)
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nSimulation stopped by the user.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")