#!/usr/bin/env python3

import socket               

def connect():
    soc = socket.socket()         
    host = "localhost" 
    port = 8888                
    soc.bind((host, port))      
    soc.listen(5)                 
    print("listening on port: {}".format(port))
    conn, addr = soc.accept()     
    print("accepted connection from: ", addr)
    return conn

def process_messages(conn):
    connected = True

    while connected:
        try:
            msg = conn.recv(1024)  
        except socket.error as e:
            if e.errno == errno.ECONNRESET:
                print("connection reset")
            else:
                print("connection error")
            connected = False
            continue


        if msg is None:
            print("nil message")
            connected = False
            continue

        if len(msg) == 0:
            print("empty message")
            connected = False
            continue

        text = msg.decode('utf-8')
            
        if text == 'CLOSE_CONNECTION':
            connected = False
            continue

        print(text)

    conn.close()


while True:
    conn = connect()
    process_messages(conn)