import socket
from PIL import Image
from utils.epd_image_processor import convert_image_to_bytes

ACK: bytes = (6).to_bytes()

SERVER_IP = '0.0.0.0'
SERVER_PORT = 5000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen(1)

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
print(f"Server available at {ip_address}:{SERVER_PORT}")

payload = convert_image_to_bytes(
    # Image.open("C:/Users/peppo/mcal/utils/test_image.png"), (768, 960),
    Image.open("C:/Users/peppo/mcal/render/calendar.png"), (768, 960),    
)

client_socket, client_address = server_socket.accept()
print(f"Connection from {client_address} established.")

data_to_send = payload + payload
# data_to_send = "\x00" * (960 * 768 // 8)
# data_to_send = data_to_send.encode("latin1")
client_socket.sendall(data_to_send)
print(f"Sent {len(data_to_send)} bytes: {data_to_send[:8]} ... {data_to_send[-8:]}")
if client_socket.recv(1) == ACK:
    print(f"{ip_address} transfer complete and begin processing")
