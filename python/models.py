from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
# from sklearn.svm import SVC
# from sklearn.gaussian_process import GaussianProcessClassifier
# from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.pipeline import make_pipeline
from sklearn.decomposition import PCA
from sklearn.externals import joblib

classifiers = [
    ['KNN', KNeighborsClassifier(3)],
    ['NeuralNet', MLPClassifier(alpha=1)],

    ['MLP_7_7_7', MLPClassifier(hidden_layer_sizes=(7, 7, 7), max_iter=500)],
    # locks up? #['LinearSVM', SVC(kernel="linear", C=0.025)],
    # locks up? ['RBFSVM', SVC(gamma=2, C=1)],
    # crashes ['GaussianProcess', GaussianProcessClassifier(1.0 * RBF(1.0))],
    
    ['DecisionTree', DecisionTreeClassifier(max_depth=5)],
    ['RandomForest', RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1)],
    ['AdaBoost', AdaBoostClassifier()],
    ['NaiveBayes', GaussianNB()],
    ['QDA', QuadraticDiscriminantAnalysis()]
]


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

def generate():
    npca = [0, 2, 3, 7]
    for name, clf in classifiers:
        for n in npca:
            if n != 0:
                pca = PCA(n_components=n)
                model = make_pipeline(pca, clf)
                mmname = name + '_' + 'PCA{}'.format(n)
                description = mmname
            else:
                model = make_pipeline(clf)
                mmname = name
                description = name
            mm = MetaModel(model, mmname, description)
            yield mm

def create(features_class):

    # TODO generator

    classifier = MLPClassifier(hidden_layer_sizes=(7, 7, 7), max_iter=500)
    pca5 = PCA(n_components=5)
    description = "+ PCA(n_components=5)" \
                  " + MLPClassifier(hidden_layer_sizes=(7, 7, 7), max_iter=500)"
    name = "mlp_classifier_7_7_7_pca_5"
    model = make_pipeline(pca5, classifier)

    mm = MetaModel(model, name, description)
    return mm
