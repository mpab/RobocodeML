#!/usr/bin/env python3

import os

import json
import pandas as pd

import cfg
import features
import observations


def extract(obs_list):

    features_fp = []

    # create feature files
    for features_class in cfg.features_classes:
        fp = cfg.ensure_fp(cfg.features_root + features_class, cfg.features)
        print("creating features file: {}".format(fp))
        features.csv_create(fp)
        features_fp.append(fp)

    for jsn in obs_list:
        obs = observations.json_to_observation(jsn)
        pure_pure = features.observation_to_features(obs)

        if pure_pure is None:
            continue

        for features_class in cfg.features_classes:

            fp = cfg.ensure_fp(cfg.features_root + features_class, cfg.features)

            if features_class == "pure_pure":
                features.csv_append(fp, pure_pure)

            if features_class == "pure_classified":
                out = features.classify(pure_pure)
                features.csv_append(fp, out)

            if features_class == "pure_boolean":
                out = features.binarise(pure_pure)
                features.csv_append(fp, out)

            if features_class == "pure_boolean_classified":
                out = features.binarise(pure_pure)
                out = features.classify(out)
                features.csv_append(fp, out)

            scaled_pure = features.scale(pure_pure)

            if features_class == "scaled_pure":
                features.csv_append(fp, scaled_pure)

            if features_class == "scaled_classified":
                out = features.classify(scaled_pure)
                features.csv_append(fp, out)

            if features_class == "scaled_boolean":
                out = features.binarise(scaled_pure)
                features.csv_append(fp, out)

            if features_class == "scaled_boolean_classified":
                out = features.binarise(scaled_pure)
                out = features.classify(out)
                features.csv_append(fp, out)

    for fp in features_fp:
        if not fp.exists():
            raise RuntimeError("features file: {} not found".format(features_fp))

        size = os.path.getsize(fp)
        if size < 1024:
            print("WARNING: length of file {} is {} bytes".format(features_fp, size))


def main():
    obs_fp = cfg.ensure_fp(cfg.observations_root, cfg.observations)
    print("extracting from: {}".format(obs_fp))
    frame = pd.read_csv(obs_fp)
    raw = frame.to_json(orient='records')
    obs_list = json.loads(raw)

    extract(obs_list)


if __name__ == "__main__":
    main()
