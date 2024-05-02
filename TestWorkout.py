from tracking.WorkoutClass import workout
from statistics import mean
import numpy as np

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


leftCurlPoints = np.load("data/leftCurlPoints.npy")

#curl = workout(side=True, front=False)

#curl.setupCamera()

# If you are doing from side
#curl.excludeLandmarks(rightArm=False)
angles = []
buffer = 0

distanceList = []
goodForm = True
okForm = False
badForm = False

maxGoodForm = 0.09
maxOkForm = 0.11


running = True
curlUp = False

rep = 0
'''
while running:
    
    curl.oneFrame()
    
    shoulder, wrist, elbow = curl.returnPoints()
    
# Create a numpy array to represent the keypoints
    realtime_keypoints = np.array([wrist, elbow, shoulder])

    # Example of how to use the functions
    distance, closest_point = calculate_distance(realtime_keypoints, leftCurlPoints)
    
    print("Distance:", distance)

    
    angle = curl.curl()
    if buffer < 3:
        angles.append(angle)
        distanceList.append(distance)
        buffer += 1
    if buffer >= 3:
        if mean(angles) > angles[0]:
            print("Down")
        else:
            print("Up")
        if mean(distanceList) < maxGoodForm:
            goodForm = True
            okForm = False
            badForm = False
        elif mean(distanceList) < maxOkForm:
            goodForm = False
            okForm = True
            badForm = False
        else:
            goodForm = False
            okForm = False
            badForm = True
            
        if goodForm:
            print("You have great form")
        elif okForm:
            print("Your form is ok")
        elif badForm:
            print("Your form is terrible")
        
        angles = []
        distanceList = []
        buffer = 0
    
    if angle <= 35.0 and not curlUp:
        rep += 1
        curlUp = True
    elif angle >= 160 and curlUp:
        curlUp = False
    
    print(f"Your on rep: {rep}")
'''
