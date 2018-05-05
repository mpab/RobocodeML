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


def test(conn, tracker):

    p = util.MsgParser()

    expected_handshake = 0

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

        if tracker is None:
            tracker = util.Tracker(obs)
        else:
            tracker.update(obs)

        if expected_handshake > 0 and expected_handshake != obs.handshake:
            print("{}/{}: expected_handshake/obs.handshake - {}/{}".format(tracker.round, tracker.frame, expected_handshake, obs.handshake))

        # recommend(obs)
        recommender.random_recommendation(obs)

        expected_handshake = expected_handshake + 1
        obs.handshake = expected_handshake

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
    return tracker


def main():

    tracker = None
    host = "localhost"
    port = 8889

    print("monitoring {}:{}".format(host, port))

    while True:

        tracker = test(util.connect(host, port), tracker)

        if tracker is None:
            print("invalid battle tracker, aborting")
            return

        print("completed round: {}/{}".format(tracker.round, tracker.num_rounds))

        if tracker.round == tracker.num_rounds:
            print("battle ended")
            return


if __name__ == "__main__":
    main()

