from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.logger import Logger
import cv2
import numpy as np

import mediapipe as mp
import cv2

class CamApp(App):
    def build(self):
        self.web_cam = Image(size_hint = (1,.8))
        self.button = Button(text = "Start", size_hint = (1,.1))
        self.form_detec = Label(text = "Form:Good", size_hint = (1,.1))

        layout = BoxLayout(orientation = 'vertical')
        layout.add_widget(self.web_cam)
        layout.add_widget(self.form_detec)
        layout.add_widget(self.button)
        
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update, 1.0/33.0)

        return layout

    def update(self, *args):
        ret, frame = self.capture.read()
        frame = frame[120:120+150, 200:200+250, :]

        buf = cv2.flip(frame, 0).tobytes()
        img_texture = Texture.create(size = (frame.shape[1], frame.shape[0]), colorfmt = 'bgr')
        img_texture.blit_buffer(buf, colorfmt = "bgr", bufferfmt = 'ubyte')
        self.web_cam.texture = img_texture

if __name__ == '__main__':
    CamApp().run()