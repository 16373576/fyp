from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.svm import LinearSVC
import pandas as pd
from sklearn import tree, metrics


def main():
    # read in the .csv file and shuffle
    df = pd.read_csv('C:/Users/caire/OneDrive/Documents/forth yr semester 1/Final Year Project/HTMLTagsIndividualArticles2Normalized.csv',
                     header=0, delimiter=",")
    df = df.sample(frac=1)

    # assign the column "Reliability" as the labels
    labels = df["Reliability"]

    # find the attributes with teh highest correlation to the class
    cor = df.corr(method='pearson')
    cor_target = abs(cor["Reliability"])
    relevant_features = cor_target[cor_target > 0.3]
    print(relevant_features)
    data = df[[relevant_features.index[0], relevant_features.index[1], relevant_features.index[2],
               relevant_features.index[3], relevant_features.index[4], 'Reliability']]

    # split into training and test datasets
    train_split = int((len(data) * 2) / 3)
    training = data.values[0:train_split]
    test = data.values[train_split - 1:]

    # initialise variables
    lsvm_learningCurve_accuracy = []
    knn_learningCurve_accuracy = []
    clf_learningCurve_accuracy = []
    naive_learningCurve_accuracy = []
    logReg_learningCurve_accuracy = []

    # used to track how many more instances may exist
    print(len(training))

    # get data for learning curves and save to file to be used in excel
    for instances in range(11, len(training), 502):
        print(instances)
        knn = KNeighborsClassifier(n_neighbors=11)
        knn.fit(training[0:instances, :4], training[0:instances, 5])
        knn_test_predictions = knn.predict(test[:, :4])
        knn_learningCurve_accuracy.append((metrics.accuracy_score(test[:, -1], knn_test_predictions)) * 100)

        lsvm = LinearSVC()
        lsvm.fit(training[0:instances, :4], training[0:instances, 5])
        lsvm_test_predictions = lsvm.predict(test[:, :4])
        lsvm_learningCurve_accuracy.append((metrics.accuracy_score(test[:, -1], lsvm_test_predictions)) * 100)

        clf = tree.DecisionTreeClassifier()
        clf.fit(training[0:instances, :4], training[0:instances, 5])
        clf_test_predictions = clf.predict(test[:, :4])
        clf_learningCurve_accuracy.append((metrics.accuracy_score(test[:, -1], clf_test_predictions)) * 100)

        naive = GaussianNB()
        naive.fit(training[0:instances, :4], training[0:instances, 5])
        naive_test_predictions = naive.predict(test[:, :4])
        naive_learningCurve_accuracy.append((metrics.accuracy_score(test[:, -1], naive_test_predictions)) * 100)

        logReg = LogisticRegression()
        logReg.fit(training[0:instances, :4], training[0:instances, 5])
        logReg_test_predictions = logReg.predict(test[:, :4])
        logReg_learningCurve_accuracy.append((metrics.accuracy_score(test[:, -1], logReg_test_predictions)) * 100)

    # print the results
    print(lsvm_learningCurve_accuracy)
    print(knn_learningCurve_accuracy)
    print(clf_learningCurve_accuracy)
    print(naive_learningCurve_accuracy)
    print(logReg_learningCurve_accuracy)

    # send results to a .csv file to be used for creating a learning curve
    newFile = open("C:/Users/caire/PycharmProjects/fyp/LearningCurveIndividualArticles2.csv", 'a+')
    newFile.write(str(lsvm_learningCurve_accuracy))
    newFile.write(str(knn_learningCurve_accuracy))
    newFile.write(str(clf_learningCurve_accuracy))
    newFile.write(str(naive_learningCurve_accuracy))
    newFile.write(str(logReg_learningCurve_accuracy))
    newFile.close()

    # print the confusion matrix and classification report for the algorithms
    print_confusion_matrix_and_report("KNN", test, knn_test_predictions)
    print_confusion_matrix_and_report("LSVM", test, lsvm_test_predictions)
    print_confusion_matrix_and_report("CART", test, clf_test_predictions)
    print_confusion_matrix_and_report("Naive", test, naive_test_predictions)
    print_confusion_matrix_and_report("Logistic Regression", test, logReg_test_predictions)


def print_confusion_matrix_and_report(algorithmName, test, algorithmPredictions):
    print(algorithmName)
    print(confusion_matrix(test[:, -1], algorithmPredictions))
    print(classification_report(test[:, -1], algorithmPredictions))


main()
