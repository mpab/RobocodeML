#!/usr/bin/env python3

import errno
import json
import socket
import pathlib
import threading

import observation
import features
import util


def capture(conn, tracker):

    observations = []

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

                observations.append(obs)

    conn.close()

    return tracker, observations


def save(observations):
    num_rewards = 5
    obs_fp = "../data/observations.csv"
    feat_fp = "../data/features/feat_reward_{}.csv"
    qfeat_fp = "../data/features/qfeat_reward_{}.csv"

    path = pathlib.Path('../data/features')
    path.mkdir(parents=True, exist_ok=True)

    print("creating: {}".format(obs_fp))
    observation.csv_create(obs_fp)

    for n in range(num_rewards):
        fp = feat_fp.format(n)
        print("creating: {}".format(fp))
        features.csv_create(fp)
        fp = qfeat_fp.format(n)
        print("creating: {}".format(fp))
        features.csv_create(fp)

    for obs in observations:

        observation.csv_append(obs_fp, obs)

        feat = features.observation_to_features(obs)

        if feat is not None:
            norm = features.normalise_features(feat)

            for n in range(num_rewards):
                fp = feat_fp.format(n)
                features.set_reward(feat, n)
                features.csv_append(fp, feat)

                fp = qfeat_fp.format(n)
                features.set_reward(norm, n)
                features.csv_append(fp, norm)

    print("saved observations to: {}".format(obs_fp))
    for n in range(num_rewards):
        actual_fp = feat_fp.format(n)
        print("saved features to: {}".format(actual_fp))


def main():

    tracker = None
    host = "localhost"
    port = 8888

    print("capturing from: {}:{}".format(host, port))
    print("waiting for data...")

    task = None

    observations = []

    while True:

        tracker, new_observations = capture(util.connect(host, port), tracker)

        if tracker is None:
            print("invalid battle tracker, aborting")
            return

        print("captured round: {}/{}".format(tracker.round, tracker.num_rounds))

        observations.extend(new_observations)

        if tracker.round == tracker.num_rounds:
            save(observations)
            return


if __name__ == "__main__":
    main()

