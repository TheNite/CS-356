#! /usr/bin/env python3

'''
Paul Cruz
psc28
CS 356-001
'''

import sys
import socket
import struct
import time
import random

# Get the server hostname, port and hostname as command line arguments
host = sys.argv[1]
port = int(sys.argv[2])
hostname = sys.argv[3]

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


pings, count, max_sec, min_sec, avg, timeout = 10, 0, -1, 1, 0, 0


# Create UDP client socket. Note the use of SOCK_DGRAM
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientsocket.settimeout(1)  # 1 Second timeout

print(f"Pinging {host}, {port}:")
data = struct.pack('!hhhhis', message_type, return_code, answer_length, message_length, message_id, hostname.encode())


def output(output_data):
    output_data = struct.unpack('!hhhis', output_data)
    print(f'Sending Request to {host}, {port}: '
          f'Message ID: {message_id}'
          f'Question Length: {message_length}'
          f'Answer Length: {answer_length}'
          f'Question: {hostname}\n'
          f'Received Response from: '
          f'Return Code: '
          f'Message ID: '
          f'Question Length: '
          f'Answer Length: '
          f'Question: '
          f'Answer: ')

try:
    # Send data to server
    clientsocket.sendto(data, (host, port))
    # Receive the server response
    dataEcho, address = clientsocket.recvfrom(1024)
    # dataEcho = struct.unpack('!hh', dataEcho)
    t2 = time.time()
    print(f"Ping Message number {count}, RTT: sec")

except socket.timeout:
    print(f'Ping message number {count} timed out')
    timeout += 1

# print(f'\nStatistics: \n'
#       f'{count} packets transmitted, {count - timeout} Received, {(timeout / count) * 100}% packet loss\n'
#       f'Min/Max/Avg RTT = {min_sec:.10f} / {max_sec:.10f} / {avg / (count - timeout):.10f} sec')

# Close the client socket
clientsocket.close()
