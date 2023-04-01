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
price_data = pd.read_excel('books_cost.xlsx')

def suggest_books(area, min_mil, max_mil, lvl_diff):
    filtered_books = books_data[(books_data['Area'].str.lower() == area.lower()) & 
                                (books_data['Distance'].astype(int) >= min_mil) & 
                                (books_data['Distance'].astype(int) <= max_mil) &
                                (books_data['Difficult'].str.lower() == lvl_diff.lower())]
    
    return filtered_books
def purchase(title, quantity):
  
    # Filter and get the price of the book
    book = price_data[(price_data['Books'].str.lower() == title.lower())]

    # Generate the invoice
    price_per_book = book['Price'].values[0]
    total_price = quantity * price_per_book

    #applying 10% discount if total is more than 75
    if total_price > 75:
        discount = total_price * 0.1
        total_price = total_price - discount
        invoice = f"You got a 10% discount!\nBook Title: {title}\nQuantity: {quantity}\nPrice per book: {price_per_book}\nTotal price after discount: {total_price}"
    else:
        invoice = f"Book Title: {title}\nQuantity: {quantity}\nPrice per book: {price_per_book}\nTotal price: {total_price}"
    return invoice


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
        print ("\nWaiting to receive message from client")
        client, address = sock.accept() 
        data = client.recv(data_payload)
        print("\nMessage Received form client: ",data)

        if data:
            # Split the client input into category and author
            input_data = data.decode().split(',')
            area = input_data[0]
            min_mil = int(input_data[1])
            max_mil = int(input_data[2])
            lvl_diff = input_data[3]

            # Call the suggest_books function to get book suggestions
            book_suggestions = suggest_books(area,min_mil,max_mil,lvl_diff)

            if book_suggestions.empty:
                book_suggestions_str = "No books found for the given input"
                client.send(bytes(book_suggestions_str, 'utf-8'))
            else:
                book_suggestions_str = book_suggestions.to_string(index=False)
                client.send(bytes(book_suggestions_str, 'utf-8'))
                #print ("sent %d bytes back to %s" % (len(book_suggestions), address))
            
            books_to_buy = client.recv(data_payload)
            print("\nRequest for Purchase obtained from the client: ", books_to_buy)

            if books_to_buy:
                # Split the purchase request into title and quantity
                title_quantity = books_to_buy.decode().split(',')
                title = title_quantity[0]
                quantity = int(title_quantity[1])

                # Call the purchase function to generate the invoice
                invoice = purchase(title, quantity)
                client.send(bytes(invoice, 'utf-8'))
        # End connection
        client.close() 

 

if __name__ == '__main__':
    #given_args = parser.parse_args() 
    port =9900
    echo_server(9900)
  

