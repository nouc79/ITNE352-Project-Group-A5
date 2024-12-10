import socket
import threading
import json
from urllib import request


# Function to fetch news from NewsAPI
def fetch_news():
    API_KEY = "c23b132ee7ae4d1aad0ef2a8924af422"
    api_url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}"  # Static endpoint for top headlines
    response = request.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

# Handle client
def handle_client(client_socket, client_address):
    try:
        # I will receive the client's name and store it.
        client_socket.send("Enter your name please:".encode("utf-8"))
        client_name = client_socket.recv(1024).decode("utf-8")
        print(f"{client_address} connected as {client_name}")

        while True:
            # Now I will wait for the request from the client.
            client_socket.send("Requesting news articles...".encode("utf-8"))
            client_request = client_socket.recv(1024).decode("utf-8").strip()
            # If it disconnected (The client).
            if client_request.lower() == "quit":  
                print(f"{client_name} disconnected.")
                break

            print(f"{client_name} requested news articles.")

            # Fetch news data from the API
            news_data = fetch_news()
            if news_data is None:
                client_socket.send("Failed to fetch news data.".encode("utf-8"))
                continue

            # Now I will save the data to a JSON file.
            file_name = f"client_data/{client_name}_news_data.json"
            with open(file_name, "w") as json_file:
                json.dump(news_data, json_file, indent=4)
            print(f"Data successfully saved to: {file_name}")

            # Send a list of articles to the client if available
            articles = news_data.get('articles', [])
            if articles:
                # If articles are found, send the titles to the client.
                titles = [article['title'] for article in articles]
                client_socket.send(json.dumps({"options": titles}).encode("utf-8"))
            else:
                # If no articles are found, inform the client.
                client_socket.send("No articles found.".encode("utf-8"))
                continue

            # Ask the client to choose an item from the list.
            client_socket.send("Choose an item from the list: ".encode("utf-8"))
            selected_item = client_socket.recv(1024).decode("utf-8").strip()

            # Check if the selected item is valid.
            if selected_item in titles:
                # If the item is valid, send the corresponding info to the client.
                details = next((article for article in articles if article['title'] == selected_item), None)
                client_socket.send(json.dumps({"details": details}).encode("utf-8"))
            else:
                # If the selected item is invalid, tell the client to try again.
                client_socket.send("Invalid selection, try again.".encode("utf-8"))

    except Exception as e:
        print(f"Something went wrong with client {client_address}: {e}")
    finally:
        print(f"{client_name} has disconnected.")
        client_socket.close()

# The server will start and wait for clients
def start_Server(host="127.0.0.1", port=5501):
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