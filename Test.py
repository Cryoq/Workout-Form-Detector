from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.metrics import accuracy_score, classification_report
import numpy as np
import pickle

# Load data
good_curl_data = np.load("data/TimeGoodLeftCurl.npy")
bad_curl_data = np.load("data/TimeBadLeftCurl.npy")

# Concatenate data and create labels
X = np.concatenate((good_curl_data, bad_curl_data), axis=0)
y = np.array(['Good Curl'] * len(good_curl_data) + ['Bad Curl'] * len(bad_curl_data))

# Flatten data if needed
if len(X.shape) == 3:
    X = X.reshape(X.shape[0], -1)
print(X)

# Split dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, random_state=42)

# Normalize input features (optional, comment out if not needed)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Define parameter grid for GridSearchCV
param_grid = {'C': [0.01, 0.1, 1, 10], 'kernel': ['linear', 'rbf']}

# Create SVC classifier with GridSearchCV
clf = GridSearchCV(SVC(random_state=42), param_grid, cv=5, refit=True)

# Train the model with grid search
clf.fit(X_train_scaled, y_train)

# Get the best model and its parameters
best_model = clf.best_estimator_
best_params = clf.best_params_

# Print the best parameters found by GridSearchCV
print("Best Parameters:", best_params)

# Use the best model for prediction and evaluation on test set
y_pred = best_model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy with best parameters:", accuracy)

# Print classification report for more detailed evaluation
print(classification_report(y_test, y_pred))

# Cross-validation for robust evaluation (using best model)
cv_scores = cross_val_score(best_model, X_train_scaled, y_train, cv=5)
print("Cross-Validation Scores:", cv_scores)
print("Mean CV Accuracy:", np.mean(cv_scores))

with open('best_svm_model.pkl', 'wb') as file:
    pickle.dump(clf.best_estimator_, file)
