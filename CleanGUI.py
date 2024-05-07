import pygame_menu
import pygame
import numpy as np
import pygame_menu.themes
from tracking.curl import workout
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

text_font = pygame.font.SysFont("Arial", 45)

def change_side(value, *args):
    global side
    side = value[0]

def text(text, font, text_color, x, y):
    put_text = font.render(text, True, text_color)
    surface.blit(put_text, (x, y))
    
def draw(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  
    frame = np.rot90(frame)
    frame = pygame.surfarray.make_surface(frame)
    surface.blit(frame, (screen_width/10, screen_height/10))

def open_camera_screen(workout) -> None:
    """
    Function to open a new screen with camera feed.
    """
    form = ''
    rep = 0
    global side
    workout.setupCamera()  # Initialize camera capture
    
    running = True
    rightCurlPoints = np.load("data/rightCurlPoints.npy")
    leftCurlPoints = np.load("data/leftCurlPoints.npy")
    
    if side == "Left Curl":
        workout_instance.excludeLandmarks(rightArm=False)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        running = False
                
            # runs one frame of the workout 
            frame = workout.oneFrame()
                        
            try:
                # Calculates distance between good form dataset and real time form data
                Lwrist, Lelbow, Lshoulder = workout.returnPoints(True, False)
                realtime_keypoints = np.array([Lwrist, Lelbow, Lshoulder])
                distance = calculate_distance(realtime_keypoints, leftCurlPoints)
                print("Distance", distance)
                    
                # The main curl workout part
                form, rep = workout.curl(distance, Lwrist, Lelbow, Lshoulder)    
            except:
                pass

            if frame is not None:
                # Converts cv2 frame to work with pygame and blits it onto the screen
                draw(frame)
                text(f'Form: {form}',text_font, (255,255,255), screen_width/6, screen_height-70)
                text(f'Rep:{rep}',text_font, (255,255,255), screen_width/2, screen_height-70)
                
                pygame.display.flip()
            
    if side == "Right Curl":
        workout_instance.excludeLandmarks(leftArm=False) 
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
            # runs one frame of the workout 
            frame = workout.oneFrame()
                
            try:
                # Calculates distance between good form dataset and real time form data
                Rwrist, Relbow, Rshoulder = workout.returnPoints(False, True)
                realtime_keypoints = np.array([Rwrist, Relbow, Rshoulder])
                distance = calculate_distance(realtime_keypoints, rightCurlPoints)
                print("Distance", distance)
                    
                # The main curl workout part
                form, rep = workout.curl(distance, Rwrist, Relbow, Rshoulder)
            except:
                pass
            
            if frame is not None:
                # Converts cv2 frame to work with pygame and blits it onto the screen
                draw(frame)
                text(f'Form: {form}',text_font, (255,255,255), screen_width/6, screen_height-70)
                text(f'Rep:{rep}',text_font, (255,255,255), screen_width/2, screen_height-70)
                pygame.display.flip()

main_menu_theme = pygame_menu.themes.THEME_GREEN.copy()
main_menu_theme.set_background_color_opacity(0.5)
theme_bg_image = main_menu_theme.copy()
theme_bg_image.background_color = pygame_menu.BaseImage(image_path='background.png')

menu = pygame_menu.Menu(height=600, theme=theme_bg_image, title='Workout Form Tester', width=800)

workout_instance = workout(False, True)

menu.add.dropselect(
    title='Curls',
    items=['Left Curl', 'Right Curl'],
    placeholder='Select which side',
    onchange=change_side,
    background_color=pygame_menu.BaseImage(image_path='button.png')
    )

menu.add.button('Open Camera Screen', open_camera_screen, workout_instance, background_color=pygame_menu.BaseImage(image_path='button.png') )
menu.add.button('Quit', pygame_menu.events.EXIT, background_color=pygame_menu.BaseImage(image_path='button.png'))

if __name__ == '__main__':
    menu.mainloop(surface)