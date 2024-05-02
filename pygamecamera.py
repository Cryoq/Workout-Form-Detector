import pygame_menu
import pygame
import cv2
import numpy as np
import pygame_menu.themes

screen_width = 800
screen_height = 600

surface = pygame.display.set_mode((screen_width, screen_height))
pygame.init()

def open_camera_screen() -> None:
    """
    Function to open a new screen with camera feed.
    """
    cap = cv2.VideoCapture(0)  # Initialize camera capture
    
    running = True
    while running:
        ret, frame = cap.read()  # Read frame from camera
        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert OpenCV BGR to RGB

        frame = np.rot90(frame)  # Rotate frame 90 degrees clockwise

        frame = pygame.surfarray.make_surface(frame)  # Convert frame to pygame surface
        
        surface.blit(frame, (screen_width/8, screen_height/8))  # Blit frame onto pygame surface
        
        pygame.display.flip()  # Update display
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
    cap.release()  # Release camera
    cv2.destroyAllWindows()  # Close OpenCV windows

menu = pygame_menu.Menu(
    height=600,
    theme=pygame_menu.themes.THEME_DARK,
    title='Workout Form Tester',
    width=800,
)

menu.add.dropselect(
    title='Curls',
    items=['Left Curl', 'Right Curl'],
    placeholder='Select which side'
)
menu.add.button('Open Camera Screen', open_camera_screen)
menu.add.button('Quit', pygame_menu.events.EXIT)

if __name__ == '__main__':
    menu.mainloop(surface)
