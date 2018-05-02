#!/usr/bin/env python3

import os

import util
import cfg
import features
import observations


def extract(features_class, pure_pure):
    if features_class == "pure_pure":
        return pure_pure

    if features_class == "pure_classified":
        return features.classify(pure_pure)

    if features_class == "pure_boolean":
        return features.binarise(pure_pure)

    if features_class == "pure_boolean_classified":
        out = features.binarise(pure_pure)
        return features.classify(out)

    scaled_pure = features.scale(pure_pure)

    if features_class == "scaled_pure":
        return scaled_pure

    if features_class == "scaled_classified":
        return features.classify(scaled_pure)

    if features_class == "scaled_boolean":
        return features.binarise(scaled_pure)

    if features_class == "scaled_boolean_classified":
        out = features.binarise(scaled_pure)
        return features.classify(out)

    return None


def extract_to_csv(obs_list):

    features_fp = []

    # create feature files
    for features_class in cfg.features_classes:
        fp = cfg.ensure_fp(cfg.features_root + features_class, cfg.features)
        print("creating features file: {}".format(fp))
        features.csv_create(fp)
        features_fp.append(fp)
        fp = cfg.ensure_fp(cfg.features_scanned_root + features_class, cfg.features)
        print("creating features file: {}".format(fp))
        features.csv_create(fp)
        features_fp.append(fp)

    for jsn in obs_list:
        obs = observations.json_to_observation(jsn)
        
        pure_pure = features.observation_to_features(obs)

        for features_class in cfg.features_classes:

            out = extract(features_class, pure_pure)

            if out is None:
                raise RuntimeError("no feature converter for features_class: {}".format(features_class))

            fp = cfg.ensure_fp(cfg.features_root + features_class, cfg.features)
            features.csv_append(fp, out)

            if obs.scanned:
                fp = cfg.ensure_fp(cfg.features_scanned_root + features_class, cfg.features)
                features.csv_append(fp, out)

    for fp in features_fp:
        size = os.path.getsize(fp)
        if size < 1024:
            print("WARNING: length of file {} is {} bytes".format(features_fp, size))


def main():
    obs_fp = cfg.ensure_fp(cfg.observations_root, cfg.observations)
    print("extracting from: {}".format(obs_fp))
    obs_list = util.csv_to_json(obs_fp)

    extract_to_csv(obs_list)


if __name__ == "__main__":
    main()
