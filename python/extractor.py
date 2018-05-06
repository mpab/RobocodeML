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


def make_features_fp(features_class):
    fp = cfg.ensure_fp(cfg.features_root + features_class, cfg.features)
    return fp


def make_features_fp2(features_class, features_filter):
    fp = cfg.ensure_fp(cfg.features_root + features_class + '_' + features_filter, cfg.features)
    return fp

def fn_name(pure_pure, features_class, features_filter, target):
    return features_class + '_' + features_filter + '_' + target


def fn_feature(pure_pure, features_class, features_filter, target):
    ex1 = extract(features_class, pure_pure)


def features_combinations(pure_pure, fn):
    for features_class in cfg.features_classes:
        for features_filter in cfg.features_filters:
            for target in cfg.onehot_targets:
                return fn(pure_pure, features_class, features_filter, target)


def extract_to_csv2(obs_list):
    features_fp = []

    # create feature files
    for features_class in cfg.features_classes:
        for features_filter in cfg.features_filters:
            fp = make_features_fp(features_class)
            print("creating features file: {}".format(fp))
            features.csv_create(fp)
            features_fp.append(fp)
            # fp = cfg.ensure_fp(cfg.features_unscanned_root + features_class, cfg.features)
            # print("creating features file: {}".format(fp))
            # features.csv_create(fp)
            # features_fp.append(fp)

    for jsn in obs_list:
        obs = observations.json_to_observation(jsn)

        pure_pure = features.observation_to_features(obs)

        for features_class in cfg.features_classes:
            for features_filter in cfg.features_filters:

                out = extract(features_class, pure_pure)

                if out is None:
                    raise RuntimeError("no feature converter for features_class: {}".format(features_class))

                # fp = cfg.ensure_fp(cfg.features_unscanned_root + features_class, cfg.features)
                # features.csv_append(fp, out)

                if obs.scanned:
                    fp = make_features_fp(features_class)
                    features.csv_append(fp, out)

    for fp in features_fp:
        size = os.path.getsize(fp)
        if size < 1024:
            print("WARNING: length of file {} is {} bytes".format(features_fp, size))


def extract_to_csv(obs_list):

    features_fp = []

    # create feature files
    for features_class in cfg.features_classes:
        # for features_filter in cfg.features_filters:
        fp = make_features_fp(features_class)
        print("creating features file: {}".format(fp))
        features.csv_create(fp)
        features_fp.append(fp)
        #print("creating features file: {}".format(fp))
        #features.csv_create(fp)
        #features_fp.append(fp)

    for jsn in obs_list:
        obs = observations.json_to_observation(jsn)
        
        pure_pure = features.observation_to_features(obs)

        for features_class in cfg.features_classes:

            out = extract(features_class, pure_pure)

            if out is None:
                raise RuntimeError("no feature converter for features_class: {}".format(features_class))

            #fp = cfg.ensure_fp(cfg.features_unscanned_root + features_class, cfg.features)
            #features.csv_append(fp, out)

            if obs.scanned:
                fp = make_features_fp(features_class)
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
