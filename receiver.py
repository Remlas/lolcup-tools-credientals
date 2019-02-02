import socket
import json

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# get local machine name
host = "192.168.1.10"

port = 25565

# connection to hostname on the port.
s.connect((host, port))                               

# Receive no more than 1024 bytes

msg = s.recv(1024)                                     
print (msg.decode('utf-8'))

s.close()

data = json.loads(msg.decode('utf-8'))

print(data['Port'])
print(data['Password'])