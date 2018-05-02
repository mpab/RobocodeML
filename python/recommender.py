#!/usr/bin/env python3

import random

import util
import observations
import cfg
import models
import extractor
import features
import classification_ds


classifier_filter = 'mlp_classifier_7_7_7_pca_5'
#features_classification_filter = 'pure_boolean_classified'
#target_filter = 'enemy_collisions'
__classification_metamodels__ = [None]


def load_classification_models():

    if __classification_metamodels__[0] is not None:
        return __classification_metamodels__[0]

    classification_metamodels = {}

    for features_classification in cfg.classification_compatible:
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
    load_classification_models()
    key = features_classification + '_' + target
    return __classification_metamodels__[0][key]


def test_select_classification_metamodel():
    for features_class in cfg.classification_compatible:
        for target in cfg.onehot_targets:
            mdl = select_classification_metamodel(features_class, target)
            print('features_class: {}, target: {}, model: {}'.format(features_class, target, mdl.name))


def model(feat_class_filt, target):
    return select_classification_metamodel(feat_class_filt, target).model


def predict(obs, feat_class_filt, target):

    obs.scanned = True

    pure_pure = features.observation_to_features(obs)
    if pure_pure is None:
        raise RuntimeError("failed to convert observation to features")

    eval_features = []
    for action in range(1, 6):
        pbc = extractor.extract(feat_class_filt, pure_pure)
        if pbc is None:
            raise RuntimeError("no feature converter for features_class: {}".format(feat_class_filt))

        pbc.action = action
        eval_features.append(pbc)

    # TODO: convert observation to dataframe and process using dataset
    data_fp = './features.csv'
    features.csv_create(data_fp)
    for ef in eval_features:
        features.csv_append(data_fp, ef)

    discard = cfg.onehot_targets
    target_name = 'enemy_collisions'

    ds = classification_ds.load_encoded(data_fp, discard, target_name)

    mdl = model(feat_class_filt, target)
    predictions = mdl.predict(ds.data)
    return predictions, ds.data, eval_features


def avoid_wall_recommendation(obs):
    predictions, data, evfs = predict(obs, 'scaled_classified', 'wall_collisions')
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
    # test_select_classification_model()
    obs_fp = cfg.ensure_fp(cfg.observations_root, cfg.observations)
    print("recommending from: {}".format(obs_fp))
    obs_list = util.csv_to_json(obs_fp)

    print('-------------------- PREDICTIONS --------------------')

    for idx, jsn in enumerate(obs_list):

        obs = observations.json_to_observation(jsn)

        for feat_class_filt in cfg.classification_compatible:
            for target in cfg.onehot_targets:
                predictions, data, evfs = predict(obs, feat_class_filt, target)

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


if __name__ == "__main__":
    main()