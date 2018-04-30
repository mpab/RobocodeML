#!/usr/bin/env python3

import json
import pathlib
import pandas as pd

import observation
import features


def extract(obs_list):
    num_rewards = 5

    feat_fp = "../data/features/feat_reward_{}.csv"
    qfeat_fp = "../data/features/qfeat_reward_{}.csv"

    path = pathlib.Path('../data/features')
    path.mkdir(parents=True, exist_ok=True)

    for n in range(num_rewards):
        fp = feat_fp.format(n)
        print("creating: {}".format(fp))
        features.csv_create(fp)
        fp = qfeat_fp.format(n)
        print("creating: {}".format(fp))
        features.csv_create(fp)

    for jsn in obs_list:

        obs = observation.json_to_observation(jsn)

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

    for n in range(num_rewards):
        actual_fp = feat_fp.format(n)
        print("saved features to: {}".format(actual_fp))


def main():
    obs_fp = "../data/observations.csv"
    print("extracting from: {}".format(obs_fp))
    frame = pd.read_csv(obs_fp)
    raw = frame.to_json(orient='records')
    obs_list = json.loads(raw)

    extract(obs_list)


if __name__ == "__main__":
    main()
