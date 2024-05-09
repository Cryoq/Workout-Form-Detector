import pygame_menu
import pygame
import numpy as np
import pygame_menu.events
import pygame_menu.themes
from tracking.curl import workout
import cv2

class textbox():
    def __init__(self, indicator, value, font, text_col, x, y, group):
        self.x = x
        self.y = y
        self.text = f"{indicator}:"
        self.text_col = text_col
        self.font = font
        self.value = value
        self.surf = self.font.render(self.text, True, self.text_col)

        group.append(self)

    def changevalue(self, val):
        self.value = val
    
    def getvalue(self):
        return self.value
    
    def gettext(self):
        return f"{self.text} {self.getvalue()}"

    def changetext(self, text):
        self.surf = self.font.render(self.gettext(), True, self.text_col)

    def update(self):
        self.surf = self.font.render(self.gettext(), True, self.text_col)
        surface.blit(self.surf, (self.x, self.y))

def draw(frame):
    frame = np.rot90(frame)
    frame = pygame.surfarray.make_surface(frame)
    surface.blit(frame, (screen_width/10, screen_height/10))

def change_side(value, *args):
    global side
    side = value[0][0]
    
def text(text, font, text_color, x, y):
    put_text = font.render(text, True, text_color)
    surface.blit(put_text, (x, y))

def open_camera_screen(workout) -> None:
    """
    Function to open a new screen with camera feed.
    """
    global side
    running = True
    rightCurlPoints = np.load("data/rightCurlPoints.npy")
    leftCurlPoints = np.load("data/MLLeftCurl.npy")
    
    if side == "Left Curl":
        workout_instance.excludeLandmarks(rightArm=False)
        while running:
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                    running = False
            # runs one frame of the workout 
            frame = workout.oneFrame()
            
            try:
                form, rep = workout.curl(leftCurl = True, rightCurl = False, dataset = leftCurlPoints)
            except Exception as f:
                print(f)
                print("Please Step into frame")
                
            if frame is not None:
                # Converts cv2 frame to work with pygame and blits it onto the screen
                draw(frame)
                pygame.display.flip()
                
            labels.clear()
            
            formlabel = textbox("Form", form, text_font, (0,0,0), screen_width-723, screen_height-70, labels)
            replabel = textbox("Reps", rep, text_font, (0,0,0), screen_width-225, screen_height-70, labels)             
            surface.blit(background,(0,0))
            for label in labels:
                label.update()  

    if side == "Right Curl": 
        workout_instance.excludeLandmarks(leftArm=False)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
            # runs one frame of the workout 
            frame = workout.oneFrame()
            
            try:
                form, rep = workout.curl(leftCurl = False, rightCurl = True, dataset = rightCurlPoints)
            except:
                print("Please Step into frame")
                
            if frame is not None:
                # Converts cv2 frame to work with pygame and blits it onto the screen
                draw(frame)
                pygame.display.flip()
                
            labels.clear()
            try:
                formlabel = textbox("Form", form, text_font, (0,0,0), screen_width-723, screen_height-70, labels)
                replabel = textbox("Reps", rep, text_font, (0,0,0), screen_width-225, screen_height-70, labels)             
                surface.blit(background,(0,0))
                for label in labels:
                    label.update()
            except:
                pass

#### pygame ###
button_image_path = 'images/button.png'
background_image_path = 'images/background.png'

screen_width = 800
screen_height = 600

Window_Size = (screen_width, screen_width)

surface = pygame.display.set_mode((screen_width, screen_height))
labels = []
background = pygame.image.load(background_image_path)
background = pygame.transform.smoothscale(background, (screen_width,screen_height))

pygame.init()

text_font = pygame.font.SysFont("Arial", 45)
            
### pygame Menu ###

main_menu_theme = pygame_menu.themes.THEME_GREEN.copy()
main_menu_theme.set_background_color_opacity(0.5)
theme_bg_image = main_menu_theme.copy()
theme_bg_image.background_color = pygame_menu.BaseImage(image_path=background_image_path)

menu = pygame_menu.Menu(height=screen_height, theme=theme_bg_image, title='Workout Form Detector', width=screen_width)

workout_instance = workout(False, True)
workout_instance.setupCamera()  # Initialize camera capture

menu.add.dropselect(
    title='Curls',
    items=[('Left Curl', 0), ('Right Curl', 1)],
    placeholder='Select which side',
    onchange=change_side,
    background_color=pygame_menu.BaseImage(image_path=button_image_path)

    )

menu.add.button('Open Camera Screen', open_camera_screen, workout_instance, background_color=pygame_menu.BaseImage(image_path=button_image_path) )
menu.add.button('Quit', pygame_menu.events.EXIT, background_color=pygame_menu.BaseImage(image_path=button_image_path))

if __name__ == '__main__':
    menu.mainloop(surface)