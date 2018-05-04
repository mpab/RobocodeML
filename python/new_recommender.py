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

# classifier_filter = 'AdaBoost'
# features_classification_filter = 'pure_boolean_classified'
# target_filter = 'enemy_collisions'
__classification_metamodels__ = [None]


def make_key(features_classification, model_name, target_name):
    return features_classification + '_' + model_name + '_' + target_name


def classification_models():
    if __classification_metamodels__[0] is not None:
        return __classification_metamodels__[0]

    print('loading models')

    classification_metamodels = {}

    for target_name in cfg.onehot_targets:
        for model_info in models.models_info:
            for features_classification in cfg.features_classes:
                for target in cfg.onehot_targets:
                    path = '../data/models/' + features_classification + '/' + model_info[0] + '/' + target
                    # print(path)
                    mm = models.load(path)
                    if mm is None:
                        continue
                    key = make_key(features_classification, model_info[0], target_name)
                    # print(key)
                    # print(model.name)
                    # print(model.description)
                    classification_metamodels[key] = mm

    __classification_metamodels__[0] = classification_metamodels
    return __classification_metamodels__[0]


def select_classification_metamodel(features_classification, model_name, target_name):
    key = make_key(features_classification, model_name, target_name)
    return classification_models()[key]


def test_select_classification_metamodel():
    for model_info in models.models_info:
        for features_classification in cfg.features_classes:
            for target in cfg.onehot_targets:
                mdl = select_classification_metamodel(features_classification, model_info[0], target)
                print('features_class: {}, target: {}, model: {}'.format(features_classification, target, mdl.name))


def model(features_classification, model_name, target_name):
    return select_classification_metamodel(features_classification, model_name, target_name).model


def create_features_test_dataset(features_classification, feat, target_name):
    csv_data = features.header()

    record = extractor.extract(features_classification, feat)
    if record is None:
        raise RuntimeError("no feature converter for features_class: {}".format(features_classification))

    for action in range(1, 6):
        record.action = action
        csv_data += '\n'
        csv_data += features.to_string(record)

    data_fp = io.StringIO(csv_data)
    ds = datasets.from_csv(data_fp, cfg.onehot_targets, target_name)

    return ds, csv_data


def predict(obs, features_classification, model_name, target_name):
    obs.scanned = True

    pure_pure = features.observation_to_features(obs)
    if pure_pure is None:
        raise RuntimeError("failed to convert observation to features")

    ds, test_features = create_features_test_dataset(features_classification, pure_pure, target_name)
    mdl = model(features_classification, model_name, target_name)
    predictions = mdl.predict(ds.data)
    return predictions, ds.data, test_features


def avoid_wall_recommendation(obs):
    predictions, _, _ = predict(obs, 'pure_boolean', 'AdaBoost', 'wall_collisions')
    for idx, p in enumerate(predictions):
        if p == 0:
            obs.action = idx + 1
            print("avoid_wall_recommendation: {}".format(obs.action))
            return obs
    return random_recommendation(obs)


def random_recommendation(obs):
    action = random.randint(1, 5)
    obs.action = action
    print("random_recommendation action: {}".format(obs.action))
    return obs


def recommend(obs):
    return random_recommendation(obs)


def main():
    test_select_classification_metamodel()

    obs_fp = cfg.ensure_fp(cfg.observations_root, cfg.observations)
    print("recommending from: {}".format(obs_fp))
    obs_list = util.csv_to_json(obs_fp)

    print('-------------------- PREDICTIONS --------------------')

    for idx, jsn in enumerate(obs_list):

        obs = observations.json_to_observation(jsn)

        for model_info in models.models_info:
            for features_classification in cfg.features_classes:
                for target_name in cfg.onehot_targets:
                    model_name = model_info[0]
                    predictions, _, _ = predict(obs, features_classification, model_name, target_name)

                    found = False
                    n = predictions[0]
                    for t in predictions:
                        if found:
                            continue

                        if n != t:
                            print("{}: model={}, target_name={}, features_classification={}, predictions={}".format(
                                idx, model_name, target_name, features_classification, predictions))
                            found = True
                            continue


if __name__ == "__main__":
    main()
