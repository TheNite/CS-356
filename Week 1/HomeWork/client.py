#! /usr/bin/env python3

'''
Paul Cruz
psc28
CS 356-001
'''

import sys
import socket

# Get the server hostname, port and data length as command line arguments
host = sys.argv[1]
port = int(sys.argv[2])
count = int(sys.argv[3])
data = 'X' * count  # Initialize data to be sent
max_tries = 3

# Create UDP client socket. Note the use of SOCK_DGRAM
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientsocket.settimeout(1)  # 1 Second timeout

while True:

    if max_tries == 0:
        break

    # Send data to server
    # Literal String Interpolation - https://www.python.org/dev/peps/pep-0498/
    print(f"Sending data to {host}, {port} : {data} ({len(data)} characters)")
    clientsocket.sendto(data.encode(), (host, port))

    try:
        # Receive the server response
        dataEcho, address = clientsocket.recvfrom(count)
        # print(dataEcho, address)
        print(f"Receive data from {address[0]}, {address[1]}: {dataEcho.decode()}")
        break
    except socket.timeout:
        print('Message timed out')
        max_tries -= 1

#Close the client socket
clientsocket.close()
