#!/usr/bin/env python3

import json
import pathlib
import pandas as pd

import observation
import features


def extract(obs_list):
    # num_rewards = 5

    raw_class_fp = "../data/features/raw_class.csv"
    raw_reg_fp = "../data/features/raw_reg.csv"
    scaled_class_fp = "../data/features/scaled_class.csv"
    scaled_reg_fp = "../data/features/scaled_reg.csv"

    path = pathlib.Path('../data/features')
    path.mkdir(parents=True, exist_ok=True)

    features.csv_create(raw_class_fp)
    features.csv_create(raw_reg_fp)
    features.csv_create(scaled_class_fp)
    features.csv_create(scaled_reg_fp)

    # for n in range(num_rewards):
    #    fp = feat_fp.format(n)
    #    print("creating: {}".format(fp))
    #    features.csv_create(fp)
    #    fp = qfeat_fp.format(n)
    #    print("creating: {}".format(fp))
    #    features.csv_create(fp)

    for jsn in obs_list:

        obs = observation.json_to_observation(jsn)

        feat = features.observation_to_features(obs)

        if feat is not None:
            features.csv_append_classification(raw_class_fp, feat)
            features.csv_append_regression(raw_reg_fp, feat)

            scaled = features.scale(feat)
            features.csv_append_classification(scaled_class_fp, scaled)
            features.csv_append_regression(scaled_reg_fp, feat)

            # for n in range(num_rewards):
            #    fp = feat_fp.format(n)
            #    features.set_reward(feat, n)
            #    features.csv_append(fp, feat)

            #    fp = qfeat_fp.format(n)
            #    features.set_reward(norm, n)
            #    features.csv_append(fp, norm)

    # for n in range(num_rewards):
    #    actual_fp = feat_fp.format(n)
    #    print("saved features to: {}".format(actual_fp))


def main():
    obs_fp = "../data/observations.csv"
    print("extracting from: {}".format(obs_fp))
    frame = pd.read_csv(obs_fp)
    raw = frame.to_json(orient='records')
    obs_list = json.loads(raw)

    extract(obs_list)


if __name__ == "__main__":
    main()
