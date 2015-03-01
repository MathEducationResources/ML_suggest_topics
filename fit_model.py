import numpy as np
from sklearn.multiclass import OneVsRestClassifier
#from sklearn.multiclass import OneVsOneClassifier
from sklearn.svm import SVC
#from sklearn.svm import LinearSVC
from sklearn.cross_validation import train_test_split
#from sklearn.neural_network import BernoulliRBM
#from sklearn.ensemble import RandomForestClassifier
#from sklearn.neighbors import NearestNeighbors
#from sklearn.naive_bayes import GaussianNB
#from sklearn.linear_model import LogisticRegression
#from sklearn.lda import LDA
from sklearn.metrics import classification_report
import pickle


def load_train_test_data(test_size=0.0):
    X = np.genfromtxt("X_data.csv", delimiter=',')
    y = np.genfromtxt("Y_data.csv", delimiter=',')

    X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                        test_size=test_size)
    return (X_train.astype(int),
            X_test.astype(int),
            y_train.astype(int),
            y_test.astype(int))


def print_classification_report(clf, X_test, y_test):
    print(classification_report(clf.predict(X_test), y_test))


if __name__ == '__main__':
    X_train, X_test, y_train, y_test = load_train_test_data(test_size=0.0)
    clf = OneVsRestClassifier(
        SVC(kernel='linear', class_weight='auto', probability=True))
    clf.fit(X_train, y_train)
    pickle.dump(clf, open("classifier.bin", "wb"))
    print_classification_report(clf, X_test, y_test)
