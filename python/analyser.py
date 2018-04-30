#!/usr/bin/env python3

import logging

from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
import datetime
from timeit import default_timer as timer
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.metrics import confusion_matrix
import distutils.dir_util
import pandas as pd

# data
import dataset

# local utilities
import stats
import graphs

# -----------------------------------------------------------


class Analyser():

    def __init__(self, log_path, dataset):
        self.dataset = dataset

        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.y_predict = None
        self.classification_report = None
        self.accuracy_score = None

        self.creation_timestamp = '{:%Y-%m-%d_%H.%M.%S}'.format(datetime.datetime.now())
        self.instance_name = self.creation_timestamp + '_' + type(self).__name__

        self.log = None
        self.log_file_path = log_path + '/' + self.instance_name
        self.get_logger()
        self.log.info("------------------------ NEW CLASSIFIER -----------------------------------")

    def get_logger(self):
        if self.log is None:
            logging.basicConfig(level=logging.INFO)
            logger = logging.getLogger(self.instance_name)
            fh = logging.FileHandler(self.log_file_path + '.log')
            fh.setLevel(logging.INFO)
            logger.addHandler(fh)
            self.log = logger
        return self.log

    def split(self, splitter=train_test_split, test_size=0.33):
        self.log.info(
            "splitting data into train/test %0.2f/%0.2f using splitter: '%s'",
            1.0 - test_size,
            test_size,
            splitter.__name__)

        self.X_train, self.X_test, self.y_train, self.y_test = splitter(self.dataset.data, self.dataset.target)


    def train(self, model):
        start = timer()
        model.fit(self.X_train, self.y_train)
        elapsed = timer() - start
        self.log.info("train: took %.2fs", elapsed)

    def test(self, model):
        start = timer()
        self.y_predict = model.predict(self.X_test)
        elapsed = timer() - start
        self.log.info("test: took %.2fs", elapsed)

    def eval(self, classifier, splitter):
        start = timer()
        scores = cross_val_score(classifier, self.dataset.data, self.dataset.target, cv=splitter)
        elapsed = timer() - start
        self.log.info("eval: took %.2fs", elapsed)

        self.log.info(scores)
        self.log.info("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
        self.log.info("")

    def assess(self):
        self.classification_report = \
            metrics.classification_report(self.y_test, self.y_predict, target_names=self.dataset.target_names)
        self.accuracy_score = metrics.accuracy_score(self.y_test, self.y_predict)

    def report(self):
        self.log.info("------------------------- START REPORT ----------------------------------")

        df = self.classification_report_dataframe()
        df.to_csv(self.log_file_path + '_classification_report.csv', index = False)

        self.log.info('classification report:\n%s', self.classification_report)
        self.log.info('accuracy score: %f', self.accuracy_score)

        test = list(self.dataset.encoders[self.dataset.target_name].inverse_transform(self.y_test))
        predict = list(self.dataset.encoders[self.dataset.target_name].inverse_transform(self.y_predict))

        stats.report(test, predict, self.dataset.target_names, self.log)

        self.log.info("-------------------------- END REPORT -----------------------------------")

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
        cm = confusion_matrix(self.y_test, self.y_predict)
        graphs.plot_cm(cm, self.dataset.target_names, self.log_file_path)

# -----------------------------------------------------------


def main():
    log_path = "../analysis/MLP_005/"
    data_fp = "./qfeatures.csv"

    distutils.dir_util.mkpath(log_path)

    ds, _ = dataset.load(data_fp)

    classifier = MLPClassifier(hidden_layer_sizes=(7, 7, 7), max_iter=500)
    pca5 = PCA(n_components=5)
    pipeline = make_pipeline(pca5, classifier)

    analyser = Analyser(log_path, ds)

    log = analyser.get_logger()
    log.info("MLPClassifier(hidden_layer_sizes=(7, 7, 7), max_iter=500)")
    log.info("no scaling, pca5")

    analyser.split()
    analyser.train(pipeline)
    analyser.test(pipeline)
    analyser.assess()
    analyser.report()
    analyser.graph()


if __name__ == "__main__":
    main()