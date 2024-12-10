Multithreaded News Client/Server Information System 

Descripition:The system includes server script and a client script. The server retrieves news from NewsAPI.org and shares it with clients. It can manage multiple clients simultaneously, providing them with news lists and details upon request. The client connects to the server to access this news.

2023-2024

A5, NE352, Sec1, Raghad Ahmed202202365 - Noora Sami202203065

Table of Contents: 
-Requirment.
-How to.
-The scripts.
-Additional concept.
-Acknowledgments.
-Conclusion.

Requirment: We installed Python and ran pip install requests socket threading json to get the needed libraries.
I signed up with my personal email at [NewsAPI.org] for an API key and they gave me(c23b132ee7ae4d1aad0ef2a8924af422).
In VS Code,We created a 2 folder(server.py) and (client.py). Then, We opened the terminal,We write first git add . / git commit -m "project" / git push

How to run the system:The client connects to the server, showing a menu to search news or sources, filter results, and view details. 
Follow the prompts to input choices, and the server will display the data. Select "Quit" to exit.

The scripts: The client-server scripts implement a Python socket system where the server uses multithreading to handle multiple clients.
It processes requests (options 1, 2, 3) and responds with data or errors. The client connects, sends a username, interacts through a menu, and exchanges data.
These scripts demonstrate socket programming, multithreading, and JSON handling in Python.

Additional concept:I added a feature that allows users to search for news by keyword. In the client code, I updated the `search_by_keyword` function to ask for a keyword and send it to the server. The server then uses this keyword in the API request to fetch relevant news. This makes the search more focused on specific topics.

Acknowledgments:We would like to extend our heartfelt thanks to Dr. Mohammed Almeer for his immense contributions to our project. His valuable knowledge, guidance, and unwavering support have been instrumental in our success, and we are truly grateful for his generosity in sharing his expertise with us.

Conclusion: This project involved creating a multithreaded news client/server system, enhancing our understanding of client-server architecture, network communication, and Python API integration.
We developed a server that manages multiple connections and a user-friendly client interface, gaining valuable coding experience and teamwork skills. Overall,
this project provided practical insights and a strong foundation in network programming for future challenges.
