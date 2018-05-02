from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.decomposition import PCA
from sklearn.externals import joblib
import cfg


class MetaModel:
    def __init__(self, model, name, description):
        self.model = model
        self.name = name
        self.description = description

    def save(self, folder):
        with open(meta_fp(folder), 'w') as handle:
            handle.write("{}\n".format(self.name))
            handle.write("{}\n".format(self.description))
        joblib.dump(self.model, model_fp(folder))


def meta_fp(folder):
    return str(folder) + "/model.txt"


def model_fp(folder):
    return str(folder) + "/model.pickle"


def load(folder):
    with open(meta_fp(folder), 'r') as handle:
        name = handle.readline()
        description = handle.readline()
        model = joblib.load(model_fp(folder))

    return MetaModel(model, name, description)


def create(features_class):

    # TODO generator

    compatible = False
    if features_class in cfg.classification_compatible:
        compatible = True

    if not compatible:
        return None

    classifier = MLPClassifier(hidden_layer_sizes=(7, 7, 7), max_iter=500)
    pca5 = PCA(n_components=5)
    description = "+ PCA(n_components=5)" \
                  " + MLPClassifier(hidden_layer_sizes=(7, 7, 7), max_iter=500)"
    name = "mlp_classifier_7_7_7_pca_5"
    model = make_pipeline(pca5, classifier)

    mm = MetaModel(model, name, description)
    return mm
