#!/usr/bin/env python3

import errno
import json
import socket
import pathlib

import observation
import util


def capture(conn, filepath, tracker):

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
            connected = False
            continue

        fragment = msg.decode('utf-8')
        text = p.scan(fragment)

        if text is not None:
            jsn = json.loads(text)
            obs = observation.json_to_observation(jsn)

            if tracker is None:
                tracker = util.Tracker(obs)
            else:
                tracker.update(obs)

                observation.csv_append(filepath, obs)

    conn.close()

    return tracker


def main():

    filepath = "../data/observations.csv"
    tracker = None

    host = "localhost"
    port = 8888

    print("capturing from: {}:{}".format(host, port))
    print("saving to: {}".format(filepath))

    path = pathlib.Path('../data')
    path.mkdir(parents=True, exist_ok=True)
    observation.csv_create(filepath)

    while True:

        tracker = capture(util.connect(host, port), filepath, tracker)

        if tracker is None:
            print("invalid battle tracker, aborting")
            return

        print("captured round: {}/{}".format(tracker.round, tracker.num_rounds))

        if tracker.round == tracker.num_rounds:
            print("saved observations to: {}".format(filepath))
            return


if __name__ == "__main__":
    main()

