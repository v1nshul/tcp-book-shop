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
        area= input('Enter the area you want to walk:')
        min_mil = input('Enter the minimum milage you want to walk:')
        max_mil = input('Enter the maximum milage you want to walk:')
        lvl_diff = input('Enter the level of difficulty you want to walk:')

        message = area + ',' + min_mil + ',' + max_mil + ',' + lvl_diff
        print ("Sending to Server: %s :" % message) 
        sock.sendall(message.encode('utf-8')) 
        # Look for the response 
        amount_received = 0 
        amount_expected = len(message) 
        #while amount_received < amount_expected: 
         #   data = sock.recv(1024) 
          #  amount_received += len(data) 
           # print ("Received from Server:", data.decode("utf-8"))
    except socket.error as e: 
        print ("Socket error: %s" %str(e)) 
    except Exception as e: 
        print ("Other exception: %s" %str(e)) 
    finally: 
        print ("Closing connection to the server") 
        sock.close() 
     
if __name__ == '__main__': 
    port = 9900 
    while True:
        echo_client(port) 

