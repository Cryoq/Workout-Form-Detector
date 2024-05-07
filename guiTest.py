import pygame_menu
import pygame
import numpy as np
import pygame_menu.themes
from tracking.curl import workout
import cv2

def calculate_euclidean_distance(keypoints1, keypoints2):
    # Calculate Euclidean distance between two sets of keypoints
    return np.linalg.norm(keypoints1 - keypoints2)

def calculate_distance(realtime_keypoints, dataset):
    min_distance = float('inf')
    
    # Iterate through dataset
    for i, data_point in enumerate(dataset):
        # Calculate distance between each dataset point and real-time keypoints
        distance = calculate_euclidean_distance(realtime_keypoints, data_point)
        # Check if this distance is smaller than previous min_distance
        if distance < min_distance:
            min_distance = distance

    return min_distance


screen_width = 800
screen_height = 600

Window_Size = (screen_width, screen_width)

surface = pygame.display.set_mode((screen_width, screen_height))
pygame.init()

text_font = pygame.font.SysFont('Arial', 30)

def text(text, font, text_color, x, y):
    put_text = font.render(text, True, text_color)
    surface.blit(put_text, (x, y))

def open_camera_screen(workout) -> None:
    """
    Function to open a new screen with camera feed.
    """
    rep = 0
    form = ''
    workout.setupCamera()  # Initialize camera capture
    leftCurlPoints = np.load("data/MLLeftCurl.npy")
    running = True
    
    reps = text_font.render(f"Reps: {rep}", True, (255,255,255))
    form = text_font.render(f"Form: {form}", True, (255,255,255))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # runs one frame of the workout 
        frame = workout.oneFrame()
        try:
        
            # Calculates distance between good form dataset and real-time form data
            Lwrist, Lelbow, Lshoulder = workout.returnPoints(True, False)
            realtime_keypoints = np.array([Lwrist, Lelbow, Lshoulder])
            distance = calculate_distance(realtime_keypoints, leftCurlPoints)
            print("Distance", distance)
            
            
            # The main curl workout part
            
            form, rep = workout.curl(distance, Lwrist, Lelbow, Lshoulder)
            
            #print(form)
            #print(f"You are on rep {rep}")
        except:
            pass
        
        if frame is not None:
            # Converts cv2 frame to work with pygame and blits it onto the screen
            surface.fill((0,0,0))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  
            frame = np.rot90(frame)
            frame = pygame.surfarray.make_surface(frame)
            surface.blit(frame, (screen_width/10, screen_height/10))
            reps = text_font.render(f"Reps: {rep}", True, (255,255,255))
            form = text_font.render(f"Form: {form}", True, (255,255,255))
            surface.blit(form, (screen_width/6, screen_height-70))
            surface.blit(reps, (screen_width/2, screen_height-70))
            pygame.display.flip()

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
