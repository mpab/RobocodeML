#!/usr/bin/env python3

import socket
import json

import parser
#import features

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

    p = parser.JsonParser();

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
        js = p.scan(text)

        if js is not None:
            jsn = json.loads(js)
            print(json.dumps(jsn))

    conn.close()


while True:
    conn = connect()
    process_messages(conn)
