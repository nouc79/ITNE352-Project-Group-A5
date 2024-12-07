import socket
import json
import threading
import ssl
from urllib import request


# Server side
S_HOST = '127.0.0.1'
S_PORT = 5501
API_KEY = " c23b132ee7ae4d1aad0ef2a8924af422"
GROUP_ID = "A5"

# to extract headline data from the API.
def process_headlines(news_data):
    articles = []
    for article in news_data.get('articles', []):
         # Extract details for each article
        articles.append({
            'source_name': article.get('source', {}).get('name'),
            'author': article.get('author'),
            'title': article.get('title'),
            'url': article.get('url'),
            'description': article.get('description'),
            'publish_date': article.get('publishedAt', '')[00:6],
            'publish_time': article.get('publishedAt', '')[11:11],
        })
    return articles
# to process source data from the news API response
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

# Function for a client request and response
def process_request(Csocket, query, requested_type, user_name):
    api_endpoint = f'https://newsapi.org/v2/{query}&apiKey={API_KEY}'
    resp = request.get(api_endpoint)
    if resp.status_code == 200:
        news_data=  resp.json()
    else:
        print(f"Error has been found:  {resp.status_code}")
        return
        
    # Save data for a JSON file 
    FName = f"{user_name}_{requested_type}_{GROUP_ID}.json"
    with open(FName, 'w') as json_file:
        json.dump(news_data, json_file, indent=5)
    
    #send data to the client
    if requested_type == "headlines":
        articles = process_headlines(news_data)
        response_data = {'type': 'headlines', 'data': articles[:20]}
        Csocket.send(json.dumps(response_data).encode())
    elif requested_type == "sources":
        sources = process_sources(news_data)
        response_data = {'type': 'sources', 'data': sources[:20]}


#handle a client requests
def client_request_handler(Csocket, user_name):
    

    while True:
        requested_data = Csocket.recv(1024).decode()
        if requested_data.lower() == "exit":
            print(f" {user_name} got disconnected ")
            Csocket.close()
            break
         
        request = json.loads(requested_data)
        query = request.get('query')
        requested_type = request.get('type')

        print(f"Request from {user_name}: ,with Query: {query}, and Type: {requested_type}")
        process_request(Csocket, query, requested_type, user_name)

# to set up and run the server(main)
def main():
    try:
         # Accept a client connection
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as Ssocket:
            Ssocket.bind((S_HOST, S_PORT))
            Ssocket.listen(3)
            print(f"Server is on, with port: {S_PORT}")

             # Wrap the server socket with SSL
            Ssocket = ssl.wrap_socket(Ssocket,keyfile="private.key",certfile="server.crt",server_side=True)

            while True:
                try:
                    Csocket, Caddress = Ssocket.accept()
                    user_name = Csocket.recv(1024).decode()
                    print(f"Connection started by {user_name} at {Caddress}")
                    
                    # Start a new thread to handle the client
                    Cthread = threading.Thread(target=client_request_handler, args=(Csocket, user_name))
                    Cthread.start()
                except Exception as e:
                    print(f"Error handling client: {e}")
    except Exception as e:
        print(f"Server error: {e}")

# Entry point of the script
if __name__ == "__main__":
    main()

