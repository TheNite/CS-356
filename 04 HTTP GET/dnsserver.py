#! /usr/bin/env python3

"""
Paul Cruz
psc28
CS 356-001
"""

import sys
import socket
import struct

# Read server IP address and port from command-line arguments
serverIP = sys.argv[1]
serverPort = int(sys.argv[2])

# Create a UDP socket. Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Assign server IP address and port number to socket
serverSocket.bind((serverIP, serverPort))

# dns-master-file
dns_records_file = 'dns-master.txt'

records = []
labels = ['dns', 'record', 'class', 'ttl', 'ip']
message_type = 2


def search_records(dns_records, hostname):
    for dns_host in dns_records:
        if hostname == dns_host['dns']:
            return True, f'{dns_host["dns"]} {dns_host["record"]} {dns_host["class"]} ' \
                         f'{dns_host["ttl"]} {dns_host["ip"]}'
    return False, None


with open(dns_records_file, 'r') as f:
    for line in f:
        if line.strip().startswith('#') or len(line) == 1 or len(line.split()) != 5:
            continue
        records.append(dict(zip(labels, line.strip().split())))


print(f"The server is ready to receive on port: {serverPort}\n")

# loop forever listening for incoming UDP messages
while True:
    data, address = serverSocket.recvfrom(1024)

    # noinspection SpellCheckingInspection
    client_message_type, client_return_code, client_answer_length, client_message_length, \
        client_message_id = struct.unpack(f'!hhhhi', data[:12])

    requested_hostname = struct.unpack_from(f'!{client_message_length}s', data[12:])
    requested_hostname = requested_hostname[0].decode()

    print(f'\nMessage Type: {client_message_type}'
          f'\nReturn Code: {client_return_code}'
          f'\nMessage ID: {client_message_id}'
          f'\nQuestion Length: {client_message_length}'
          f'\nAnswer Length: {client_answer_length}'
          f'\nQuestion: {requested_hostname}')

    result, data = search_records(records, requested_hostname.split()[0])

    if result:
        print('Found Match!\n')
        return_code = 0  # 2 Bytes
        answer_length = sys.getsizeof(data)
        # noinspection SpellCheckingInspection
        data = struct.pack(f'!hhihh{client_message_length}s{answer_length}s', message_type, return_code,
                           client_message_id, client_message_length, answer_length,
                           requested_hostname.encode(), data.encode())
    else:
        print('No Match Found!\n')
        return_code = 1  # 2 Bytes
        answer_length = 0
        # noinspection SpellCheckingInspection
        data = struct.pack(f'!hhihh{client_message_length}s', message_type, return_code,
                           client_message_id, client_message_length, answer_length,
                           requested_hostname.encode())

    serverSocket.sendto(data, address)
