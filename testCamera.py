import cv2
import numpy as np
import pygame
from pygame.locals import *

class PygameApp:
    def __init__(self, width, height, workout):
        self.width = width
        self.height = height
        self.workout = workout
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Workout App")
        self.clock = pygame.time.Clock()

    def run(self):
        self.workout.setupCamera()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            frame = self.workout.oneFrame()
            if frame is not None:
                self.display_frame(frame)

            pygame.display.flip()
            self.clock.tick(30)

        self.workout.releaseCamera()
        pygame.quit()

    def display_frame(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        frame = pygame.surfarray.make_surface(frame)
        self.screen.blit(frame, (0, 0))

if __name__ == "__main__":
    from tracking.curl import workout  # Import your workout class

    workout = workout(front=False, side=True)
    workout.excludeLandmarks(rightArm=False)
    pygame.init()
    app = PygameApp(800, 600, workout)
    app.run()
