#!/usr/bin/env python3

import logging
import os
import datetime
import traceback
from timeit import default_timer as timer

from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.metrics import confusion_matrix
import pandas as pd
import numpy as np

# models
import models

# data
import datasets
import cfg

# local utilities
import stats
import graphs


# -----------------------------------------------------------

def tostrlist(v):
    a = np.array([str(e) for e in v])
    return list(a)


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


class Trainalyser:  # because it trains and analyses...

    def __init__(self, working_folder, ds):
        self.working_folder = working_folder
        self.ds = ds

        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.y_predict = None
        self.classification_report = None
        self.accuracy_score = None

        self.errors = []
        self.num_errors = 0

        log().info("------------------------ NEW CLASSIFIER ---------------------------------")

    def on_err(self, err, note=None):
        if note is not None:
            self.errors.append(note)
            log().error(note)
        self.errors.append(err)
        log().error(err)
        self.num_errors = self.num_errors + 1

    def split(self, splitter=train_test_split, test_size=0.33):
        log().info(
            "splitting data into train/test %0.2f/%0.2f using splitter: '%s'",
            1.0 - test_size,
            test_size,
            splitter.__name__)

        self.X_train, self.X_test, self.y_train, self.y_test = splitter(self.ds.data, self.ds.target)

    def train(self, model):
        start = timer()
        model.fit(self.X_train, self.y_train)
        elapsed = timer() - start
        log().info("train: took %.2fs", elapsed)

    def test(self, model):
        start = timer()
        self.y_predict = model.predict(self.X_test)
        elapsed = timer() - start
        log().info("test: took %.2fs", elapsed)

    def eval(self, classifier, splitter):
        start = timer()
        scores = cross_val_score(classifier, self.ds.data, self.ds.target, cv=splitter)
        elapsed = timer() - start
        log().info("eval: took %.2fs", elapsed)

        log().info(scores)
        log().info("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
        log().info("")

    def target_names(self):
        if hasattr(self.ds, 'target_names'):
            return np.array([str(e) for e in self.ds.target_names])

        return None

    def assess(self):
        tn = self.target_names()
        if tn is not None:
            self.classification_report = metrics.classification_report(
                self.y_test,
                self.y_predict,
                target_names=tn)
            self.accuracy_score = metrics.accuracy_score(self.y_test, self.y_predict)
        else:
            log().info('assess() not run, no target names in data store')

    def report(self):
        log().info("------------------------- START REPORT ----------------------------------")

        df = self.classification_report_dataframe()
        df.to_csv(self.working_folder / 'classification_report.csv', index=False)

        log().info('classification report:\n%s', self.classification_report)
        log().info('accuracy score: %f', self.accuracy_score)

        # check for encoders
        if hasattr(self.ds, 'encoders'):
            test = list(self.ds.encoders[self.ds.target_name].inverse_transform(self.y_test))
            predict = list(self.ds.encoders[self.ds.target_name].inverse_transform(self.y_predict))
            stats.report(test, predict, self.ds.target_names, log())
        else:
            tn = self.target_names()
            if tn is not None:
                stats.report(self.y_test, self.y_predict, tn, log())
            else:
                log().info('stats.report() not run, no target names in data store')

        log().info("-------------------------- END REPORT -----------------------------------")

    def classification_report_dataframe(self):
        report_data = []
        lines = self.classification_report.split('\n')
        for line in lines[2:-3]:
            row = {}
            row_data = line.split()
            row['class'] = row_data[0]
            row['precision'] = row_data[1]
            row['recall'] = row_data[2]
            row['f1-score'] = row_data[3]
            row['support'] = row_data[4]
            report_data.append(row)
        return pd.DataFrame.from_dict(report_data)

    def graph(self):
        tn = self.target_names()
        if tn is not None:
            cm = confusion_matrix(tostrlist(self.y_test), tostrlist(self.y_predict))
            graphs.plot_cm(cm, tn, self.working_folder)
        else:
            log().info('graph() not run, no target names in data store')


# -----------------------------------------------------------


def train_and_evaluate(mm, features_id, target_name):
    feat_fp = cfg.ensure_fp(cfg.features_root + features_id, cfg.features)
    model_path = cfg.ensure_path(cfg.models_root + "/" + features_id)

    working_folder = cfg.ensure_path(model_path / mm.name)
    ds = datasets.from_csv_with_target_names(feat_fp, cfg.onehot_targets, target_name)

    analyser = Trainalyser(working_folder, ds)

    log().info("target: {}".format(target_name))
    log().info("features id: {}".format(features_id))
    log().info("model name: {}".format(mm.name))
    log().info("model description: {}".format(mm.description))

    try:
        analyser.split()
    except:
        log().error('analyser.split()')
        log().error(traceback.format_exc())
        return analyser

    try:
        analyser.train(mm.model)
    except:
        log().error('analyser.train(mm.model)')
        log().error(traceback.format_exc())
        return analyser

    try:
        analyser.test(mm.model)
    except:
        log().error('analyser.test(mm.model)')
        log().error(traceback.format_exc())
        return analyser

    try:
        analyser.assess()
    except:
        log().error('analyser.assess()')
        log().error(traceback.format_exc())
        return analyser

    try:
        analyser.report()
    except:
        log().error('analyser.report()')
        log().error(traceback.format_exc())
        return analyser

    try:
        analyser.graph()
    except:
        log().error('analyser.graph()')
        log().error(traceback.format_exc())
        return analyser

    mm.save(working_folder)

    return analyser


def make_features_fp(features_class):
    fp = cfg.ensure_fp(cfg.features_root + features_class, cfg.features)
    return fp


def train_and_evaluate_all():
    for mm in models.generate():
        for features_class in cfg.features_classes:
            for features_filter in cfg.features_filters:
                target_name = features_filter[1][-1]

                features_id = features_class + '_' + features_filter[0]

                tr = train_and_evaluate(mm, features_id, target_name)
                if tr.num_errors > 0:
                    log().info('=========================================================================')
                    log().info('========================= ERROR SUMMARY =================================')
                    for err in tr.errors:
                        log().Info(err)
                    log().info('=========================================================================')
                    log().info('')


def main():
    train_and_evaluate_all()


if __name__ == "__main__":
    main()

