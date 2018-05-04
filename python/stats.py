#!/usr/bin/env python3

from collections import Counter
from nltk.metrics import ConfusionMatrix
import logging
import numpy as np
import pandas as pd
import cfg


def report(xexpected, xpredicted, xlabels, log):
    xxx = np.array([str(e) for e in xexpected])
    yyy = np.array([str(e) for e in xpredicted])
    zzz = np.array([str(e) for e in xlabels])

    expected = list(xxx)
    predicted = list(yyy)
    labels = list(zzz)

    cm = ConfusionMatrix(expected, predicted)
    log.info("Confusion matrix:")
    log.info("\n%s", cm)
    log.info("Confusion matrix: sorted by count")
    log.info("\n%s", cm.pretty_format(sort_by_count=True))

    # merge expected & predicted, & get unique values
    all_labels = set(expected + predicted)

    true_positives = Counter()
    false_negatives = Counter()
    false_positives = Counter()

    for i in all_labels:
        for j in all_labels:
            if i == j:
                true_positives[i] += cm[i, j]
            else:
                false_negatives[i] += cm[i, j]
                false_positives[j] += cm[i, j]

    sb = ''
    for value, count in true_positives.most_common():
        s = '{0}={1}, '.format(value, count)
        sb += s
    log.info("True Positives (%d): %s\n", sum(true_positives.values()), sb)

    sb = ''
    for value, count in false_negatives.most_common():
        s = '{0}={1}, '.format(value, count)
        sb += s
    log.info("False Negatives (%d): %s\n", sum(false_negatives.values()), sb)

    sb = ''
    for value, count in false_positives.most_common():
        s = '{0}={1}, '.format(value, count)
        sb += s
    log.info("False Positives (%d): %s\n", sum(false_positives.values()), sb)

    sb = ''
    last = len(all_labels) - 1
    for i, x in enumerate(sorted(all_labels)):
        if true_positives[x] == 0:
            fscore = 0
        else:
            precision = true_positives[x] / float(true_positives[x] + false_positives[x])
            recall = true_positives[x] / float(true_positives[x] + false_negatives[x])
            fscore = 2 * (precision * recall) / float(precision + recall)

        if i != last:
            sb += '{0}={1}, '.format(x, fscore)
        else:
            sb += '{0}={1}'.format(x, fscore)

    # log.info('F Scores: {0}\n'.format(sb))

    untested_labels = set(labels) - all_labels

    if len(untested_labels):
        log.info('Untested: {0}\n'.format(list(untested_labels)))

    log.info('#expected: {}, #predicted: {}, #labels: {}'.format(len(expected), len(predicted), len(labels)))
    log.info('labels: {}'.format(labels))
    log.info('')


def targets_info(fp):
    data = pd.read_csv(fp)
    print('targets information from: {}'.format(fp))
    for t in cfg.onehot_targets:
        print(t)
        print('val  count')
        print(data[t].value_counts())
        print()


def test_cm():
    expected = 'DET NN VB DET JJ NN NN IN DET NN DET NN VB DET JJ NN NN IN DET NN'.split()
    predicted = 'DET VB VB DET NN NN NN IN DET NN DET NN NN DET NN NN NN IN DET NN'.split()
    labels = 'DET NN VB IN JJ'.split()
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()
    report(expected, predicted, labels, logger)


def test_targets_info():
    targets_info('../data/observations/observations.csv')


if __name__ == "__main__":
    # test_cm()
    test_targets_info()
