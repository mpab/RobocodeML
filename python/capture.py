#!/usr/bin/env python3

import errno
import json
import socket
import cfg

import observations
import util


def capture(conn, obs_fp, tracker):

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
            obs = observations.json_to_observation(jsn)

            if tracker is None:
                tracker = util.Tracker(obs)
            else:
                tracker.update(obs)
                observations.csv_append(obs_fp, obs)

    conn.close()

    return tracker


def main():

    tracker = None
    host = "localhost"
    port = 8888

    obs_fp = cfg.ensure_fp(cfg.observations_root, cfg.observations)
    observations.csv_create(obs_fp)

    print("capturing from: {}:{}".format(host, port))
    print("waiting for data...")

    while True:

        tracker = capture(util.connect(host, port), obs_fp, tracker)

        if tracker is None:
            print("invalid battle tracker, aborting")
            return

        print("captured round: {}/{}".format(tracker.round, tracker.num_rounds))

        if tracker.round == tracker.num_rounds:
            print("saved observations to: {}".format(obs_fp))
            return


if __name__ == "__main__":
    main()
