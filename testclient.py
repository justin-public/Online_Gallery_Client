from socket import *
import sys
import time

HOST = '127.0.0.1'
PORT = 10000
BUFSIZE = 1024
ADDR = (HOST, PORT)

while True:
    clientSocket = socket(AF_INET, SOCK_STREAM)
    try:
        clientSocket.connect(ADDR)
        print('Connected to server')

        while True:
            try:
                # Send data to the server
                clientSocket.send('Hello!'.encode())
                print('Message sent')
                # Wait for a while before sending the next message
                time.sleep(5)  # Adjust the interval as needed
            except Exception as e:
                print('Error sending message:', e)
                break  # Exit inner loop on error

    except Exception as e:
        print('Connection failed:', e)
        time.sleep(1)  # Wait before trying to reconnect

    finally:
        clientSocket.close()
        print('Connection closed\n')
