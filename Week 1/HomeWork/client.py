#! /usr/bin/env python3
# Echo Client
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
    print("Sending data to   " + host + ", " + str(port) + ": " + data)
    clientsocket.sendto(data.encode(), (host, port))

    try:
        # Receive the server response
        dataEcho, address = clientsocket.recvfrom(count)
        print(dataEcho, address)
        print("Receive data from " + address[0] + ", " + str(address[1]) + ": " + dataEcho.decode())
        break
    except socket.timeout:
        print(f'Message timed out')
        max_tries -= 1

#Close the client socket
clientsocket.close()
