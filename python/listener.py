#!/usr/bin/env python3

import socket
import errno
import util


def listen(conn):

    p = util.MsgParser();

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
            connected = False
            continue

        fragment = msg.decode('utf-8')
        text = p.scan(fragment)

        if text is not None:
            print(text)

    conn.close()


def main():

    host = "localhost"
    port = 8888

    print("listening to: {}:{}".format(host, port))

    while True:
        listen(util.connect(host, port))
        print("connection closed")


if __name__ == "__main__":
    main()

