#! /usr/bin/env python3

"""
Paul Cruz
psc28
CS 356-001
"""

import sys
import socket
import struct
import random

# Get the server hostname, port and hostname as command line arguments
host = sys.argv[1]
port = int(sys.argv[2])
hostname = f'{sys.argv[3]} A IN'
max_tries = 3   # Max amount of tries program will try before exiting

'''
2 Bytes Variables
'''
message_type = 1
return_code = 0
answer_length = 0
message_length = sys.getsizeof(hostname)

'''
4 Bytes Variables
'''
message_id = random.randint(1, 100)     # returns a number between 1 and 100 (both included)

'''
Network Socket UDP
'''
# Create UDP client socket. Note the use of SOCK_DGRAM
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientsocket.settimeout(1)  # 1 Second timeout

# noinspection SpellCheckingInspection
data = struct.pack(f'!hhhhi{message_length}s', message_type, return_code, answer_length, message_length,
                   message_id, hostname.encode())


error_codes = {
    0: "No Errors",
    1: "Name not found"
}


def request_output():
    print(f'\nSending Request to {host}, {port}: '
          f'\nMessage ID: {message_id}'
          f'\nQuestion Length: {message_length}'
          f'\nAnswer Length: {answer_length}'
          f'\nQuestion: {hostname}')


def response_output(output_data, server_address):
    # noinspection SpellCheckingInspection
    server_message_type, server_return_code, server_message_id, server_message_length, \
        server_answer_length = struct.unpack('!hhihh', output_data[:12])

    print(f'\nReceived Response from: {server_address[0]}, {server_address[1]}'
          f'\nReturn Code: {server_return_code} ({error_codes[server_return_code]})'
          f'\nMessage ID: {server_message_id}'
          f'\nQuestion Length: {message_length}'
          f'\nAnswer Length: {server_answer_length}')

    server_question = struct.unpack_from(f'!{message_length}s', output_data[12:])
    print(f'Question: {server_question[0].decode()}')

    if server_return_code == 0:
        server_answer = struct.unpack_from(f'!{server_answer_length}s', output_data[message_length:])
        print(f'Answer: {server_answer[0].decode()}')


while True:

    if max_tries == 0:
        print('Request timed out... Exiting Program')
        break

    try:
        # Send data to server
        clientsocket.sendto(data, (host, port))
        # Receive the server response
        dataEcho, address = clientsocket.recvfrom(1024)

        request_output()
        response_output(dataEcho, address)
        break

    except socket.timeout:
        print('Request timed out....')
        print(f'Sending Request to {host}, {port}')
        max_tries -= 1

# Close the client socket
clientsocket.close()
