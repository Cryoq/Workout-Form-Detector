from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score
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

# Create MLP classifier (basic architecture)
clf = MLPClassifier(solver='lbfgs', alpha=0.01, hidden_layer_sizes=(100,), random_state=42, max_iter=5000)
# Train the model
clf.fit(X_train, y_train)  # Use X_train and y_train directly (no scaling in this example)

# Save the trained model to a file (optional)
# with open('mlp_model.pkl', 'wb') as file:
#     pickle.dump(clf, file)

# Evaluate model performance
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# Print classification report for more detailed evaluation
print(classification_report(y_test, y_pred))

# Cross-validation for robust evaluation
cv_scores = cross_val_score(clf, X_train, y_train, cv=5)
print("Cross-Validation Scores:", cv_scores)
print("Mean CV Accuracy:", np.mean(cv_scores))
