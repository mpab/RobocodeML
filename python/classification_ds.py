#!/usr/bin/env python3

"""
(c) Michael Alderson-Bythell
RobocodeML dataset helper for scikit-learn
used for classifiers
"""

import os
import datetime
import json
import logging

import pandas as pd
from sklearn.datasets.base import Bunch
from sklearn.preprocessing import LabelEncoder

import cfg

# see here for tips on preparing data
# https://districtdatalabs.silvrback.com/building-a-classifier-from-census-data
# https://bbengfort.github.io/programmer/2016/04/19/bunch-data-management.html

# see here for data wrangling
# http://fastml.com/converting-categorical-data-into-numbers-with-pandas-and-scikit-learn/

# -----------------------------------------------------------

__logger__ = [None]


def log():

    if __logger__[0] is not None:
        return __logger__[0]

    log_name = '{:%Y-%m-%d_%H.%M.%S}'.format(datetime.datetime.now()) + '_' + os.path.basename(__file__) + '.log'

    log_fp = cfg.ensure_fp(cfg.data_root + "logs", log_name)

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(log_name)
    fh = logging.FileHandler(log_fp)
    fh.setLevel(logging.INFO)
    logger.addHandler(fh)
    __logger__[0] = logger
    return __logger__[0]

# -----------------------------------------------------------


def create_metadata(data_fp, meta_fp, discard, target_name):
    # analyse csv & create json metadata file
    df = pd.read_csv(data_fp)

    feature_names = list(df.columns)
    for d in discard:
        for f in feature_names:
            if d in f:
                log().info("removing feature: {}".format(d))
                feature_names.remove(d)
                df = df.drop(d, axis=1)

    feature_names.remove(target_name)

    target_names = list(df[target_name].unique())

    meta = {
        'target_names': target_names,
        'names': list(df.columns),
        'feature_names': feature_names,
        'categorical_data': {
            column: list(df[column].unique())
            for column in df.columns
            if df[column].dtype == 'object'
        },
    }

    with open(meta_fp, 'w') as f:
        json.dump(meta, f, indent=2)

    return meta, df, feature_names


def label_encoder(ds, target_name):

    encoders = dict()
    raw_data = dict()

    for x in ds.categorical_data:
        log().info("encoding column: {}".format(x))
        if x == target_name:
            encoder = LabelEncoder()
            encoder.fit(ds.target)
            encoders[x] = encoder
            transformed_data = encoder.transform(ds.target)
            raw_data[x] = ds.target
            ds.target = transformed_data
        else:
            encoder = LabelEncoder()
            encoder.fit(ds.data[x])
            encoders[x] = encoder
            transformed_data = encoder.transform(ds.data[x])
            raw_data[x] = ds.data[x]
            ds.data = ds.data.drop(x, 1)
            ds.data[x] = transformed_data

    ds['encoders'] = encoders
    ds['raw_data'] = raw_data


def create_dataset(df, meta, target_name, readme):

    column_names = list(df.columns)
    # Return the bunch with the appropriate data
    ds = Bunch(
        data=df[column_names[:-1]],
        target=df[column_names[-1]],
        target_names=meta['target_names'],
        feature_names=meta['feature_names'],
        categorical_data=meta['categorical_data'],
        target_name=target_name,
        DESCR=readme)

    return ds


def check_filter(discard, target):

    filtered = list(discard)

    if target in discard:
        filtered.remove(target)

    for d in filtered:
        log().info("discard: {}".format(d))

    log().info("target: {}".format(target))

    return filtered


def load(data_fp, discard, target_name, readme_fp=None):

    filtered = check_filter(discard, target_name)

    meta_fp = data_fp + ".meta"
    meta, df, feature_names = create_metadata(data_fp, meta_fp, filtered, target_name)

    # Load the readme information
    if readme_fp is not None:
        with open(readme_fp, 'r') as f:
            readme = f.read()
    else:
        readme = "NO README"

    return create_dataset(df, meta, target_name, readme)


def load_encoded(data_fp, discard, target_name, readme_fp=None):
    ds = load(data_fp, discard, target_name, readme_fp)
    label_encoder(ds, target_name)
    return ds


def main():
    # load raw dataset

    data_fp = "../data/features/pure_classified/features.csv"
    discard = cfg.onehot_targets
    target_name = cfg.onehot_targets[0]
    ds = load_encoded(data_fp, discard, target_name)

    # store the feature matrix (X) and response vector (y)
    X = ds.data
    y = ds.target

    # store the feature and target names
    feature_names = ds.feature_names
    target_names = ds.target_names

    # printing features and target names of our dataset
    print("Feature names:", feature_names)
    print("Target names:", target_names)

    print("\nType of X is:", type(X))  # should be <class 'pandas.core.frame.DataFrame'>
    print("\nType of y is:", type(y))  # should be <class 'numpy.ndarray'>

    # printing first 5 input rows
    print("\nFirst 5 rows of X:\n", X[:5])

    print("\nFirst 5 rows of y:\n", y[:5])

    # load scaled dataset

    data_fp = "../data/features/scaled_classified/features.csv"

    ds = load_encoded(data_fp, discard, target_name)

    # store the feature matrix (X) and response vector (y)
    X = ds.data
    y = ds.target

    # store the feature and target names
    feature_names = ds.feature_names
    target_names = ds.target_names

    # printing features and target names of our dataset
    print("Feature names:", feature_names)
    print("Target names:", target_names)

    # X and y are numpy arrays
    print("\nType of X is:", type(X))  # should be <class 'pandas.core.frame.DataFrame'>
    print("\nType of y is:", type(y))  # should be <class 'numpy.ndarray'>

    # printing first 5 input rows
    print("\nFirst 5 rows of X:\n", X[:5])

    print("\nFirst 5 rows of y:\n", y[:5])


if __name__ == "__main__":
    main()
