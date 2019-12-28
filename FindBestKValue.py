import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import matplotlib.pyplot as plt

# df = pd.read_csv('C:/Users/caire/OneDrive/Documents/forth yr semester 1/Final Year Project/HTMLTagsFrequency.csv',
#                  header=0, delimiter=",")
df = pd.read_csv(
    'C:/Users/caire/OneDrive/Documents/forth yr semester 1/Final Year Project/HTMLTagsIndividualArticlesNormalized.csv',
    header=0, delimiter=",")

data_before_feature_sel = df.values[:, :305]
cor = df.corr(method='pearson')
cor_target = abs(cor["Reliability"])
relevant_features = cor_target[cor_target > 0.35]
print(relevant_features)
data = df[[relevant_features.index[0], relevant_features.index[1], relevant_features.index[2],
           relevant_features.index[3], relevant_features.index[4], 'Reliability']]

data = data.sample(frac=1)
train_split = int((len(data) * 2) / 3)
training = data.values[0:train_split]
test = data.values[train_split - 1:]

error = []
# Calculating error for K values between 1 and 40
for i in range(1, 200, 10):
    knn = KNeighborsClassifier(n_neighbors=i)
    x = training[:, :4]
    y = training[:, 5]
    y = y.astype('int')
    knn.fit(x, y)
    predictions = knn.predict(test[:, :4])
    error.append(np.mean(predictions != test[:, -1]))

plt.figure(figsize=(12, 6))
plt.plot(range(1, 200, 10), error, color='red', linestyle='dashed', marker='o',
         markerfacecolor='blue', markersize=10)
plt.title('Error Rate K Value')
plt.xlabel('K Value')
plt.ylabel('Mean Error')
plt.show()
