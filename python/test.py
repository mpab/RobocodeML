#!/usr/bin/env python3

import errno
import json
import socket

import parser
import observation
import features
import nnet


def connect(host, port):
    soc = socket.socket()
    soc.bind((host, port))
    soc.listen(5)
    conn, addr = soc.accept()
    return conn


def test(conn, tracker):

    p = parser.MsgParser();

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

        if text is None:
            continue

        jsn = json.loads(text)
        obs = observation.json_to_observation(jsn)
        feat = features.observation_to_features(obs)

        action = nnet.recommend(feat)
        obs.action = action

        #print(text)
        recommendation = json.dumps(obs.__dict__)

        try:
            conn.send(recommendation + "\n")  # add EOL for java client
            print("recommending action: {}".format(action))
        except socket.error as e:
            if e.errno == errno.ECONNRESET:
                print("connection reset")
            else:
                print("connection error")
            connected = False

    conn.close()

    return tracker


def main():

    tracker = None

    host = "localhost"
    port = 8889

    print("monitoring {}:{}".format(host, port))

    while True:

        tracker = test(connect(host, port), tracker)

        if tracker is not None:
            print("round: {}/{}".format(tracker.round, tracker.num_rounds))


if __name__ == "__main__":
    main()

