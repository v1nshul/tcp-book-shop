#importing the socket library
import socket                              
#importing the sys library                                      
import sys 
#importing the argparse library
import argparse 

#defining the host
host = '127.0.0.1'
 
#additional feature 2 - prevent potential illegal purchases
#setting up a counter for the number of purchases
purchase_count = 0
#ask the user if they want to buy any of the books

#function to create the client
def echo_client(port): 
    # Create a TCP/IP socket 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    print("--------------------")
    sock.connect((host, port))


    # Send data 
    try: 
        #ask the user to enter the area, min miles, max miles and level of difficulty
        area= input('Enter the area you want to walk: ')
        min_mil = input('Enter the minimum miles you want to walk: ')
        max_mil = input('Enter the maximum miles you want to walk: ')
        lvl_diff = input('Enter the level of difficulty you want to walk: ')

        #sending the user input to the server
        message = area + ',' + min_mil + ',' + max_mil + ',' + lvl_diff
        print ("Sending to Server: %s :" % message) 
        sock.sendall(message.encode('utf-8')) 
        #look for the response 
        data = sock.recv(1024) 
        print ("Received from Server:\n", data.decode("utf-8"))


        #ask the user if they want to buy any of the books
        q_to_buy = input('Do you want to buy any of the books? (y/n): ')

        #if the user wants to buy a book
        if q_to_buy == 'y':
            book_title = input('Enter the name of the book you want to buy: ')
            book_quantity = int(input('Enter the quantity: '))

            #Send purchase request to the server
            request = f"{book_title},{book_quantity}"
            sock.sendall(request.encode('utf-8'))
            #Receive invoice from the server
            invoice_data = sock.recv(1024)
            print ("Received bill from the Server:\n", invoice_data.decode("utf-8"))

            #check if the book is available
            if invoice_data.decode("utf-8") == "No books found for the given input":
                #thank the user for visiting the store
                print("Thanks for visiting our store")
                return
            else:
                #ask the user to confirm the purchase
                confirm = input('confirm the purchase? (y/n): ')
                #if the user confirms the purchase
                if confirm == 'y':
                    #thank the user for the purchase
                    print("Thank you for your purchase and have a nice day :)")
                    
                    #check if the user has exceeded the maximum number of purchases
                    
                else:
                    #thank the user for visiting the store
                    print("Thanks for visiting our store")
                    print ("\nClosing connection to the server")
                    sock.close()
        else:
            print("Thanks for visiting our store")
            print ("\nClosing connection to the server")
            sock.close()
        
    #exceptions
    except socket.error as e: 
        print ("Socket error: %s" %str(e)) 
    except Exception as e: 
        print ("Other exception: %s" %str(e)) 
    finally: 
        print ("\nClosing connection to the server") 
        sock.close() 

#main function
if __name__ == '__main__': 
    #setting the port number
    port = 9900 
    #calling the client function

    while True and purchase_count < 1:   
        #close the connection
        echo_client(port)
        purchase_count += 1 
        if purchase_count > 1:
            print("You have exceeded the maximum number of purchases")
            print ("\nClosing connection to the server")

