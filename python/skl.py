#!/usr/bin/env python3


import sklearn.datasets
import datasets as lds


def datasets():
    yield sklearn.datasets.load_boston()
    yield sklearn.datasets.load_breast_cancer()
    yield sklearn.datasets.load_diabetes()
    yield sklearn.datasets.load_digits()
    yield sklearn.datasets.load_iris()
    yield sklearn.datasets.load_linnerud()
    yield lds.load_features_u()
    yield lds.load_features_c()


def main():

    for ds in datasets():
        lds.print_info(ds)


if __name__ == '__main__':
    main()
