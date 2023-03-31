    #!/usr/bin/env python
    # Python Network Programming Cookbook,Second Edition -- Chapter - 1
    
import pandas as pd
import socket
import sys
    
host = '127.0.0.1'
port = 9879
data_payload = 2048
backlog = 5

books_data = pd.read_excel('circular_walks.xlsx')

def suggest_books(area, min_mil, max_mil, lvl_diff):
    
    filtered_books = books_data[(books_data['Area'].str.lower() == area.lower()) & 
                                (books_data['Distance'].astype(int) >= min_mil) & 
                                (books_data['Distance'].astype(int) <= max_mil) &
                                (books_data['Difficult'].str.lower() == lvl_diff.lower())]

    return filtered_books

def echo_server(port):
    """ A simple echo server """
    # Create a TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Enable reuse address/port 
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Bind the socket to the port
    sock.bind((host, port))
    # Listen to clients, backlog argument specifies the max no. of queued connections
    sock.listen(backlog) 
    while True: 
        print ("Waiting to receive message from client")
        client, address = sock.accept() 
        data = client.recv(data_payload)
        print("Message Received form client: ",data)

        if data:
            # Split the client input into category and author
            input_data = data.decode().split(',')
            area = input_data[0]
            min_mil = int(input_data[1])
            max_mil = int(input_data[2])
            lvl_diff = input_data[3]

            # Call the suggest_books function to get book suggestions
            book_suggestions = suggest_books(area,min_mil,max_mil,lvl_diff)
            # Send book suggestions back to client
            #book_suggestions_js = book_suggestions.to_json(orient='records')
           
            #client.send(bytes(book_suggestions_js, 'utf-8'))

            book_suggestions_str = book_suggestions.to_string(index=False)
            client.send(bytes(book_suggestions_str, 'utf-8'))
            #client.send(book_suggestions_str.encode())
            print ("Data to Send to Client: \n%s " % book_suggestions_str)
            #print ("sent %d bytes back to %s" % (len(book_suggestions), address))
            
        # End connection
        client.close() 

 

if __name__ == '__main__':
    #given_args = parser.parse_args() 
    port =9900
    echo_server(9900)
  

