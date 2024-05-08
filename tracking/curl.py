import cv2
import mediapipe as mp
import numpy as np
from tracking.exclusionLandmarks import *
from mediapipe.python.solutions.drawing_utils import DrawingSpec
from statistics import mean

class workout:
    def __init__(self,front:bool,side:bool) -> None:
        
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.pose_with_landmarks = self.mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.5, static_image_mode=False)
        
        # Mainly used for when you want to use the normal points or custom points
        self.front = front
        self.side = side
        
        # If you are using the camera from the side, we will use custom points 
        # so we can get rid unused points as they like to spaz out
            
        # For the workout part
        self.buffer = 0

        self.distanceList = []

        self.maxGoodForm = 0.19
        self.maxOkForm = 0.21

        self.curlUp = False
        self.rep = 0
        self.prevAngle = 0
        
        self.speedList = []
        self.form = ['Great', 'good', 'bad', 'uncontrolled']
        self.formIndex = 0
    
    def setupCamera(self):
        # 0 used for webcam, 1 used for seperate camera
        self.cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

        
    def excludeLandmarks(self,leftLeg=True, rightLeg=True, leftArm=True, rightArm=True, face=False):
        
        if self.side:
            self.customStyle = self.mp_drawing_styles.get_default_pose_landmarks_style()
            self.customConnections = list(self.mp_pose.POSE_CONNECTIONS)
        else:
            self.drawing_spec = self.mp_drawing.DrawingSpec(thickness=int(2), circle_radius=int(2), color=(0,255,0))
            
            
        # Appends all excluded landmarks into a list
        excludedLandmarks = []
        points = [leftLeg, rightLeg, leftArm, rightArm, face]
        
        for index,bodyPart in enumerate(points):
            if not bodyPart:
                excludedLandmarks.extend(exLandmarks[index])

        # Sets all excluded landmarks to be unseen
        for landmark in excludedLandmarks:
            self.customStyle[landmark] = DrawingSpec(color=(0,0,0), thickness=None, circle_radius=0)
            self.customConnections = [connection_tuple for connection_tuple in self.customConnections if landmark.value not in connection_tuple]  
        
    # Plays one frame of the display
    def oneFrame(self):
        success, image = self.cap.read()
        
        if not success:
            print("Ignoring empty camera frame")
        
        # Converts BRG image to RGB format for MediaPipe processing
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        
        # Performs pose detection
        results = self.pose_with_landmarks.process(image)
        
        # Converts image back to BRG format to display
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            
            # Gets LEFT shoulder, wrist, elbow (x,y) Values
            self.leftShoulder = self.getPoints(landmarks, "LEFT_SHOULDER")
            self.leftWrist = self.getPoints(landmarks, "LEFT_WRIST")
            self.leftElbow = self.getPoints(landmarks, "LEFT_ELBOW")
            
            # Gets RIGHT shoulder, wrist, elbow (x,y) Values
            self.rightShoulder = self.getPoints(landmarks, "RIGHT_SHOULDER")
            self.rightWrist = self.getPoints(landmarks, "RIGHT_WRIST")
            self.rightElbow = self.getPoints(landmarks, "RIGHT_ELBOW")
            
        # If the front is being used, use normal connections/landmarks
        if self.front:
            self.mp_drawing.draw_landmarks(image, results.pose_landmarks, connections=self.mp_pose.POSE_CONNECTIONS, landmark_drawing_spec=self.drawing_spec)
        
        # If the side  is being used, use custom connections/landmarks    
        if self.side:
            self.mp_drawing.draw_landmarks(image, results.pose_landmarks, connections=self.customConnections, landmark_drawing_spec=self.customStyle)
            
        return image
    
    # Returns Specific points to be used 
    def returnPoints(self, leftCurl = False, rightCurl = False):
        if leftCurl:
            return self.leftWrist, self.leftElbow, self.leftShoulder
        elif rightCurl:
            return self.rightWrist, self.rightElbow, self.rightShoulder
    
    def curl(self, distance, point1, point2, point3):
        angle = self.calculateAngle(point1, point2, point3)
        
        vel = np.diff(np.array([angle, self.prevAngle]))
        self.prevAngle = angle
        
        if vel > 9 or vel < -9:
            self.speedList.append("Fast")
        else:
            self.speedList.append("Good")
        
        if len(self.speedList) > 7:
            self.speedList.pop(0)
        
        if self.buffer < 3:
            self.distanceList.append(distance)
            self.buffer += 1
            
            if mean(self.distanceList) < self.maxGoodForm:
                self.formIndex = 0
            elif mean(self.distanceList) < self.maxOkForm:
                self.formIndex = 1
            else:
                self.formIndex = 2
            
            self.distanceList = []
            self.buffer = 0

        if angle <= 35.0 and not self.curlUp:
            self.rep += 1
            self.curlUp = True
        elif angle >= 160 and self.curlUp:
            self.curlUp = False
        
        if self.speedList.count("Fast") > 3:
            self.formIndex += 1
        
        form = self.form[self.formIndex]

        return form, self.rep
    
    def calculateAngle(self,a,b,c):
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)
    
        rad = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(rad*180.0/np.pi)
        
        if angle > 180.0:
            angle = 360 - angle
        
        return angle
    
    getPoints = lambda self, landmarks, point: [landmarks[self.mp_pose.PoseLandmark[point].value].x,landmarks[self.mp_pose.PoseLandmark[point].value].y] 