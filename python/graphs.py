#!/usr/bin/env python3

import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn.datasets
import datasets as lds

from pylab import rcParams

rcParams['figure.figsize'] = 12, 12


def plot_hist():
    data = pd.read_csv('../data/features/pure_pure/features.csv', quoting=2)
    data.hist(bins=50)
    plt.xlim([0, 115000])
    plt.title("Data")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.show()


def datasets():
    yield sklearn.datasets.load_boston()
    yield sklearn.datasets.load_breast_cancer()
    yield sklearn.datasets.load_diabetes()
    yield sklearn.datasets.load_digits()
    yield sklearn.datasets.load_iris()
    yield sklearn.datasets.load_linnerud()
    yield lds.load_features_u()
    yield lds.load_features_c()


def plot_cm(cm,
            target_names,
            path,
            normalize=False,
            title='Confusion matrix',
            cmap=plt.cm.Blues, ):
    """
    renders a confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    np.set_printoptions(precision=2)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(target_names))
    plt.xticks(tick_marks, target_names, rotation=45)
    plt.yticks(tick_marks, target_names)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

    # plt.show()

    plt.savefig(str(path) + '/confusion_matrix.png', bbox_inches='tight')


def main():
    # for ds in datasets():
    #    lds.print_info(ds)
    plot_hist()


if __name__ == '__main__':
    main()
