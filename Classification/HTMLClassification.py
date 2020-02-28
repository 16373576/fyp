from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
import pandas as pd
from sklearn import tree


def main():
    # read in the data from the .csv file and shuffle
    df = pd.read_csv(
        "C:/Users/caire/Desktop/OutputData/OutputHtmlExcel/outputContentAnalysisNormalized.csv",
        header=0, delimiter=",")
    df = df.sample(frac=1)

    # assign the labels as the Reliability column
    labels = df["Reliability"]

    # conduct feature selection so the algorithms will run faster as now only the 5 most related attributes are used
    data = feature_selection(df)
    # data = df[["Article wc", "Title wc", "Article Pos Sentiment", "Article Neu Sentiment", "Article Neg Sentiment",
    #             "Article Compound Sentiment", "Title Pos Sentiment", "Title Neu Sentiment", "Title Neg Sentiment",
    #             "Title Compound Sentiment", "Article Bias wc", "Title Bias wc", "Article Stopword wc", "Title Stopword wc",
    #             "Article Exclamation Count", "Article Cap Count", "Article Number Count", "Article Question Count",
    #             "Article Comma Count", "Article Quote Count", "Title Exclamation Count", "Title Cap Count",
    #             "Title Number Count", "Title Question Count", "Title Comma Count", "Title Quote Count"]]

    # initialise the algorithms and fit to the data
    knn = KNeighborsClassifier(n_neighbors=11)
    lsvm = LinearSVC()
    clf = tree.DecisionTreeClassifier()
    clf.fit(data, labels)
    naive = GaussianNB()
    naive.fit(data, labels)
    logReg = LogisticRegression()
    logReg.fit(data, labels)

    # run 10 fold cross-validation
    cross_validation_test(knn, "KNN", data, labels)
    cross_validation_test(lsvm, "LSVM", data, labels)
    cross_validation_test(clf, "CART", data, labels)
    cross_validation_test(naive, "Naive Bayes Model", data, labels)
    cross_validation_test(logReg, "logistic regression", data, labels)


# checks the results of the algorithms using 10-fold cross-validation and prints out the results
def cross_validation_test(algorithm, algorithm_name, data, results):
    scores = cross_val_score(algorithm, data, results, cv=10)
    print(algorithm_name + ":\n" + str(scores))
    print("Accuracy: {:0.4} (+/- {:0.3})\n".format(scores.mean(), scores.std() * 2))


# method to find the attributes with highest correlation to the class
def feature_selection(dataframe):
    cor = dataframe.corr(method='pearson')
    cor_target = abs(cor["Reliability"])
    relevant_features = cor_target[cor_target > 0.13]
    print(relevant_features)
    data = dataframe[[relevant_features.index[0], relevant_features.index[1], relevant_features.index[2],
                      relevant_features.index[3], relevant_features.index[4]]]
    return data


main()
