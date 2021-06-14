#!/usr/bin/env python
import socket
import threading

IP = "192.168.1.4" # change this to your ip address
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((IP, 8080))
s.listen(10)

participants = dict()

def worker(conn):
    """This is the worker. When a single connection comes in. This is what will handle that"""
    name = conn.recv(100)
    name = name.decode("ascii").strip()
    participants[name] = conn
    print (f"{name} is on chat!")
    conn.send(f"Hello {name}. Type quit and hit enter to leave the chat. Anything else will be sent to all the users.\n".encode("ascii"))
    while True:
        # This is the a loop that will run till the remote client types "quit"
        data = conn.recv(100).decode("ascii").strip()
        if data == "quit":
            conn.send(b"Goodbye!\n")
            conn.close()
            del participants[name]
            break
        for k,v in participants.items():
            v.send(f"{name}: {data}\n".encode("ascii"))
        
while True:
    print ("Waiting for connection")
    conn, addr = s.accept()
    print (f"Received connection from {addr}")
    t = threading.Thread(target =worker, args=(conn,))
    t.start()
    
    





