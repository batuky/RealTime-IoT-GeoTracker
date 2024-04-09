import socket
import threading

# TCP Sunucusu Ayarları
TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024  # Alınacak maksimum veri miktarı

def client_thread(conn, ip, port):
    """İstemci bağlantısı için bir thread işlevi."""
    with conn:
        print(f'Bağlanılan IP: {ip}, Port: {port}')
        try:
            while True:
                data = conn.recv(BUFFER_SIZE)
                if not data:
                    break
                print(f"Alınan veri: {data.decode()}")
        except ConnectionResetError:
            print(f"Bağlantı kesildi: IP {ip}, Port {port}")
        print(f"Bağlantı sonlandı: IP {ip}, Port {port}")

def start_server():
    """TCP sunucusunu başlat ve istemci bağlantılarını kabul et."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((TCP_IP, TCP_PORT))
        s.listen()
        print(f"Sunucu {TCP_IP} üzerinde {TCP_PORT} portunu dinliyor...")
        
        while True:
            conn, addr = s.accept()
            threading.Thread(target=client_thread, args=(conn, addr[0], addr[1])).start()

if __name__ == "__main__":
    start_server()