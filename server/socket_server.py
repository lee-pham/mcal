import sys
import socket
import random
from PIL import Image

from utils.epd_image_processor import convert_image_to_bytes

SERVER_IP = '0.0.0.0'
SERVER_PORT = 5000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen(1)

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
print(f"Server available at {ip_address}:{SERVER_PORT}")

payload = convert_image_to_bytes(
    Image.open(("C:/Users/peppo/mcal/utils/test_image.png")),
    (768, 960),
)

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address} established.")

    try:
        while True:
            data = client_socket.recv(1024)
            print(f"Received request: {data.decode('utf-8')}")

            data_to_send = payload
            client_socket.sendall(data_to_send)
            print(f"Sent data: {data_to_send[:8]} ... {data_to_send[-8:]}")
    finally:
        client_socket.close()
        print("Client disconnected.")
