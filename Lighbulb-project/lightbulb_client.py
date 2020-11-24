import sys
import socket
import struct
import random

host = sys.argv[1]
port = int(sys.argv[2])
action = int(sys.argv[3])

max_tries = 3  # Max amount of tries program will try before exiting

'''
2 Bytes Variables
'''

message_type = 1
return_code = 0

'''
4 Bytes Variables
'''
message_id = random.randint(1, 100)  # returns a number between 1 and 100 (both included)

'''
Network Socket UDP
'''
# Create UDP client socket. Note the use of SOCK_DGRAM
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientsocket.settimeout(1)  # 1 Second timeout

data_action = None

error_codes = {
    0: "No Errors",
    1: "Error!"
}


def response_output(output_data, server_address):
    # noinspection SpellCheckingInspection
    server_message_type, server_return_code, server_message_id, response = struct.unpack('!hhih', output_data)
    print(f'\nReceived Response from: {server_address[0]}, {server_address[1]}'
          f'\nReturn Code: {server_return_code} ({error_codes[server_return_code]})'
          f'\nMessage ID: {server_message_id}')


if action == 2 or action == 1:
    print('Please input color rgb % you would like to change:')
    red = float(input("Red %: "))
    green = float(input('Green %: '))
    blue = float(input('Blue %: '))
    data_action = (red, green, blue)
elif action == 3:
    brightness = float(input("Change light bulb brightness %: "))
    data_action = brightness

data = struct.pack(f'!hhihf', message_type, return_code, message_id, action, data_action)


while True:

    if max_tries == 0:
        print('Request timed out... Exiting Program')
        break

    print(f'\nSending Request to {host}, {port}: '
          f'\nMessage ID: {message_id}'
          f'\nAction: {action}')

    if action == 1:
        print(f'\nColor set: {data_action}')
    elif action == 2:
        print(f'\nRGB Colors %: {str(data_action)}')
    elif action == 3:
        print(f'\nBrightness %: {str(data_action)}')

    try:
        # Send data to server
        clientsocket.sendto(data, (host, port))
        # Receive the server response
        dataEcho, address = clientsocket.recvfrom(1024)
        response_output(dataEcho, address)
        break

    except socket.timeout:
        print('Request timed out....')
        print(f'Sending Request to {host}, {port}')
        max_tries -= 1

# Close the client socket
clientsocket.close()