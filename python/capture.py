#!/usr/bin/env python3

import errno
import json
import socket
import pathlib

import observation
import features
import util


def capture(conn, obs_fp, feat_fp, num_rewards, tracker):

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

                observation.csv_append(obs_fp, obs)

                feat = features.observation_to_features(obs)

                if feat is not None:
                    norm = features.normalise_features(feat)

                    for n in range(num_rewards):
                        actual_fp = feat_fp.format(n)
                        features.set_reward(norm, n)
                        features.csv_append(actual_fp, norm)

    conn.close()

    return tracker


def main():

    num_rewards = 5

    obs_fp = "../data/observations.csv"
    feat_fp = "../data/features_rwd_{}.csv"
    tracker = None

    host = "localhost"
    port = 8888

    path = pathlib.Path('../data')
    path.mkdir(parents=True, exist_ok=True)
    observation.csv_create(obs_fp)

    print("capturing from: {}:{}".format(host, port))
    print("creating: {}".format(obs_fp))

    for n in range(num_rewards):
        actual_fp = feat_fp.format(n)
        print("creating: {}".format(actual_fp))
        features.csv_create(actual_fp)

    while True:

        tracker = capture(util.connect(host, port), obs_fp, feat_fp, num_rewards, tracker)

        if tracker is None:
            print("invalid battle tracker, aborting")
            return

        print("captured round: {}/{}".format(tracker.round, tracker.num_rounds))

        if tracker.round == tracker.num_rounds:
            print("saved observations to: {}".format(obs_fp))
            for n in range(num_rewards):
                actual_fp = feat_fp.format(n)
                print("saved features to: {}".format(actual_fp))
                features.csv_create(actual_fp)
            return


if __name__ == "__main__":
    main()

