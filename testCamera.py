import pygame_menu
import pygame
import numpy as np
import pygame_menu.themes
from tracking.curl import workout
import cv2

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

    return min_distance

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
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # runs one frame of the workout 
        frame = workout.oneFrame()
        
        if frame is not None:
            # Converts cv2 frame to work with pygame and blits it onto the screen
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  
            frame = np.rot90(frame)
            frame = pygame.surfarray.make_surface(frame)
            surface.blit(frame, (screen_width/8, screen_height/8))
            pygame.display.flip()
            
        # Calculates distance between good form dataset and real time form data
        Lwrist, Lelbow, Lshoulder = workout.returnPoints(True, False)
        realtime_keypoints = np.array([Lwrist, Lelbow, Lshoulder])
        distance = calculate_distance(realtime_keypoints, leftCurlPoints)
        print("Distance", distance)
        
        # The main curl workout part
        form, rep = workout.curl(distance, Lwrist, Lelbow, Lshoulder)
        
        print(form)
        print(f"You are on rep {rep}")

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
