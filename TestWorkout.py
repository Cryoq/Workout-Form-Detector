from tracking.WorkoutClass import workout
from statistics import mean
import pickle

model = pickle.loads("curlmodel.pkl")

curl = workout(side=False, front=True)

curl.setupCamera()
#curl.excludeLandmarks(rightArm=False)
angles = []
buffer = 0

running = True
curlUp = False

rep = 0

while running:
    curl.oneFrame()
    shoulder, wrist, elbow = curl.returnPoints()
    print(f"shoulder: {shoulder}\nwrist: {wrist}\nelbow: {elbow}")
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
