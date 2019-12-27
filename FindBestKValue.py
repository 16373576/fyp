import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('C:/Users/caire/OneDrive/Documents/forth yr semester 1/Final Year Project/HTMLTagsFrequency.csv',
                 header=0, delimiter=",")
df = df.sample(frac=1)
train_split = int((len(df) * 2) / 3)
training = df.values[0:train_split]
test = df.values[train_split - 1:]

error = []
# Calculating error for K values between 1 and 40
for i in range(1, 40):
    knn = KNeighborsClassifier(n_neighbors=i)
    knn.fit(training[:, :305], training[:, 307])
    predictions = knn.predict(test[:, :305])
    error.append(np.mean(predictions != test[:, -1]))

plt.figure(figsize=(12, 6))
plt.plot(range(1, 40), error, color='red', linestyle='dashed', marker='o',
         markerfacecolor='blue', markersize=10)
plt.title('Error Rate K Value')
plt.xlabel('K Value')
plt.ylabel('Mean Error')
plt.show()