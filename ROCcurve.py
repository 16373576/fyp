from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
import pandas as pd
from sklearn import tree
from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score
from matplotlib import pyplot


def main():
    # read in the data and shuffle
    df = pd.read_csv('C:/Users/caire/OneDrive/Documents/forth yr semester 1/Final Year '
                     'Project/HTMLTagsIndividualArticlesNormalizedMinMax.csv', header=0, delimiter=",")
    df = df.sample(frac=1)

    # find the attributes with the highest correlation to the class
    cor = df.corr(method='pearson')
    cor_target = abs(cor["Reliability"])
    relevant_features = cor_target[cor_target > 0.3]
    print(relevant_features)
    data = df[[relevant_features.index[0], relevant_features.index[1], relevant_features.index[2],
               relevant_features.index[3], relevant_features.index[4], 'Reliability']]

    # split the data into training and test data
    train_split = int((len(data) * 2) / 3)
    training = data.values[0:train_split]
    test = data.values[train_split - 1:]

    # fit all models to the data and make predictions
    knn = KNeighborsClassifier(n_neighbors=11)
    lsvm = SVC(kernel="linear", probability=True)
    clf = tree.DecisionTreeClassifier()
    naive = GaussianNB()
    logReg = LogisticRegression()

    # calculate roc curves
    knn_fpr, knn_tpr, _ = roc_curve(test[:, 5], generate_ROC_curve_data(knn, "KNN", training, test))
    lsvm_fpr, lsvm_tpr, _ = roc_curve(test[:, 5], generate_ROC_curve_data(lsvm, "LSVM", training, test))
    clf_fpr, clf_tpr, _ = roc_curve(test[:, 5], generate_ROC_curve_data(clf, "CART", training, test))
    naive_fpr, naive_tpr, _ = roc_curve(test[:, 5], generate_ROC_curve_data(naive, "Naive Bayes", training, test))
    log_fpr, log_tpr, _ = roc_curve(test[:, 5], generate_ROC_curve_data(logReg, "Logistic Regression", training, test))

    # plot the roc curve for the model
    pyplot.plot(knn_fpr, knn_tpr, marker='.', label='KNN')
    pyplot.plot(lsvm_fpr, lsvm_tpr, marker='.', label='LSVM')
    pyplot.plot(clf_fpr, clf_tpr, marker='.', label='CART')
    pyplot.plot(naive_fpr, naive_tpr, marker='.', label='Naive Bayes')
    pyplot.plot(log_fpr, log_tpr, marker='.', label='Logistic Regression')

    # axis labels
    pyplot.title('ROC curve')
    pyplot.xlabel('False Positive Rate')
    pyplot.ylabel('True Positive Rate')
    # show the legend
    pyplot.legend()
    pyplot.savefig('ROCcurve.png', bbox_inches='tight')
    # show the plot
    pyplot.show()


def generate_ROC_curve_data(algorithm, algorithmName, training, test):
    # fit the model and make predictions
    algorithm.fit(training[:, :4], training[:, 5])
    algorithm_test_predictions = algorithm.predict_proba(test[:, :4])

    # keep probabilities for the positive outcome only
    algorithm_test_predictions = algorithm_test_predictions[:, 1]

    # calculate and print the ROC AUC scores
    algorithm_auc = roc_auc_score(test[:, 5], algorithm_test_predictions)
    print(algorithmName + ': ROC AUC=%.3f' % algorithm_auc)

    # return predictions to be plotted in the curve
    return algorithm_test_predictions


main()
