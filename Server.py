import socket  # To create the TCP connection.
import threading  # To handle multiple clients at the same time.
import json  # For saving data in a JSON file.
import os  # To ensure directories exist.

def handle_client(client_socket, client_address):
    try:
        # I will receive the client's name and store it.
        client_socket.send("Enter your name please:".encode("utf-8"))
        client_name = client_socket.recv(1888).decode("utf-8")
        print(f"{client_address} as {client_name}")

        while True:
            # Now I will wait for the request from the client.
            client_socket.send("Enter your request option: ".encode("utf-8"))
            client_request = client_socket.recv(1888).decode("utf-8")
            
            # If the client disconnects.
            if not client_request:
                print(f"{client_name} disconnects.")
                break
            
            print(f"{client_name} asked for: {client_request}")

            # Data for testing.
            data = {
                "option1": {"item1": "Details for the item1", "item2": "Details for item2"},
                "option2": {"itemR": "Details for itemR", "itemN": "Details for itemN"},
            }

            # Now I will save the data to a JSON file.
            file_name = f"client_data/{client_name}_{client_request}_A5.json"
            with open(file_name, "w") as json_file:
                json.dump(data, json_file, indent=4)
            print(f"Data successfully saved to: {file_name}")

            # Send a list to the client.
            if client_request in data:
                # If the client's request is valid, send the options (like a list of items(R or N)).
                client_socket.send(json.dumps({"options": list(data[client_request].keys())}).encode("utf-8"))
            else:
                # If the request is invalid, tell the client it's not a valid option.
                client_socket.send("Invalid request option.".encode("utf-8"))

            # Ask the client to choose an item from the list.
            client_socket.send("Choose an item from the list: ".encode("utf-8"))
            selected_item = client_socket.recv(1024).decode("utf-8")

            # Check if the selected item is valid.
            if selected_item in data.get(client_request, {}):
                # If the item is valid, send the details to the client.
                client_socket.send(json.dumps({"details": data[client_request][selected_item]}).encode("utf-8"))

            else:
                # If the select item is invalid, it will the client to try again.
                client_socket.send("Invalid try again.".encode("utf-8"))

    except Exception as e:
        print(f"Something wrong with client {client_address}: {e}")
    finally:
        print(f" {client_name} has disconnected.")
        client_socket.close()

# The server will start and wait for clients
def start_Server(host="0.0.0.0", port=8999):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(3)  # Accept up to 3 simultaneous connections
    print("Waiting for clients...")
    
    while True:  
        client_socket, client_address = server_socket.accept()
        print(f"{client_address} connected.")

        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

# Start the server
start_Server()

