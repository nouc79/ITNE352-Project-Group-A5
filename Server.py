import socket
import threading
import json
import ssl
from urllib import request

# Configuration of the server
S_HOST = '0.0.0.0'
S_PORT = 5501
API_KEY = "c23b132ee7ae4d1aad0ef2a8924af422"
GROUP_ID = "A5"

# Retrieve headline information from the API
def process_headlines(news_data):
    articles = []
    for article in news_data.get('articles', []):
        articles.append({
            'source_name': article.get('source', {}).get('name'),
            'author': article.get('author'),
            'title': article.get('title'),
            'url': article.get('url'),
            'description': article.get('description'),
            'publish_date': article.get('publishedAt', '')[:10],  # Fixed the slicing to get the date
            'publish_time': article.get('publishedAt', '')[11:19],  # Fixed the slicing to get the time
        })
    return articles

# Handle the source data from the API response
def process_sources(news_data):
    sources = []
    for source in news_data.get('sources', []):
        sources.append({
            'source_name': source.get('name'),
            'country': source.get('country'),
            'description': source.get('description'),
            'url': source.get('url'),
            'category': source.get('category'),
            'language': source.get('language'),
        })
    return sources

# Handle client requests
def process_request(Csocket, query, requested_type, user_name):
    api_endpoint = f'https://newsapi.org/v2/{query}&apiKey={API_KEY}'
    resp = request.get(api_endpoint)
    if resp.status_code == 200:
        news_data = resp.json()
    else:
        print(f"Error has been found:  {resp.status_code}")
        return

    # Store data in a JSON file
    FName = f"{user_name}{requested_type}{GROUP_ID}.json"
    with open(FName, 'w') as json_file:
        json.dump(news_data, json_file, indent=5)
    
    # Sending data to the client
    if requested_type == "headlines":
        articles = process_headlines(news_data)
        response_data = {'type': 'headlines', 'data': articles[:20]}
        Csocket.send(json.dumps(response_data).encode())
    elif requested_type == "sources":
        sources = process_sources(news_data)
        response_data = {'type': 'sources', 'data': sources[:20]}
        Csocket.send(json.dumps(response_data).encode())

# Handle client requests
def client_request_handler(Csocket, user_name):
    while True:
        requested_data = Csocket.recv(1024).decode()
        if requested_data.lower() == "exit":
            print(f"{user_name} got disconnected")
            Csocket.close()
            break
         
        request = json.loads(requested_data)
        query = request.get('query')
        requested_type = request.get('type')

        print(f"Request from {user_name}: with Query: {query}, and Type: {requested_type}")
        process_request(Csocket, query, requested_type, user_name)

# Configure and run the server with SSL
def main():
    try:
        # Creating server socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as Ssocket:
            Ssocket.bind((S_HOST, S_PORT))
            Ssocket.listen(3)
            print(f"Server is on, with port: {S_PORT}")

            # Wrap the server socket with SSL
            context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            context.load_cert_chain(certfile="server.crt", keyfile="private.key")

            # Protect the server socket with SSL
            secure_socket = context.wrap_socket(Ssocket, server_side=True)

            while True:
                try:
                    Csocket, Caddress = secure_socket.accept()
                    user_name = Csocket.recv(1024).decode()
                    print(f"Connection started by {user_name} at {Caddress}")
                    
                    # Create a new thread to manage the client
                    Cthread = threading.Thread(target=client_request_handler, args=(Csocket, user_name))
                    Cthread.start()
                except Exception as e:
                    print(f"Error handling client: {e}")
    except Exception as e:
        print(f"Server error: {e}")
if __name__ == "__main__":
    main()