#! /usr/bin/env python3

'''
Paul Cruz
psc28
CS 356-001
'''

import sys
import socket
import struct

# Get the server hostname, port and data length as command line arguments
host = sys.argv[1]
port = int(sys.argv[2])
data = struct.pack('!i', 1)
max_tries = 10

# Create UDP client socket. Note the use of SOCK_DGRAM
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientsocket.settimeout(1)  # 1 Second timeout

while True:

    if max_tries == 0:
        break

    # Send data to server
    # Literal String Interpolation - https://www.python.org/dev/peps/pep-0498/
    print(f"Sending data to {host}, {port} : {data}")
    clientsocket.sendto(data, (host, port))

    try:
        # Receive the server response
        dataEcho, address = clientsocket.recvfrom(100)
        dataEcho = struct.unpack('!i', dataEcho)
        if dataEcho[0] == 2:
            print('here')
        # print(dataEcho, address)
        print(f"Receive data from {address[0]}, {address[1]}: {dataEcho[0]}")
        max_tries -= 1
        break
    except socket.timeout:
        print('Message timed out')
        max_tries -= 1

#Close the client socket
clientsocket.close()
