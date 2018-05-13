# !/usr/bin/env python

import socket
import pickle
import json
from pip._vendor.distlib.compat import raw_input

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response
END = "$END$"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print ('Connection address:', addr)
data = ""
while data != END:
    print("enter a message to send to client")
    MESSEGE = raw_input()
    conn.send(MESSEGE.encode('utf-8'))
    if data == END: break
    data = conn.recv(BUFFER_SIZE)
    if not data: break
    # v = json.loads(data)
    # v = pickle.loads(data)

    v = pickle.load(open(data.decode(), 'rb'))
    print("recived data")
    print(v)

conn.close()