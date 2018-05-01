#!/usr/bin/env python3

import util
import observations
import cfg
import models
import extractor
import features
import random

enemy_collisions = cfg.ensure_path("../data/models/pure_boolean_classified/mlp_classifier_7_7_7_pca_5/enemy_collisions")
shell_wounds = cfg.ensure_path("../data/models/pure_boolean_classified/mlp_classifier_7_7_7_pca_5/shell_wounds")
wall_collisions = cfg.ensure_path("../data/models/pure_boolean_classified/mlp_classifier_7_7_7_pca_5/wall_collisions")

ecm = models.load(enemy_collisions)
swm = models.load(shell_wounds)
wcm = models.load(wall_collisions)


def xrecommend(obs):
    features_class = "pure_boolean_classified"
    pure_pure = features.observation_to_features(obs)
    pure_boolean_classified = extractor.extract(features_class, pure_pure)

    if pure_boolean_classified is None:
        raise RuntimeError("no feature converter for features_class: {}".format(features_class))

    ecr = ecm.model


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
