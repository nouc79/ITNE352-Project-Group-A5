# Server code
import socket
import threading
import json
import os
import requests



# Function to fetch news from NewsAPI
def fetch_news():
    url = 'https://newsapi.org/v2/top-headlines?country=us&apiKey=c23b132ee7ae4d1aad0ef2a8924af422'
    response = requests.get(url)
    return response.json()

# Handle client
def handle_client(client_socket, client_address):
    try:
        # I will receive the client's name and store it.
        client_socket.send("Enter your name please:".encode("utf-8"))
        client_name = client_socket.recv(5501).decode("utf-8")
        print(f"{client_address} connected as {client_name}")

        
        while True:
            # Now I will wait for the request from the client.
            client_socket.send("Enter your request option: ".encode("utf-8"))
            client_request = client_socket.recv(5501).decode("utf-8").strip()
            # If it disconnected(The client).
            if client_request.lower() == "quit":  
                print(f"{client_name} disconnected.")
                break

            print(f"{client_name} asked for: {client_request}")

            # Data for testing
            data = {
                "1": {"item1": "Details for the item1", "item2": "Details for item2"},
                "2": {"itemR": "Details for itemR", "itemN": "Details for itemN"},
                "3": {"itemX": "Details for itemX", "itemY": "Details for itemY"},
            }

            # Now I will save the data to a JSON file.
            file_name = f"client_data/{client_name}_option_{client_request}_A5.json"
            with open(file_name, "w") as json_file:
                json.dump(data, json_file, indent=4)
            print(f"Data successfully saved to: {file_name}")

            # Send a list to the client.
            if client_request in data:
                # If the client's request is valid, send the options.
                client_socket.send(json.dumps({"options": list(data[client_request].keys())}).encode("utf-8"))
            else:
                # If the request is invalid, Will print an invalid massage to the client.
                client_socket.send("Invalid option.".encode("utf-8"))
                continue

            # Ask the client to choose an item from the list.
            client_socket.send("Choose an item from the list: ".encode("utf-8"))
            selected_item = client_socket.recv(5501).decode("utf-8").strip()

            # Check if the selected item is valid.
            if selected_item in data.get(client_request, {}):
                # If the item is valid, send the info to the client.
                details = data[client_request][selected_item]
                client_socket.send(json.dumps({"details": details}).encode("utf-8"))
            else:
                # If the selected item is invalid, tell the client to try again.
                client_socket.send("Invalid try again.".encode("utf-8"))

    except Exception as e:
        print(f"Something went wrong with client {client_address}: {e}")
    finally:
        print(f"{client_name} has disconnected.")
        client_socket.close()

# The server will start and wait for clients
def start_Server(host="0.0.0.0", port=5501):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(3) 
    print("Waiting for clients...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"{client_address} connected.")

        # Start a new thread for the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

# Start the server
start_Server()