from tracking.WorkoutClass import workout
from statistics import mean
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.exceptions import NotFittedError
from time import time


def calculate_euclidean_distance(keypoints1, keypoints2):
    # Calculate Euclidean distance between two sets of keypoints
    return np.linalg.norm(keypoints1 - keypoints2)

# Assuming dataset is your dataset loaded from the npy file
def calculate_distance(realtime_keypoints, dataset):
    min_distance = float('inf')
    closest_point = None

    # Iterate through dataset
    for data_point in dataset:
        # Calculate distance between each dataset point and real-time keypoints
        distance = calculate_euclidean_distance(realtime_keypoints, data_point)
        # Check if this distance is smaller than previous min_distance
        if distance < min_distance:
            min_distance = distance
            closest_point = data_point

    return min_distance, closest_point

with open('best_svm_model.pkl', 'rb') as f:
    loaded_model = pickle.load(f)
    
scaler = StandardScaler()


curl = workout(side=True, front=False)

curl.setupCamera()

# If you are doing from side
curl.excludeLandmarks(rightArm=False)
angles = []
buffer = 0


running = True
curlUp = False

start_time = time()

rep = 0

while running:
    curl.oneFrame()


    try:
        shoulder, wrist, elbow = curl.returnPoints()
        angle = curl.curl()
        
        realtime_features = np.array(angles)
        scaler.fit(realtime_features)
        realtime_features = scaler.transform(realtime_features)

        # Reshape for SVM model (assuming 1 sample)
        realtime_features_reshaped = realtime_features.reshape(1, -1)
        print(realtime_features_reshaped)

        # Scale features if used during training
        realtime_features_scaled = scaler.transform(realtime_features_reshaped)

        # Make prediction using the loaded SVM model
        predicted_class = loaded_model.predict(realtime_features_scaled)[0]
        
        print(predicted_class)
    except Exception as f:
        print(f)
        
    

    if buffer < 3:
        angles.append(angle)
        buffer += 1
        #print(angles)
        
    if buffer >= 3:
        
        if mean(angles) > angles[0]:
            print("Down")
        else:
            print("Up")
        
        angles = []
        buffer = 0
    
    if angle <= 35.0 and not curlUp:
        rep += 1
        curlUp = True
    elif angle >= 160 and curlUp:
        curlUp = False
    
    print(f"Your on rep: {rep}")