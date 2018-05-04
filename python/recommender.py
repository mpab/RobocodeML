#!/usr/bin/env python3

import random
import io
import copy

import util
import observations
import cfg
import models
import extractor
import features
import datasets

model_name = 'AdaBoost'
# features_classification_filter = 'pure_boolean_classified'
# target_filter = 'enemy_collisions'
__classification_metamodels__ = [None]

num_actions = 5


def make_key(features_classification, target_name):
    return features_classification + '_' + model_name + '_' + target_name


def model_path(features_classification, target_name):
    path = '../data/models/' + features_classification + '/' + model_name + '/' + target_name
    # print(path)
    return path


def classification_models():
    if __classification_metamodels__[0] is not None:
        return __classification_metamodels__[0]

    print('loading models')

    classification_metamodels = {}

    for features_classification in cfg.features_classes:
        for target_name in cfg.onehot_targets:
            mm = models.load(model_path(features_classification, target_name))
            key = make_key(features_classification, target_name)
            classification_metamodels[key] = mm

    __classification_metamodels__[0] = classification_metamodels
    return __classification_metamodels__[0]


def select_classification_metamodel(features_classification, target_name):
    key = make_key(features_classification, target_name)
    return classification_models()[key]


def test_select_classification_metamodel():
    for features_class in cfg.features_classes:
        for target in cfg.onehot_targets:
            mdl = select_classification_metamodel(features_class, target)
            print('features_class: {}, target: {}, model: {}'.format(features_class, target, mdl.name))


def model(feat_class_filt, target_name):
    return select_classification_metamodel(feat_class_filt, target_name).model


def randomized_actions():
    indices = random.sample(range(1, num_actions + 1), num_actions)
    for idx in indices:
        yield idx


def create_features_test_dataset(feat_class_filt, feat, target_name):
    csv_data = features.header()

    record = extractor.extract(feat_class_filt, feat)
    if record is None:
        raise RuntimeError("no feature converter for features_class: {}".format(feat_class_filt))

    test_features = []

    for action in randomized_actions():
        test_feature = copy.copy(record)
        test_feature.action = action
        test_features.append(test_feature)
        csv_data += '\n'
        csv_data += features.to_string(test_feature)

    data_fp = io.StringIO(csv_data)
    ds = datasets.from_csv(data_fp, cfg.onehot_targets, target_name)

    return ds, test_features


def predict(obs, feat_class_filt, target_name):
    obs.scanned = True

    pure_pure = features.observation_to_features(obs)
    if pure_pure is None:
        raise RuntimeError("failed to convert observation to features")

    ds, test_features = create_features_test_dataset(feat_class_filt, pure_pure, target_name)
    mdl = model(feat_class_filt, target_name)
    predictions = mdl.predict(ds.data)
    return predictions, ds.data, test_features


def random_recommendation(obs):
    action = random.randint(1, 5)
    obs.action = action
    return obs


def randomize_predictions(predictions):
    np = len(predictions)
    indices = random.sample(range(1, np + 1), np)
    for idx in indices:
        yield predictions[idx]


def minimise(obs, feat_class_filt, target_name):
    predictions, _, test_features = predict(obs, feat_class_filt, target_name)
    lowest = 99999
    for idx, p in enumerate(predictions):
        if p < lowest:
            lowest = p
            feat = test_features[idx]
            obs.action = feat.action
    print("minimise {} recommendation: {} ({})".format(target_name, obs.action, lowest))
    # print("{}/{})".format(predictions, features.to_string(feat)))
    return lowest


def maximise(obs, feat_class_filt, target_name):
    predictions, _, test_features = predict(obs, feat_class_filt, target_name)
    highest = -1
    for idx, p in enumerate(predictions):
        if p > highest:
            highest = p
            feat = test_features[idx]
            obs.action = feat.action
    print("maximise {} recommendation: {} ({})".format(target_name, obs.action, highest))
    # print("{}/{})".format(predictions, features.to_string(feat)))
    return highest


def minimise_enemy_collisions(obs):
    return minimise(obs, 'scaled_pure', 'enemy_collisions')


def minimise_wall_collisions(obs):
    return minimise(obs, 'scaled_pure', 'wall_collisions')


def minimise_shell_wounds(obs):
    return minimise(obs, 'scaled_pure', 'shell_wounds')


def maximise_shell_intercepts(obs):
    return maximise(obs, 'scaled_pure', 'shell_intercepts')


def maximise_shell_hits(obs):
    return maximise(obs, 'scaled_pure', 'shell_hits')


def recommend(obs):
    lowest = minimise_wall_collisions(obs)
    return lowest


def test_recommendations_from_observations():
    obs_fp = cfg.ensure_fp(cfg.observations_root, cfg.observations)
    print("recommending from: {}".format(obs_fp))
    obs_list = util.csv_to_json(obs_fp)

    print('-------------------- PREDICTIONS --------------------')

    for idx, jsn in enumerate(obs_list):

        obs = observations.json_to_observation(jsn)

        for feat_class_filt in cfg.features_classes:
            for target in cfg.onehot_targets:
                predictions, _, test_features = predict(obs, feat_class_filt, target)

                found = False
                n = predictions[0]
                for t in predictions:
                    if found:
                        continue

                    if n != t:
                        print("{}: target={}, feat_class_filt={}, predictions={}".format(
                            idx, target, feat_class_filt, predictions))
                        for f in test_features:
                            print(features.to_string(f))
                        found = True
                        continue


def test_recommenders():
    obs_fp = cfg.ensure_fp(cfg.observations_root, cfg.observations)
    print("recommending from: {}".format(obs_fp))
    obs_list = util.csv_to_json(obs_fp)

    print('-------------------- RECOMMENDATIONS --------------------')

    for idx, jsn in enumerate(obs_list):
        print('observation: {}'.format(idx))
        obs = observations.json_to_observation(jsn)

        minimise_enemy_collisions(obs)
        minimise_wall_collisions(obs)
        minimise_shell_wounds(obs)
        maximise_shell_intercepts(obs)
        maximise_shell_hits(obs)


def test_randomized_actions():
    for _ in range(10000):
        for idx in randomized_actions():
            if idx < 1 or idx > num_actions:
                raise RuntimeError('randomized_actions: {}'.format(idx))
    print('randomized_actions passed')


def main():
    test_randomized_actions()
    test_recommenders()
    # test_recommendations_from_observations()


if __name__ == "__main__":
    main()
