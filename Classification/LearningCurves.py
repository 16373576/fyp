from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.svm import LinearSVC
import pandas as pd
from sklearn import tree, metrics
from matplotlib import pyplot


def main():
    # read in the .csv file and shuffle
    df = pd.read_csv("C:/Users/caire/Desktop/OutputData/OutputHtmlExcel/outputContentAnalysisNormalized.csv",
                     header=0, delimiter=",")
    df = df.sample(frac=1)

    # # find the attributes with the highest correlation to the class
    cor = df.corr(method='pearson')
    cor_target = abs(cor["Reliability"])
    relevant_features = cor_target[cor_target > 0.13]
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
    instance = []

    # used to track how many more instances may exist
    print(len(training))

    # get data for learning curves and save to file to be used in excel
    for instances in range(11, len(training), 1502):
        print(instances)
        instance.append(instances)
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

    # plot the roc curve for the model
    pyplot.plot(instance, knn_learningCurve_accuracy, marker='.', label='KNN')
    pyplot.plot(instance, lsvm_learningCurve_accuracy, marker='.', label='LSVM')
    pyplot.plot(instance, clf_learningCurve_accuracy, marker='.', label='CART')
    pyplot.plot(instance, naive_learningCurve_accuracy, marker='.', label='Naive Bayes')
    pyplot.plot(instance, logReg_learningCurve_accuracy, marker='.', label='Logistic Regression')

    # axis labels
    pyplot.title('Learning curve')
    pyplot.xlabel('Number of Training instances')
    pyplot.ylabel('Accuracy (%)')
    # show the legend
    pyplot.legend()
    axes = pyplot.gca()
    axes.set_ylim([0, 100])
    pyplot.savefig('learningCurve.png', bbox_inches='tight')
    # show the plot
    pyplot.show()

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
