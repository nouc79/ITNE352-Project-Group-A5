import socket  # To create the TCP.
import threading  # To handle multiple clients at the same time.
import json  # Saving data in JSON file.
from urllib import request, response 
import Client

def handle_client(client_socket, client_address):
    # I will receive the client name here & store it.
    client_socket.send("Enter your name:".encode('utf-8'))
    Client = client_socket.recv(1000).decode('utf-8')
    print(f"+Connection: {client_address} from {Client}")

    # Waiting for the request from the client.
    client_request = client_socket.recv(1000).decode('utf-8')
    if not client_request:
        return
    print(f"You get request from {Client}: {client_request}") 

    response = {"message": "Your request has been received."}
    client_socket.send(json.dumps(response).encode('utf-8'))

# The server will start and wait for clients
def start_Server(host="0.0.0.0", port=8999):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))  # Bind requires a tuple (host, port)
    server_socket.listen(3)
    print("Server is working, waiting for clients...")

    # If true, we will accept new clients
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"New connection from {client_address}")
        # We will Handle client in a separate thread
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

# Start the server
start_Server()