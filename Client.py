import json
import socket
import ssl

def connect_to_server():
    # Create a regular socket connection to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 5501))  # Connect to the SSL-enabled server

    # Wrap the socket with SSL for secure communication
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)  # Set SSL context for server authentication
    context.load_verify_locations("server.crt")  # Load server certificate to verify

    # Wrap the socket with SSL to encrypt the communication
    secure_client_socket = context.wrap_socket(client_socket, server_hostname="127.0.0.1")
    return secure_client_socket

def communicate_with_server(client_socket, message):
    # Send message to server
    client_socket.sendall(message.encode())  
    return client_socket.recv(5501).decode()  # Receive the server's response

def display_main_menu():
    print("\nMain Menu:")
    print("1. Search Headlines")
    print("2. List of Sources")
    print("3. Quit")

def display_headlines_menu():
    print("\nHeadlines Menu:")
    print("1. Search for Keyword")
    print("2. Search by Category")
    print("3. Search by Country")
    print("4. List All Headlines")
    print("5. Back to Main Menu")

def display_sources_menu():
    print("\nSources Menu:")
    print("1. Search by Category")
    print("2. Search by Country")
    print("3. Search by Language")
    print("4. List All Sources")
    print("5. Back to Main Menu")

def display_options(client_socket):
    while True:
        display_main_menu()
        option = input("Select an option (1-3): ")

        if option == '1':  # Search Headlines
            display_headlines_menu()
            headline_option = input("Select an option (1-5): ")
            if headline_option == '1':
                search_by_keyword(client_socket)
            elif headline_option == '2':
                search_by_category(client_socket)
            elif headline_option == '3':
                search_by_country(client_socket)
            elif headline_option == '4':
                list_all_headlines(client_socket)
            elif headline_option == '5':
                continue  # Go back to main menu
            else:
                print("Invalid option, please try again.")

        elif option == '2':  # List Sources
            display_sources_menu()
            source_option = input("Select an option (1-5): ")
            if source_option == '1':
                search_sources_by_category(client_socket)
            elif source_option == '2':
                search_sources_by_country(client_socket)
            elif source_option == '3':
                search_sources_by_language(client_socket)
            elif source_option == '4':
                list_all_sources(client_socket)
            elif source_option == '5':
                continue  # Go back to main menu
            else:
                print("Invalid option, please try again.")
        
        elif option == '3':  # Quit
            print("Quitting...")
            client_socket.sendall("Quit".encode())  # Send quit request to server
            client_socket.close()  # Close the connection
            break
        else:
            print("Invalid option, please try again.")

def search_by_keyword(client_socket):
    user_keyword = input("Enter your keyword: ").strip().lower()
    request_query = f"top-headlines?q={user_keyword}"
    send_request(client_socket, "headlines", request_query, "keyword")

def search_by_category(client_socket):
    category = input("Enter category (business, health, etc.): ").strip().lower()
    request_query = f"top-headlines?category={category}"
    send_request(client_socket, "headlines", request_query, "category")

def search_by_country(client_socket):
    country = input("Enter country code (e.g., us, ca): ").strip().lower()
    request_query = f"top-headlines?country={country}"
    send_request(client_socket, "headlines", request_query, "country")

def list_all_headlines(client_socket):
    print("Listing all headlines...")
    request_query = "top-headlines"
    send_request(client_socket, "headlines", request_query, "list")

def search_sources_by_category(client_socket):
    category = input("Enter category (business, health, etc.): ").strip().lower()
    request_query = f"sources?category={category}"
    send_request(client_socket, "sources", request_query, "category")

def search_sources_by_country(client_socket):
    country = input("Enter country code (e.g., us, ca): ").strip().lower()
    request_query = f"sources?country={country}"
    send_request(client_socket, "sources", request_query, "country")

def search_sources_by_language(client_socket):
    language = input("Enter language code (e.g., en, ar): ").strip().lower()
    request_query = f"sources?language={language}"
    send_request(client_socket, "sources", request_query, "language")

def list_all_sources(client_socket):
    print("Listing all sources...")
    request_query = "sources"
    send_request(client_socket, "sources", request_query, "list")

def send_request(client_socket, mode, request_query, option):
    collection = json.dumps({'type': mode, 'query': request_query, 'option': option})
    client_socket.sendall(collection.encode())  # Send the request to the server
    response = client_socket.recv(5501).decode()  # Receive the server's response
    try:
        response_data = json.loads(response)
        print(f"Server Response (JSON): {response_data}")
        if 'options' in response_data:
            display_response_options(response_data['options'])
        elif 'details' in response_data:
            display_item_details(response_data['details'])
        else:
            print(response_data)  # Handle any other message
    except json.JSONDecodeError:
        print(f"Server Response: {response}")  # Handle non-JSON response

def display_response_options(options):
    print("\nResults:")
    for idx, option in enumerate(options, 1):
        print(f"{idx}. {option}")
    selected_option = input("Select an option for details: ")
    # Send the selected item back to the server to retrieve full details
    client_socket.sendall(selected_option.encode())

def display_item_details(details):
    print("\nItem Details:")
    for key, value in details.items():
        print(f"{key}: {value}")

def main():
    client_socket = connect_to_server()
    username = input("Enter your username: ")
    client_socket.sendall(username.encode())  # Send username to server
    display_options(client_socket)

if __name__ == "__main__":
    main()
