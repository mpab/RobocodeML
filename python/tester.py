#!/usr/bin/env python3

import errno
import json
import socket

import recommender
import observations
import util


def connect(host, port):
    soc = socket.socket()
    soc.bind((host, port))
    soc.listen(5)
    conn, addr = soc.accept()
    return conn


def test(conn):

    p = util.MsgParser()

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

        fragment = msg.decode('utf-8')
        text = p.scan(fragment)

        if text is None:
            continue

        jsn = json.loads(text)
        obs = observations.json_to_observation(jsn)

        recommend(obs)

        reply = json.dumps(obs.__dict__) + '\n'  # add EOL for java client

        try:
            conn.send(reply.encode('utf-8'))
        except socket.error as e:
            if e.errno == errno.ECONNRESET:
                print("connection reset")
            else:
                print("connection error")
            connected = False

    conn.close()
    print("disconnected")

def obs_fp():
    return '../data/observations/minimise_shell_wounds.csv'


def log_init():
    print('creating: {}'.format(obs_fp()))
    observations.csv_create(obs_fp())


def recommend(obs):
    recommender.minimise_shell_wounds(obs)
    observations.csv_append(obs_fp(), obs)


def main():

    host = "localhost"
    port = 8889

    log_init()

    print("monitoring {}:{}".format(host, port))

    while True:
        test(util.connect(host, port))


if __name__ == "__main__":
    main()

