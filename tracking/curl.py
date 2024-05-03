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
        self.front = front
        self.side = side
        # If you are using the camera from the side, we will use custom points 
        # so we can get rid unused points as they like to spaz out
        if self.side:
            self.customStyle = self.mp_drawing_styles.get_default_pose_landmarks_style()
            self.customConnections = list(self.mp_pose.POSE_CONNECTIONS)
        else:
            self.drawing_spec = self.mp_drawing.DrawingSpec(thickness=int(2), circle_radius=int(2), color=(0,255,0))
            

        # For the workout part
        self.buffer = 0

        self.distanceList = []

        self.maxGoodForm = 0.09
        self.maxOkForm = 0.11

        self.curlUp = False

        self.rep = 0
    
    def setupCamera(self):
        # 0 used for webcam, or provide a file path
        self.cap = cv2.VideoCapture(0)
        
    def excludeLandmarks(self,leftLeg=True, rightLeg=True, leftArm=True, rightArm=True, face=False):

        # Appends all excluded landmarks into a list
        excludedLandmarks = []    
        if not leftLeg:
            excludedLandmarks.extend(leftLegLandmarks)
        if not rightLeg:
            excludedLandmarks.extend(rightLegLandmarks)
        if not leftArm:
            excludedLandmarks.extend(leftArmLandmarks)
        if not rightArm:
            excludedLandmarks.extend(rightArmLandmarks)
        if not face:
            excludedLandmarks.extend(faceLandmarks)

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
            
            # Sets the x,y position for shoulder, wrist, and elbow
            self.leftShoulder = [landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            self.leftWrist = [landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            self.leftElbow = [landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            
            self.rightShoulder = [landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            self.rightWrist = [landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
            self.rightElbow = [landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            
        # If the front is being used, use normal connections/landmarks
        # If the side  is being used, use custom connections/landmarks 
        if self.front:
            self.mp_drawing.draw_landmarks(image, results.pose_landmarks, connections=self.mp_pose.POSE_CONNECTIONS, landmark_drawing_spec=self.drawing_spec)
        if self.side:
            self.mp_drawing.draw_landmarks(image, results.pose_landmarks, connections=self.customConnections, landmark_drawing_spec=self.customStyle)
            
        return image
            
        
    
    # Returns Specific points to be used for model
    def returnPoints(self, leftCurl = False, rightCurl = False):
        if leftCurl:
            return self.leftWrist, self.leftElbow, self.leftShoulder
        elif rightCurl:
            return self.rightWrist, self.rightElbow, self.rightShoulder
    
    def curl(self, distance, point1, point2, point3):
        angle = self.calculateAngle(point1, point2, point3)
        if self.buffer < 3:
            self.distanceList.append(distance)
            self.buffer += 1
            
            if mean(self.distanceList) < self.maxGoodForm:
                goodForm = True
                okForm = False
                badForm = False
            elif mean(self.distanceList) < self.maxOkForm:
                goodForm = False
                okForm = True
                badForm = False
            else:
                goodForm = False
                okForm = False
                badForm = True
                
            if goodForm:
                form = "You have great form"
            elif okForm:
                form = "Your form is ok"
            elif badForm:
                form = "Your form is terrible"
            
            self.distanceList = []
            self.buffer = 0

        if angle <= 35.0 and not self.curlUp:
            self.rep += 1
            self.curlUp = True
        elif angle >= 160 and self.curlUp:
            self.curlUp = False

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
    