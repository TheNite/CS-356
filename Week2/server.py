#! /usr/bin/env python3

'''
Paul Cruz
psc28
CS 356-001
'''

import sys
import socket
import struct
import random


# Read server IP address and port from command-line arguments
serverIP = sys.argv[1]
serverPort = int(sys.argv[2])

# Create a UDP socket. Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Assign server IP address and port number to socket
serverSocket.bind((serverIP, serverPort))

print("The server is ready to receive on port:  " + str(serverPort) + "\n")

# loop forever listening for incoming UDP messages
while True:
    data, address = serverSocket.recvfrom(100)
    choice = random.randint(1, 10)
    # Receive and print the client data from "data" socket
    print(choice)
    if choice > 4:
        data = struct.unpack('!i', data)[0]
        print("Receive data from client " + address[0] + ", " + str(address[1]) + ": " + str(data))

        data = struct.pack('!i', 2)
        # Echo back to client
        print("Sending data to   client " + address[0] + ", " + str(address[1]) + ": " + str(data))
        serverSocket.sendto(data, address)
    else:
        print('Send no response')
