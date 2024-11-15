import pandas as pd
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler

# define the file path
train_path = "C:\\IMSE7143-IoT2024-CW1\\TrainingData.txt"
test_path = "C:\\IMSE7143-IoT2024-CW1\\TestingData.txt"
result_path = "C:\\IMSE7143-IoT2024-CW1\\TestingResults.txt"

# read training data
train_data = pd.read_csv(train_path, delimiter=',', header=None)

# divide features and label
X_train = train_data.iloc[:, :-1]  # the first 24 data is feature.
y_train = train_data.iloc[:, -1]   # the last one is label.

# standardise training data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)

# initiate SVM classifier, set the parameters (retry other parameters)
svm_classifier = SVC(kernel='rbf', C=1.0, gamma='scale', random_state=40)

# train the classifier
svm_classifier.fit(X_train, y_train)

# read the testing data with no label
X_test_original = pd.read_csv(test_path, delimiter=',', header=None)

# use the trained scaler to standardise the testing data
X_test_scaled = scaler.transform(X_test_original)

# predict the testing data
y_pred = svm_classifier.predict(X_test_scaled)

# add the labels to the original test data (not scaled)
test_data_with_predictions = X_test_original.copy()
test_data_with_predictions['Prediction'] = y_pred

# save the result to TestingResults.txt
test_data_with_predictions.to_csv(result_path, header=False, index=False)
print(f"Results are stored in {result_path}")

