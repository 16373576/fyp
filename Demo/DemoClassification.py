from sklearn.model_selection import cross_val_score
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

    # assign the labels as the Reliability column
    labels = df["Reliability"]

    # conduct feature selection so the algorithms will run faster as now only the 5 most related attributes are used
    data = feature_selection(df)

    # initialise the algorithms and fit to the data
    lsvm = LinearSVC()
    clf = tree.DecisionTreeClassifier()
    clf.fit(data, labels)
    naive = GaussianNB()
    naive.fit(data, labels)
    logReg = LogisticRegression()
    logReg.fit(data, labels)

    # split into training and test datasets
    train_split = int((len(data) - 1))
    training = data.values[0:train_split]
    test = data.values[train_split:]

    knn = KNeighborsClassifier(n_neighbors=11)
    knn.fit(training[:, :4], training[:, 5])
    knn_test_predictions = knn.predict(test[:, :4])
    print(knn_test_predictions)
    print(test[:, 5])


# method to find the attributes with highest correlation to the class
def feature_selection(dataframe):
    cor = dataframe.corr(method='pearson')
    cor_target = abs(cor["Reliability"])
    relevant_features = cor_target[cor_target > 0.2826]
    print(relevant_features)
    data = dataframe[[relevant_features.index[0], relevant_features.index[1], relevant_features.index[2],
                      relevant_features.index[3], relevant_features.index[4], 'Reliability']]

    return data


main()
