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

# Get the server hostname, port and data length as command line arguments
host = sys.argv[1]
port = int(sys.argv[2])
pings, count, max_sec, min_sec, avg, timeout = 10, 0, -1, 1, 0, 0

# Create UDP client socket. Note the use of SOCK_DGRAM
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientsocket.settimeout(1)  # 1 Second timeout

print(f"Pinging {host}, {port}:")
for i in range(pings):

    t1 = time.time()  # Get Current time
    count += 1
    data = struct.pack('!ii', 1, count)

    try:
        # Send data to server
        clientsocket.sendto(data, (host, port))
        # Receive the server response
        dataEcho, address = clientsocket.recvfrom(100)
        dataEcho = struct.unpack('!ii', dataEcho)
        t2 = time.time()
        print(f"Ping Message number {count}, RTT: {t2 - t1:.10f} sec")
        avg += t2 - t1

        if t2 - t1 > max_sec:
            max_sec = t2 - t1
        elif t2 - t1 < min_sec:
            min_sec = t2 - t1

    except socket.timeout:
        print(f'Ping message number {count} timed out')
        timeout += 1

print(f'\nStatistics: \n'
      f'{count} packets transmitted, {count - timeout} Received, {(timeout / count) * 100}% packet loss\n'
      f'Min/Max/Avg RTT = {min_sec:.10f} / {max_sec:.10f} / {avg / (count - timeout):.10f} sec')

# Close the client socket
clientsocket.close()
