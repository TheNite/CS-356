#! /usr/bin/env python3

"""
Paul Cruz
psc28
CS 356-001
"""

import sys
import socket
import struct

# dns-master-file
dns_records = 'dns-master.txt'

# Read server IP address and port from command-line arguments
serverIP = sys.argv[1]
serverPort = int(sys.argv[2])

# Create a UDP socket. Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Assign server IP address and port number to socket
serverSocket.bind((serverIP, serverPort))

print(f"The server is ready to receive on port: {serverPort}\n")

# loop forever listening for incoming UDP messages
while True:
    data, address = serverSocket.recvfrom(1024)
    message_type, return_code, answer_length, message_length, message_id, hostname \
        = struct.unpack('!hhhhis', data)


    # Echo back to client
    # print("Sending data to   client " + address[0] + ", " + str(address[1]) + ": " + str(data))
    #serverSocket.sendto(data, address)
