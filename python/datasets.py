#!/usr/bin/env python3

import os
import datetime
import json
import logging
import cfg

import pandas as pd
from sklearn.datasets.base import Bunch
from sklearn.preprocessing import LabelEncoder


# -----------------------------------------------------------

__logger__ = [None]


def log():

    if __logger__[0] is not None:
        return __logger__[0]

    log_name = '{:%Y-%m-%d_%H.%M.%S}'.format(datetime.datetime.now()) + '_' + os.path.basename(__file__) + '.log'

    log_fp = cfg.ensure_fp(cfg.data_root + 'logs', log_name)

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(log_name)
    fh = logging.FileHandler(log_fp)
    fh.setLevel(logging.INFO)
    logger.addHandler(fh)
    __logger__[0] = logger
    return __logger__[0]

# -----------------------------------------------------------

def check_discard_list(discard, target):

    filtered = list(discard)

    if target in discard:
        filtered.remove(target)

    return filtered

def load_csv_and_discard(data_fp, discard_list, target_name):
    df = pd.read_csv(data_fp)

    checked_discard_list = check_discard_list(discard_list, target_name)

    feature_names = list(df.columns)
    for d in checked_discard_list:
        for f in feature_names:
            if d in f:
                log().debug('discard feature: {}'.format(d))
                feature_names.remove(d)
                df = df.drop(d, axis=1)

    feature_names.remove(target_name)
    column_names = list(df.columns)
    target_names = list(df[column_names[-1]].unique())

    ds = Bunch(
        data=df[column_names[:-1]].as_matrix(),
        target=df[column_names[-1]].as_matrix(),
        feature_names=feature_names,
        target_name=target_name)

    return ds, df, feature_names, target_names


def from_csv(data_fp, discard_list, target_name):
    ds, _, _, _ = load_csv_and_discard(data_fp, discard_list, target_name)
    return ds


def from_csv_with_target_names(data_fp, discard_list, target_name):
    ds, _, _, target_names = load_csv_and_discard(data_fp, discard_list, target_name)
    ds.target_names = target_names
    return ds


def load_features_u():
    data_fp = '../data/features/pure_pure/features.csv'
    discard_list = [
        'enemy_collisions',
        'wall_collisions',
        'shell_hits',
        'shell_wounds']

    ds = from_csv(data_fp, discard_list, 'shell_intercepts')

    return ds


def load_features_c():
    data_fp = '../data/features/pure_pure/features.csv'
    discard_list = [
        'enemy_collisions',
        'wall_collisions',
        'shell_hits',
        'shell_wounds']

    ds = from_csv_with_target_names(data_fp, discard_list, 'shell_intercepts')

    return ds


def datasets():
    yield load_features_u()
    yield load_features_c()


def print_info(ds):
    try:
        print("feature names:", ds.feature_names)
    except:
        print("no feature names")

    try:
        print("target name:", ds.target_name)
    except:
        print("no target name")

    try:
        print("target names type:", type(ds.target_names))
        print("target names:", ds.target_names)
    except:
        print("no target names")

    X = ds.data
    y = ds.target

    print("Type of X is:", type(X))  # should be <class 'pandas.core.frame.DataFrame'>
    print("Type of y is:", type(y))  # should be <class 'numpy.ndarray'>

    # printing first 5 input rows
    print("First 5 rows of X:\n", X[:5])
    print("First 5 rows of y:\n", y[:5])

    print()


def main():
    for ds in datasets():
        print_info(ds)


if __name__ == '__main__':
    main()
