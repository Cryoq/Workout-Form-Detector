import cv2
import mediapipe as mp
import numpy as np
from tracking.exclusionLandmarks import *
from mediapipe.python.solutions.drawing_utils import DrawingSpec
from statistics import mean

class workout:
    def __init__(self,front:bool,side:bool) -> None:
        # Main mediaPipe setup
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.pose_with_landmarks = self.mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7, static_image_mode=False)
        
        # Mainly used for when you want to use the normal points or custom points
        self.front = front
        self.side = side
            
        # For the workout part
        self.buffer = 0

        self.distanceList = []

        self.maxGoodForm = 0.1
        self.maxOkForm = 0.12

        self.curlUp = False
        self.rep = 0
        self.previous_Angle = 0
        
        self.speedList = []
        self.formList = []
        self.form = ["Uncontrolled", "Bad", "Good", "Great"]
        
        if self.front:
            self.drawing_spec = self.mp_drawing.DrawingSpec(color=(0,255,0))

    # ------- Calculations ------- #
    
    @staticmethod
    def calculate_distance(realtime_keypoints, dataset):
        min_distance = float('inf')
        
        # Iterate through dataset
        for data_point in dataset:
            # Calculate distance between each dataset point and real-time keypoints
            distance = workout.calculate_euclidean_distance(realtime_keypoints, data_point)
            # Check if this distance is smaller than previous min_distance
            if distance < min_distance:
                min_distance = distance
                
        return min_distance
    
    @staticmethod
    def calculate_euclidean_distance(keypoints1, keypoints2):
        # Calculate Euclidean distance between two sets of keypoints
        return np.linalg.norm(keypoints1 - keypoints2)

    # Calculates angle between 3 points ( Ex: returns the angle between our wrist, elbow, and shoulder for curls )
    @staticmethod
    def calculateAngle(a,b,c):
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)
    
        rad = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(rad*180.0/np.pi)
        
        if angle > 180.0:
            angle = 360 - angle
        
        return angle
    
    # Returns Specific points to be used 
    def returnPoints(self, leftCurl = False, rightCurl = False):
        if leftCurl:
            return self.leftWrist, self.leftElbow, self.leftShoulder
        elif rightCurl:
            return self.rightWrist, self.rightElbow, self.rightShoulder  
    
    # ------- main camera and curl stuff ------- #  
    
    def setupCamera(self):
        # 0 used for webcam, 1 used for seperate camera
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        
    def excludeLandmarks(self,leftLeg=True, rightLeg=True, leftArm=True, rightArm=True, face=False):
        if self.side:
            # If you are using the camera from the side, we will use custom points 
            # so we can get rid unused points as they like to spaz out
            self.customStyle = self.mp_drawing_styles.get_default_pose_landmarks_style()
            self.customConnections = list(self.mp_pose.POSE_CONNECTIONS)
                
            # Appends all excluded landmarks into a list
            allLandmarks = []
            excludedLandmarks = []
            points = [leftLeg, rightLeg, leftArm, rightArm, face]
            
            for index,bodyPart in enumerate(points):
                allLandmarks.extend(exLandmarks[index])
                if not bodyPart:
                    excludedLandmarks.extend(exLandmarks[index])
                
            for landmark in allLandmarks:
                self.customStyle[landmark] = DrawingSpec(color=(0,150,255))

            # Sets all excluded landmarks to be unseen
            for landmark in excludedLandmarks:
                self.customStyle[landmark] = DrawingSpec(color=(0,0,0), thickness=0, circle_radius=0)
                self.customConnections = [connection_tuple for connection_tuple in self.customConnections if landmark.value not in connection_tuple]
        else:
            print("If you want to exclude landmarks, you have to set front to False and side to True")
        
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
        
        # Converts image back to writable
        image.flags.writeable = True
        
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
    
    def curl(self, leftCurl:bool, rightCurl: bool, dataset):
        point1, point2, point3 = self.returnPoints(leftCurl, rightCurl)
        realtime_keypoints = np.array([point1, point2, point3])
        distance = workout.calculate_distance(realtime_keypoints, dataset)
        
        angle = workout.calculateAngle(point1, point2, point3)
        
        velocity_of_arm = np.diff(np.array([angle, self.previous_Angle]))
        self.previous_Angle = angle
        
        self.distanceList.append(distance)
        
        # Limits the list to a length of 5
        if len(self.distanceList) >= 5:
            self.distanceList.pop(0)
        
        if len(self.formList) >= 10:
            self.formList.pop(0)
        
        # Calculates if your form is Great, good, or bad
        if mean(self.distanceList) < self.maxGoodForm:
            self.formList.append(3)
        elif mean(self.distanceList) < self.maxOkForm:
            self.formList.append(2)
        else:
            self.formList.append(1)
        
        # If you are doing the workout too fast, it will bump your form down by one        
        if velocity_of_arm > 9 or velocity_of_arm < -9:
            self.formList[-1] -= 1     
            
        # Calculates if you done a full rep
        if angle <= 35.0 and not self.curlUp:
            self.rep += 1
            self.curlUp = True
        elif angle >= 160 and self.curlUp:
            self.curlUp = False
            
        # Gets string of how good your form is
        if 0 in self.formList:
            form = self.form[0]
        elif 1 in self.formList:
            form = self.form[1]
        elif self.formList.count(2) >= len(self.formList) // 2:
            form = self.form[2]
        else:
            form = self.form[3]        

        return form, self.rep
    
    # Returns the x,y points for the landmark given
    getPoints = lambda self, landmarks, point: [landmarks[self.mp_pose.PoseLandmark[point].value].x,landmarks[self.mp_pose.PoseLandmark[point].value].y] 
