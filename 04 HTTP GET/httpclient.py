#! /usr/bin/env python3

"""
Paul Cruz
psc28
CS 356-001
"""

import sys
import time
import socket
import os


# Get the server hostname, port and hostname as command line arguments
commandLineArgument = f'{sys.argv[1]}'
CACHE_FILE = "cache.txt"
# Convert Command line arguments to useful information
url, filename = commandLineArgument.split("/")
url, url_port = url.split(':')
url_port = int(url_port)

# Create TCP client socket. Note the use of SOCK_STREAM for TCP packet
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Create TCP connection to server
clientSocket.connect((url, url_port))


GETData = f'''\n
            GET /{filename} HTTP/1.1.\r\n
            {url}:{str(url_port)}\r\n
            \r\n'''

if os.path.exists(CACHE_FILE) and os.path.exists(os.path.join(os.path.curdir, filename)):
    last_change = os.path.getmtime(CACHE_FILE)
    last_time = time.gmtime(last_change)
    IF_MODIFIED_SINCE = time.strftime("%a, %d %b %Y %H:%M:%S GMT\r\n", last_time)
    GETData += f'If-Modified-Since: {IF_MODIFIED_SINCE} \r\n' \
               f'\r\n'

    clientSocket.sendall(GETData.encode())


clientSocket.sendall(GETData.encode())

# Receive the server response
dataEcho = clientSocket.recv(1024)
# Display the decoded server response as an output
dataEcho = dataEcho.decode()

if "HTTP/1.1 404" in dataEcho:
    print(f'File does not exist {filename}')
    clientSocket.close()
    exit()
    
elif ""
# Close the client socket
clientSocket.close()

