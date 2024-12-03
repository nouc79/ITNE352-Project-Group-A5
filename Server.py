import socket #To create the TCP.
import threading #To handle multiple client at the same time.
import json#Saving data in JSON file.
from urllib import request, response 
import Client

def handle_client(client_socket, client_address) :
    # I will recvie the clinet name here & store it.
client_socket.send("Enter your name:")
Client=client_socket.recv(1000).decode('utf-8')
print(f"+Connection:{client_address} from {Client}")

    # Waiting for the request from Clinet.
request =client_socket.recv(1000).decode('utf-8')
if not request : return
print(f"You get request from {Client}:{request}") 

#response, Client=request(Client,answer)
#handle_client.sendall(response.encode('utf-8'))

client_socket.send(json.dumps(response).encode('utf-8'))

# The server will start and waiting for client 
def start_Server(host="0.0.0.0",port=8999):
Server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
Server_socket.listen(3)
Server_socket.bind(host,port)
print("Server is working, waiting to client.....")

# if it true we will accept new client
while True :
 client_socket, client_address = server_socket.accept()
 print(f"New connection from {client_address}")

 start_Server()

#finally:
 #       server_socket.close()

#def handle_request(request):