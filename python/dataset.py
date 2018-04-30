#!/usr/bin/env python3

"""
(c) Michael Alderson-Bythell
RobocodeML dataset helper for scikit-learn
"""

import pandas as pd
import json
from sklearn.datasets.base import Bunch
from sklearn.preprocessing import LabelEncoder

# see here for tips on preparing data
# https://districtdatalabs.silvrback.com/building-a-classifier-from-census-data
# https://bbengfort.github.io/programmer/2016/04/19/bunch-data-management.html

# see here for data wrangling
# http://fastml.com/converting-categorical-data-into-numbers-with-pandas-and-scikit-learn/

# TODO read in the names data from disk and parse/convert to a clean list
csv_column_names = [
    "action",
    "x",
    "y",
    "heading",
    "enemy_distance",
    "enemy_bearing",
    "reward"
]

target_name = "reward"


def read_csv(data_fp):
    #csv = pd.read_csv(data_fp, names=csv_column_names, skiprows=range(1))
    #csv = pd.read_csv(data_fp)
    csv = pd.read_csv(data_fp, names=csv_column_names)
    print(csv.head())
    return csv


def categorise(data_fp, meta_fp):
    # analyse csv & create json metadata file
    csv = read_csv(data_fp)

    feature_names = list(csv.columns)
    feature_names.remove(target_name)

    meta = {
        'target_names': list(csv.reward.unique()),
        'names': list(csv.columns),
        'feature_names': feature_names,
        'categorical_data': {
            column: list(csv[column].unique())
            for column in csv.columns
            if csv[column].dtype == 'object'
        },
    }

    with open(meta_fp, 'w') as f:
        json.dump(meta, f, indent=2)


def encode(ds):

    encoders = dict()
    raw_data = dict()

    for x in ds.categorical_data:
        print("encoding column: {}".format(x))
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


def load(data_fp, readme_fp=None):

    meta_fp = data_fp + ".meta"
    categorise(data_fp, meta_fp)

    # Load the meta data from the file
    with open(meta_fp, 'r') as f:
        meta = json.load(f)

    # Load the readme information
    if readme_fp is not None:
        with open(readme_fp, 'r') as f:
            readme = f.read()
    else:
        readme = "NO README"

    # Load the data
    csv = pd.read_csv(data_fp, names=csv_column_names)

    # Return the bunch with the appropriate data chunked apart
    ds = Bunch(
        data=csv[csv_column_names[:-1]],
        target=csv[csv_column_names[-1]],
        target_names=meta['target_names'],
        feature_names=meta['feature_names'],
        target_name=target_name,
        categorical_data=meta['categorical_data'],
        DESCR=readme)

    encode(ds)
    return ds, meta_fp


def main():
    data_fp = "../data/features/feat_reward_0.csv"
    data_fp = "./features.csv"
    # readme_fp = file_root + "_readme.md"
    ds, meta_fp = load(data_fp)
    #print(ds.keys())
    #with open(meta_fp, 'r') as f:
    #    meta = json.load(f)
    #    print(meta)
    #print(ds.values())

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
    print("\nType of X is:", type(X))

    # printing first 5 input rows
    print("\nFirst 5 rows of X:\n", X[:5])

    print("\nFirst 5 rows of y:\n", y[:5])


if __name__ == "__main__":
    main()
