from tracking.WorkoutClass import workout
from statistics import mean
import numpy as np

def form(currentX, X_train):
    distances = np.linalg.norm(X_train - currentX, axis=1)

    nearest_neighbor_idx = np.argmin(distances)
    print(nearest_neighbor_idx)

    return distances[nearest_neighbor_idx]


X_train = np.load("data/3PointsWorkout_data.npy")

curl = workout(side=True, front=False)

curl.setupCamera()

# If you are doing from side
curl.excludeLandmarks(rightArm=False)
angles = []
buffer = 0

running = True
curlUp = False

rep = 0

while running:
    
    #print("HEllo")
    curl.oneFrame()
    #print("TSET")
    
    shoulder, wrist, elbow = curl.returnPoints()
    
    current_X = np.array([shoulder[0],shoulder[1], wrist[0], wrist[1], elbow[0], elbow[1]])
    
    distance = form(current_X, X_train)

    print(f"Distance to nearest trained data point: {distance}")

    
    #print("After points returned")
    
    #print(f"shoulder: {shoulder}\nwrist: {wrist}\nelbow: {elbow}")
    
    angle = curl.curl()
    if buffer < 3:
        angles.append(angle)
        buffer += 1
        
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
