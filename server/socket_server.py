import sys
import socket
import random
from PIL import Image

from utils.epd_image_processor import convert_image_to_bytes

# Define the server's IP address and port
SERVER_IP = '0.0.0.0'  # Listen on all available network interfaces
SERVER_PORT = 5000      # Port to listen for incoming connections

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen(1)  # Listen for a single connection

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
print(f"Server available at {ip_address}:{SERVER_PORT}")



payload = convert_image_to_bytes(
    Image.open(("C:/Users/peppo/mcal/utils/test_image.png")),
    (768, 960),
)

# Data to be sent to the Pico W when requested

while True:
    # Wait for a client to connect (Pico W)
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address} established.")

    try:
        while True:
        # Receive data from the Pico W (optional, just to acknowledge the request)
            data = client_socket.recv(1024)
            print(f"Received request: {data.decode('utf-8')}")

            # Send the data back to the Pico W
            rand_asc = ""
            for i in range(92160-1):
                rand_asc += random.choice("01")


            data_to_send = rand_asc.encode()
            data_to_send += chr(253).encode("latin1")
            data_to_send = payload
            # data_to_send = payload.encode()
            client_socket.sendall(data_to_send)
            print(f"Sent data: {data_to_send[:8]} ... {data_to_send[-8:]}")
    finally:
        # Close the client connection
        client_socket.close()
        print("Client disconnected.")
