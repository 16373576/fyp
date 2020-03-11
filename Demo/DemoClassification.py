import warnings

import numpy as np
import json
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
import pandas as pd
from sklearn import tree


def main():
    # read in the data from the .csv file and shuffle
    df = pd.read_csv("C:/Users/caire/Desktop/OutputData/OutputHtmlExcel/HTMLTagsNormalizedCombined.csv",
                     header=0, delimiter=",")
    df = df.sample(frac=1)
    df['Title'].astype('str')
    df['URL'].astype('str')

    # conduct feature selection so the algorithms will run faster as now only the 5 most related attributes are used
    data = feature_selection(df)

    # initialise the algorithms and fit to the data
    # lsvm = LinearSVC()
    # clf = tree.DecisionTreeClassifier()
    # clf.fit(data, labels)
    # naive = GaussianNB()
    # naive.fit(data, labels)
    # logReg = LogisticRegression()
    # logReg.fit(data, labels)

    # split into training and test datasets
    train_split = int((len(data) - 1))
    training = data.values[0:train_split]
    test = data.values[train_split:]
    Y = training[:, 5]
    Y = Y.astype('int')

    title = test[:, 6]
    url = test[:, 7]
    print("\n" + title[0])
    print(url[0])

    if test[:, 5] == 1:
        print("Actual Class: Unreliable\n")
    else:
        print("Actual Class: Reliable\n")

    knn = KNeighborsClassifier(n_neighbors=11)
    knn.fit(training[:, :4], Y)
    knn_test_predictions = knn.predict(test[:, :4])
    if knn_test_predictions == 1:
        print("KNN Prediction: Unreliable")
    else:
        print("KNN Prediction: Reliable")

    lsvm = LinearSVC(dual=False)
    lsvm.fit(training[:, :4], Y)
    lsvm_test_predictions = lsvm.predict(test[:, :4])
    if lsvm_test_predictions == 1:
        print("LSVM Prediction: Unreliable")
    else:
        print("LSVM Prediction: Reliable")

    clf = tree.DecisionTreeClassifier()
    clf.fit(training[:, :4], Y)
    clf_test_predictions = clf.predict(test[:, :4])
    if clf_test_predictions == 1:
        print("CART Prediction: Unreliable")
    else:
        print("CART Prediction: Reliable")

    naive = GaussianNB()
    naive.fit(training[:, :4], Y)
    naive_test_predictions = naive.predict(test[:, :4])
    if naive_test_predictions == 1:
        print("Naive Bayes Prediction: Unreliable")
    else:
        print("Naive Bayes Prediction: Reliable")

    # run block of code and catch warnings
    with warnings.catch_warnings():
        # ignore all caught warnings
        warnings.filterwarnings("ignore")
        # execute code that will generate warnings
        logReg = LogisticRegression()
        logReg.fit(training[:, :4], Y)
        logReg_test_predictions = logReg.predict(test[:, :4])
        if logReg_test_predictions == 1:
            print("Logistic Regression Prediction: Unreliable")
        else:
            print("Logistic Regression Prediction: Reliable")


# method to find the attributes with highest correlation to the class
def feature_selection(df):
    cor = df.corr(method='pearson')
    cor_target = abs(cor["Reliability"])
    relevant_features = cor_target[cor_target > 0.2825]
    columns = [relevant_features.index[0], relevant_features.index[1], relevant_features.index[2],
               relevant_features.index[3], relevant_features.index[4], 'Reliability', 'Title', 'URL']
    df1 = pd.DataFrame(df, columns=columns)
    return df1


main()
