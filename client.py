#!/usr/bin/env python 
# Source Python Network Programming Cookbook,Second Edition -- Chapter - 1 

 
import socket 
import sys 
 
import argparse 
 
host = '127.0.0.1'
 
def echo_client(port): 
    """ A simple echo client """ 
    # Create a TCP/IP socket 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    # Connect the socket to the server 
    #server_address = ('127.0.0.1', 9900)
    print("--------------------")
    #print ("Connecting to %s port %s" % server_address) 
    #sock.connect(server_address)
    sock.connect((host, port))
     
    # Send data 
    try: 
        # Send data
        area= input('Enter the area you want to walk: ')
        min_mil = input('Enter the minimum milage you want to walk: ')
        max_mil = input('Enter the maximum milage you want to walk: ')
        lvl_diff = input('Enter the level of difficulty you want to walk: ')

        message = area + ',' + min_mil + ',' + max_mil + ',' + lvl_diff
        print ("Sending to Server: %s :" % message) 
        sock.sendall(message.encode('utf-8')) 
        # Look for the response 
        data = sock.recv(1024) 
        print ("Received from Server:\n", data.decode("utf-8"))

        q_to_buy = input('Do you want to buy any of the books? (y/n): ')

        if q_to_buy == 'y':
            book_title = input('Enter the name of the book you want to buy: ')
            book_quantity = int(input('Enter the quantity: '))

            # Send purchase request to the server
            request = f"{book_title},{book_quantity}"
            sock.sendall(request.encode('utf-8'))
            # Receive invoice from the server
            invoice_data = sock.recv(1024)
            print ("Received bill from the Server:\n", invoice_data.decode("utf-8"))

            confirm = input('confirm the purchase? (y/n): ')
            if confirm == 'y':
                print("Thank you for your purchase and have a nice day :)")
                '''
                sock.sendall('y'.encode('utf-8'))
                # Receive confirmation from the server
                confirmation = sock.recv(1024)
                print ("Received confirmation from Server:\n", confirmation.decode("utf-8"))
                '''
            else:
                print("Thanks for visiting our store")
        else:
            print("Thanks for visiting our store")
    except socket.error as e: 
        print ("Socket error: %s" %str(e)) 
    except Exception as e: 
        print ("Other exception: %s" %str(e)) 
    finally: 
        print ("\nClosing connection to the server") 
        sock.close() 
     
if __name__ == '__main__': 
    port = 9900 
    while True:
        echo_client(port) 

