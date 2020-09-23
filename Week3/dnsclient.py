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

'''
2 Bytes Variables
'''
# Default Values
message_type = 1
return_code = 0
answer_length = 0
message_length = sys.getsizeof(hostname)

'''
4 Bytes Variables
'''
message_id = random.randint(1, 100)     # returns a number between 1 and 100 (both included)


error_codes = {
    0: "No Errors",
    1: "Name not Found",
}


def request_output():
    print(f'Sending Request to {host}, {port}: '
          f'Message ID: {message_id}'
          f'Question Length: {message_length}'
          f'Answer Length: {answer_length}'
          f'Question: {hostname}\n')


def response_output(output_data, host):
    message_type, return_code, message_id, message_length, answer_length, question, \
    answer = struct.unpack('!hhihhss', output_data)
    print(f'Received Response from: {host}, {port}'
          f'Return Code: {return_code} ({error_codes[return_code]})'
          f'Message ID: {message_id}'
          f'Question Length: {message_length}'
          f'Answer Length: {answer_length}'
          f'Question: {question.decode()}'
          f'Answer: {answer.decode()}')


# Create UDP client socket. Note the use of SOCK_DGRAM
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientsocket.settimeout(1)  # 1 Second timeout
data = struct.pack('!hhhhis', message_type, return_code, answer_length, message_length, message_id, hostname.encode())


try:
    request_output()
    # Send data to server
    clientsocket.sendto(data, (host, port))
    # Receive the server response
    dataEcho, address = clientsocket.recvfrom(1024)
    response_output(dataEcho, address)

except socket.timeout:
    pass


# print(f'\nStatistics: \n'
#       f'{count} packets transmitted, {count - timeout} Received, {(timeout / count) * 100}% packet loss\n'
#       f'Min/Max/Avg RTT = {min_sec:.10f} / {max_sec:.10f} / {avg / (count - timeout):.10f} sec')

# Close the client socket
clientsocket.close()
