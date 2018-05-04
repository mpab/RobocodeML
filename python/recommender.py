#!/usr/bin/env python3

import random
import io

import util
import observations
import cfg
import models
import extractor
import features
import datasets

classifier_filter = 'AdaBoost'
# features_classification_filter = 'pure_boolean_classified'
# target_filter = 'enemy_collisions'
__classification_metamodels__ = [None]

num_actions = 5


def classification_models():
    if __classification_metamodels__[0] is not None:
        return __classification_metamodels__[0]

    print('loading models')

    classification_metamodels = {}

    for features_classification in cfg.features_classes:
        for target in cfg.onehot_targets:
            path = '../data/models/' + features_classification + '/' + classifier_filter + '/' + target
            # print(path)
            mm = models.load(path)
            key = features_classification + '_' + target
            # print(key)
            # print(model.name)
            # print(model.description)
            classification_metamodels[key] = mm

    __classification_metamodels__[0] = classification_metamodels
    return __classification_metamodels__[0]


def select_classification_metamodel(features_classification, target):
    key = features_classification + '_' + target
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

    for action in randomized_actions():
        record.action = action
        csv_data += '\n'
        csv_data += features.to_string(record)

    data_fp = io.StringIO(csv_data)
    ds = datasets.from_csv(data_fp, cfg.onehot_targets, target_name)

    return ds, csv_data


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


def avoid_wall(obs):
    predictions, _, _ = predict(obs, 'scaled_boolean', 'avoid_wall')
    lowest = 99999
    for idx, p in enumerate(predictions):
        if p < lowest:
            obs.action = idx + 1
    print("avoid_wall recommendation: {} ({})".format(obs.action, lowest))
    return random_recommendation(obs)


def avoid_shell(obs):
    predictions, _, _ = predict(obs, 'scaled_boolean', 'shell_wounds')
    lowest = 99999
    for idx, p in enumerate(predictions):
        if p < lowest:
            obs.action = idx + 1
    print("avoid_shell recommendation: {} ({})".format(obs.action, lowest))
    return random_recommendation(obs)


def recommend(obs):
    return avoid_wall(obs)


def test_recommendations_from_observations():
    obs_fp = cfg.ensure_fp(cfg.observations_root, cfg.observations)
    print("recommending from: {}".format(obs_fp))
    obs_list = util.csv_to_json(obs_fp)

    print('-------------------- PREDICTIONS --------------------')

    for idx, jsn in enumerate(obs_list):

        obs = observations.json_to_observation(jsn)

        for feat_class_filt in cfg.features_classes:
            for target in cfg.onehot_targets:
                predictions, _, _ = predict(obs, feat_class_filt, target)

                found = False
                n = predictions[0]
                for t in predictions:
                    if found:
                        continue

                    if n != t:
                        print("{}: target={}, feat_class_filt={}, predictions={}".format(
                            idx, target, feat_class_filt, predictions))
                        found = True
                        continue


def test_randomized_actions():
    for _ in range(10000):
        for idx in randomized_actions():
            if idx < 1 or idx > num_actions:
                raise RuntimeError('randomized_actions: {}'.format(idx))
    print('randomized_actions passed')


def main():
    test_randomized_actions()
    test_recommendations_from_observations()


if __name__ == "__main__":
    main()
