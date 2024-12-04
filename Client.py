# Client code
import socket

def connect_to_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 1234))  # Ensure the host and port match your server
    return client_socket

def communicate_with_server(client_socket, message):
    client_socket.sendall(message.encode())
    return client_socket.recv(1888).decode()

def display_main_menu():
    print("\nMain Menu:")
    print("1. Option 1")
    print("2. Option 2")
    print("3. Option 3")
    print("4. Quit")

def display_options(client_socket):
    while True:
        display_main_menu()
        option = input("Select an option (1-4): ")
         # Send option to server
        if option == '1':
            print("You selected Option 1.")
            client_socket.sendall(option.encode()) 
        elif option == '2':
            print("You selected Option 2.")
            client_socket.sendall(option.encode())  
        elif option == '3':
            print("You selected Option 3.")
            client_socket.sendall(option.encode())  
        elif option == '4':
            print("Quitting...")
            client_socket.sendall("Quit".encode()) 
            client_socket.close()  
            break
        else:
            print("Invalid option please try again.")

        # Receive and print the server's response
        response = communicate_with_server(client_socket, option)
        print(f"Server response: {response}")

def main():
    client_socket = connect_to_server()
    username = input("Enter your username: ")  # Get username
    client_socket.sendall(username.encode())  # Send username to server
    display_options(client_socket)

if __name__ == "__main__":
    main()
