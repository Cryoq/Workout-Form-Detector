import pygame_menu
import pygame
import numpy as np
import pygame_menu.themes
from curl import workout
import cv2

class textbox():
    def __init__(self, indicator, value, font, text_col, x, y):
        self.x = x
        self.y = y
        self.text = f"{indicator}: "
        self.text_col = text_col
        self.font = font
        self.value = value
        self.surf = self.font.render(self.text, True, self.text_col)

    def changevalue(self, val):
        self.value = val
    
    def getvalue(self):
        return self.value
    
    def gettext(self):
        return f"{self.text}: {self.getvalue()}"

    def changetext(self, text):
        self.surf = self.font.render(self.gettext(), True, self.text_col)

    def update(self):
        self.surf = self.font.render(self.gettext(), True, self.text_col)
        surface.blit(self.surf, (self.x, self.y))

def calculate_euclidean_distance(keypoints1, keypoints2):
    # Calculate Euclidean distance between two sets of keypoints
    return np.linalg.norm(keypoints1 - keypoints2)

def calculate_distance(realtime_keypoints, dataset):
    min_distance = float('inf')
    
    # Iterate through dataset
    for data_point in dataset:
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



text_font = pygame.font.Font("Grand9k Pixel.ttf", 45)

def text(text, font, text_color, x, y):
    put_text = font.render(text, True, text_color)
    surface.blit(put_text, (x, y))

def open_camera_screen(workout) -> None:
    """
    Function to open a new screen with camera feed.
    """
    reps = 0
    form = ''
    # form = textbox("Form", "", text_font, (255,255,255), screen_width/6, screen_height-70)
    # reps = textbox("Reps", 0, text_font, (255,255,255), screen_width/2, screen_height-70)
    workout.setupCamera()  # Initialize camera capture
    leftCurlPoints = np.load("leftCurlPoints.npy")
    
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
            surface.blit(frame, (screen_width/10, screen_height/10))
            text(f'Form: {form}',text_font, (255,255,255), screen_width/6, screen_height-70)
            text(f'Rep:{reps}',text_font, (255,255,255), screen_width/2, screen_height-70)
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
