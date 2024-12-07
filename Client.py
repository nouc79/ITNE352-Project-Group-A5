import json
import socket

def connect_to_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 5501))
    return client_socket

def communicate_with_server(client_socket, message):
    client_socket.sendall(message.encode())
    return client_socket.recv(5501).decode()

def display_main_menu():
    print("\nMain Menu:")
    print("1. Search Headlines")
    print("2. List of Sources")
    print("3. Quit")

def display_options(client_socket):
    while True:
        display_main_menu()
        option = input("Select an option (1-3): ")

        # Send option to server
        if option == '1':
            search_by_keyword(client_socket)
        elif option == '2':
            list_of_sources(client_socket)
        elif option == '3':
            print("Quitting...")
            client_socket.sendall("Quit".encode())
            client_socket.close()
            break
        else:
            print("Invalid option please try again.")

def search_by_keyword(client_socket):
    user_keyword = input("Enter your keyword: ").strip().lower()
    request_query = f"top-headlines?q={user_keyword}"
    send_request(client_socket, "headlines", request_query, "keyword")

def list_of_sources(client_socket):
    print("Listing all sources...")
    send_request(client_socket, "sources", "all", "list")

def send_request(client_socket, mode, request_query, option):
    collection = json.dumps({'type': mode, 'query': request_query, 'option': option})
    client_socket.sendall(collection.encode())
    response = client_socket.recv(5501).decode()
    try:
        response_data = json.loads(response)
        print(f"Server Response (JSON): {response_data}")
    except json.JSONDecodeError:
        print(f"Server Response: {response}")

def main():
    client_socket = connect_to_server()
    # Get username
    username = input("Enter your username: ")
    # Send username to server
    client_socket.sendall(username.encode())
    display_options(client_socket)

if __name__ == "__main__":
    main()