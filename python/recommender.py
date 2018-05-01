#!/usr/bin/env python3

import random

import util
import observations
import cfg
import models
import extractor
import features
import classification_ds

enemy_collisions = cfg.ensure_path("../data/models/pure_boolean_classified/mlp_classifier_7_7_7_pca_5/enemy_collisions")
shell_wounds = cfg.ensure_path("../data/models/pure_boolean_classified/mlp_classifier_7_7_7_pca_5/shell_wounds")
wall_collisions = cfg.ensure_path("../data/models/pure_boolean_classified/mlp_classifier_7_7_7_pca_5/wall_collisions")

ecm = models.load(enemy_collisions)
swm = models.load(shell_wounds)
wcm = models.load(wall_collisions)


def xrecommend(obs):
    obs.scanned = True  # enable the conversion...
    features_class = "pure_boolean_classified"

    pure_pure = features.observation_to_features(obs)
    if pure_pure is None:
        raise RuntimeError("failed to convert observation to features")

    pure_boolean_classified = extractor.extract(features_class, pure_pure)

    if pure_boolean_classified is None:
        raise RuntimeError("no feature converter for features_class: {}".format(features_class))

    # TODO: convert observation to dataframe and process using dataset
    data_fp = "../data/features/pure_classified/features.csv"
    discard = cfg.onehot_targets
    target_name = cfg.onehot_targets[0]
    ds = classification_ds.load_encoded(data_fp, discard, target_name)

    prediction = ecm.model.predict(pure_boolean_classified)

    print(prediction)


def recommend(obs):
    action = random.randint(1, 5)
    obs.action = action
    print("recommending action: {}".format(obs.action))
    return obs


def main():
    obs_fp = cfg.ensure_fp(cfg.observations_root, cfg.observations)
    print("recommending from: {}".format(obs_fp))
    obs_list = util.csv_to_json(obs_fp)

    for jsn in obs_list:
        obs = observations.json_to_observation(jsn)

        r = xrecommend(obs)


if __name__ == "__main__":
    main()
