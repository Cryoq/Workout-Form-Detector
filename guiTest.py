import pygame_menu
import pygame
import numpy as np
import pygame_menu.themes
from tracking.curl import workout
import cv2
from statistics import mean

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

screen_width = 800
screen_height = 600

Window_Size = (screen_width, screen_width)
# MediaPipe setup

surface = pygame.display.set_mode((screen_width, screen_height))
pygame.init()

def open_camera_screen(workout) -> None:
    """
    Function to open a new screen with camera feed.
    """
    workout.setupCamera()  # Initialize camera capture
    leftCurlPoints = np.load("data/leftCurlPoints.npy")
    
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
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        frame = workout.oneFrame()
        if frame is not None:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  
            frame = np.rot90(frame)  # Rotate frame 90 degrees clockwise
            frame = pygame.surfarray.make_surface(frame)  # Convert frame to pygame surface
            surface.blit(frame, (screen_width/8, screen_height/8))  # Blit frame onto pygame surface
            pygame.display.flip()  # Update display
            
        shoulder, wrist, elbow = workout.returnPoints()
        realtime_keypoints = np.array([wrist, elbow, shoulder])
        distance, closest_point = calculate_distance(realtime_keypoints, leftCurlPoints)
        print("Distance", distance)
        
        angle = workout.curl()
        
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

    workout.releaseCamera()

menu = pygame_menu.Menu(height=600, theme=pygame_menu.themes.THEME_DARK, title='Workout Form Tester', width=800)

workout_instance = workout(False, True)
workout_instance.excludeLandmarks(rightArm=False)

menu.add.dropselect(
    title='Curls',
    items=['Left Curl', 'Right Curl'],
    placeholder='Select which side'
)
menu.add.button('Open Camera Screen', open_camera_screen, workout_instance)
menu.add.button('Quit', pygame_menu.events.EXIT)

if __name__ == '__main__':
    menu.mainloop(surface)
