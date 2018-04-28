#!/usr/bin/env python3

import errno
import json
import socket
import pathlib

import parser
import features

class Tracker:
    def __init__(self, obs):
        self.num_rounds = obs.num_rounds
        self.round = obs.round
        self.frame = obs.frame

    def update(self, obs):
        if self.num_rounds != obs.num_rounds:
            raise RuntimeError("number of rounds has changed")

        round_diff = obs.round - self.round
        if round_diff > 1:
            raise RuntimeError("missed a round")

        if round_diff > 0:
            self.round = obs.round
            self.frame = obs.frame
            return

        frame_diff = obs.frame - self.frame
        if frame_diff > 1:
            raise RuntimeError("missed a frame")

        if frame_diff == 0:
            raise RuntimeError("frame was not updated")

        self.frame = obs.frame


def connect(host, port):
    soc = socket.socket()
    host = "localhost"
    port = 8888
    soc.bind((host, port))
    soc.listen(5)
    conn, addr = soc.accept()
    return conn


def capture(conn, filepath, tracker):

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

        text = msg.decode('utf-8')
        jstr = p.scan(text)

        if jstr is not None:
            jsn = json.loads(jstr)
            obs = features.extract(jsn)

            if tracker is None:
                tracker = Tracker(obs)
            else:
                tracker.update(obs)

            features.csv_append(filepath, obs)

    conn.close()

    return tracker


def main():

    filepath = "data/features.csv"
    tracker = None

    host = "localhost"
    port = 8888

    print("capturing from: {}:{}".format(host, port))
    print("saving to: {}".format(filepath))

    path = pathlib.Path('./data')
    path.mkdir(parents=True, exist_ok=True)
    features.csv_create(filepath)

    while True:

        tracker = capture(connect(host, port), filepath, tracker)

        if tracker is None:
            print("no tracker, aborting")
            return

        if tracker.round == tracker.num_rounds:
            print("complete")
            return

        print("capturing round: {}/{}".format(tracker.round, tracker.num_rounds))


if __name__ == "__main__":
    main()

