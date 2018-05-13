#!/usr/bin/env python

import socket
import json
import pickle

import Doc2Vec

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024
END = "$END$"
# MESSAGE = "Hello, World!".encode()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

data = []
while(1):
    data.append(s.recv(BUFFER_SIZE).decode())
    print("received data:", data)
    if data[-1] == END: break

    print("calculating vector from Doc2Vec...")
    v = Doc2Vec.create_doc_object(data)
    # v = Doc2Vec.sens2vec(data)

    print("sending vector to server....")
    # MESSAGE = json.dumps(v, ensure_ascii=False)

    pickle.dump(v, open('simple1.pkl', 'wb'))

    s.send('simple1.pkl'.encode())
    print("vector sent.")
s.close()


