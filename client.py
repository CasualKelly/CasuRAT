#!/usr/bin/python3

# Standard libraries only
import socket

#initialize remote host variables with user input
RHOST = str(input("C2 IP Address\n" ))
RPORT = int(input("C2 Port\n"))

#Create a socket object, connect to the server, and send a test message
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((RHOST, RPORT))
    s.sendall(b'Successful Test')
    data = s.recv(1024)

print('Test received', repr(data))