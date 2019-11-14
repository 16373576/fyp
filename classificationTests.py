from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC
import pandas as pd


def main():
    df = pd.read_csv('C:/Users/caire/OneDrive/Documents/forth yr semester 1/Final Year Project/HTMLTagsFrequency.csv',
                     header=0, delimiter=",")
    data = df.values[:, :305]
    labels = df.values[:, 307]

    knn = KNeighborsClassifier(n_neighbors=5)
    lsvm = LinearSVC()

    # Applies KNN and LSVM algorithms to data, then checks the results using 10 fold cross-validation
    cross_validation_test(knn, "KNN", data, labels)
    cross_validation_test(lsvm, "LSVM", data, labels)


# checks the results of the algorithms using 10-fold cross-validation and prints out the results
def cross_validation_test(algorithm, algorithm_name, data, results):
    scores = cross_val_score(algorithm, data, results, cv=10)
    print(algorithm_name + ":\n" + str(scores))
    print("Accuracy: {:0.4} (+/- {:0.3})\n".format(scores.mean(), scores.std() * 2))


main()
