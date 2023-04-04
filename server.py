##importing pandas library
import pandas as pd                                                              
#importing socket library
import socket                                                                  
#importing sys library
import sys                                                                                                      
#host ip address
host = '127.0.0.1'                                                              
#port number
port = 9879                                                                     
#data payload
data_payload = 2048                                                                 
#backlog                                          
backlog = 5                                                                       
#reading the excel file containing the books data
books_data = pd.read_excel('circular_walks.xlsx')                               
#reading the excel file containing the price data 
price_data = pd.read_excel('books_cost.xlsx')                                               
#function to suggest books based on the user input
def suggest_books(area, min_mil, max_mil, lvl_diff):                            
    #filtering the books based on the user input  
    filtered_books = books_data[                                                
        #converting the user input to lower case and comparing with the input              
        (books_data['Area'].str.lower() == area.lower()) &                      
        #converting the distance to integer and comparing with the min input        
        (books_data['Distance'].astype(int) >= min_mil) &                       
        #converting the distance to integer and comparing with the max input
        (books_data['Distance'].astype(int) <= max_mil) &                       
        #converting the user input to lower case and comparing with the input
        (books_data['Difficult'].str.lower() == lvl_diff.lower())]              
     #returning the filtered books
    return filtered_books                                                      
 #function to generate the invoice
def purchase(title, quantity):                                                 
  #filtering the price data based on the user input
    book = price_data[(price_data['Books'].str.lower() == title.lower())]       
    #if no book is found 
    if book.empty:                                                               
        #error message - no books found                            
        invoice = f"No books found for the given input"                         
        #returning the error message                     
        return invoice  
        

    else:#getting the price of the book

        #additional feature - prevent illegal inputs for quantity  
        # if the user enters the quantity less than 1
        if quantity < 1:
        # the quantity will be set to 1
            quantity = 1
        # if the user enters the quantity between 1 and 10
        elif quantity > 10:
        # the quantity will be set to 10
            quantity = 10

        #getting the price of the book    
        price_per_book = book['Price'].values[0]                                
        #calculating the total price   
        total_price = quantity * price_per_book                                           
        #if the total price is greater than 75 applying 10% discount
        if total_price > 75:                                                    
            #calculating the discount
            discount = total_price * 0.1                                        
            #calculating the total price after discount
            total_price = total_price - discount                                
            #generating the invoice message with discount                                                                                
            invoice = f"You got a 10% discount!\nBook Title: {title}\nQuantity: {quantity}\nPrice per book: {price_per_book}\nTotal price after discount: {total_price}"
        else:
            #generating the invoice message without discount
            invoice = f"Book Title: {title}\nQuantity: {quantity}\nPrice per book: {price_per_book}\nTotal price: {total_price}"
        return invoice  

#function to create the server from the given code
def echo_server(port):                                                          
    #creating the socket       
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                    
    #setting the socket options          
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)                  
    #binding the host and port
    sock.bind((host, port))                                                     
    #listening to the backlog
    sock.listen(backlog)                                                                                   
    while True: #waiting to receive message from client
        print ("\nWaiting to receive message from client")                       
        #accepting the client 
        client, address = sock.accept()                                          
        #receiving the data from the client             
        data = client.recv(data_payload)                                        
        #printing the message received from the client                     
        print("\nMessage Received form client: ",data)                                      
        #if data is received
        if data:                                                                 
            #split the client input into category and author                                 
            input_data = data.decode().split(',')                               
            #getting the area from the input 
            area = input_data[0]                                                
            #getting the min distance from the input                       
            min_mil = int(input_data[1])                                        
            #getting the max distance from the input            
            max_mil = int(input_data[2])                                        
            #getting the level of difficulty from the input  
            lvl_diff = input_data[3]                                            
            #call the suggest_books function to get book suggestions
            book_suggestions = suggest_books(area,min_mil,max_mil,lvl_diff)     
            #if no books are found
            if book_suggestions.empty:                                          
                #error message - no books found                    
                book_suggestions_str = "No books found for the given input"     
                #sending the error message to the client
                client.send(bytes(book_suggestions_str, 'utf-8'))               
            else:#converting the book suggestions to string
                book_suggestions_str = book_suggestions.to_string(index=False)  
                #sending the book suggestions to the client
                client.send(bytes(book_suggestions_str, 'utf-8'))               
            #receive the purchase request from the client
            books_to_buy = client.recv(data_payload)                            
            #printing the purchase request from the client
                                                                                
            print("\nRequest for Purchase obtained from the client: ", books_to_buy) 
            #if purchase request is received 
            if books_to_buy:                                                    
                #Split the purchase request into title and quantity       
                title_quantity = books_to_buy.decode().split(',')               
                #getting the title from the purchase request
                title = title_quantity[0]                                       
                #getting the quantity from the purchase request 
                quantity = int(title_quantity[1])                               
                #call the purchase function to generate the invoice      
                invoice = purchase(title, quantity)
                #sending the invoice to the client
                client.send(bytes(invoice, 'utf-8'))                            
        #end connection
        client.close()

#main function
if __name__ == '__main__':                                                    
    #port number
    port =9900                                                                 
    #calling the echo server function
    echo_server(9900)                                                          
    
  

