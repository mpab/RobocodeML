#!/usr/bin/env python3

import pandas as pd
import cfg


def make_features_fp(features_class):
    fp = cfg.ensure_fp(cfg.features_root + features_class, cfg.features)
    return fp


def diff(first, second):
    second = set(second)
    return [item for item in first if item not in second]


def filter_features_csv():

    for features_class in cfg.features_classes:
        for features_filter in cfg.features_filters:
            feat_fp = make_features_fp(features_class)

            df = pd.read_csv(feat_fp)

            drop_list = diff(cfg.csv_column_names, features_filter[1])

            for d in drop_list:
                df = df.drop(d, axis=1)

            filter_fp = make_features_fp(features_class + '_' + features_filter[0])

            print('saving filtered features file" {}'.format(filter_fp))

            df.to_csv(filter_fp, index=False)


def main():
    filter_features_csv()


if __name__ == "__main__":
    main()
