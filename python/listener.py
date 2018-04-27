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

class MsgExtractor:
    def __init__(self):
        self.buff = ""
        self.msg = ""

    def scan(self, inBuff):

        self.buff = self.buff + inBuff

        out = ""

        found_start = False
        found_end = False

        for idx in range(len(self.buff)):

            char = self.buff[idx]

            if char == '{':
                found_start = True
                out = out + char
                continue

            if char == '}':
                found_end = True
                end_idx = idx
                out = out + char
                break

            out = out + char

        if found_start and found_end:
            self.buff = self.buff[end_idx + 1:]
            return out

        return None

def process_messages(conn):

    extractor = MsgExtractor();

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
        json = extractor.scan(text)

        if json is not None:
            print(json)

    conn.close()


while True:
    conn = connect()
    process_messages(conn)