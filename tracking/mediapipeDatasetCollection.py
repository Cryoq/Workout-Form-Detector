import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
import time

def calculateAngle(a,b,c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    rad = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(rad*180.0/np.pi)
    
    if angle > 180.0:
        angle = 360 - angle
    
    return angle

start_time = time.time()
def frontBodyTracking(videopath, debug:bool = False):
    try:
        global start_time
        mp_drawing = mp.solutions.drawing_utils
        mp_pose = mp.solutions.pose
        landmarkDataset = []

        # Create drawing spec for efficient drawing
        drawing_spec = mp_drawing.DrawingSpec(thickness=int(2), circle_radius=int(2), color=(0, 255, 0))

        # Create Pose solution with high accuracy (static image mode)
        pose_with_landmarks = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5, static_image_mode=False)

        # Use 0 for webcam, or provide video file path
        cap = cv2.VideoCapture(videopath)
        while cap.isOpened():
            success, image = cap.read()

            if not success:
                print("End of Video.")
                
                print(landmarkDataset)
                np.save("data/MLRightCurl.npy", np.array(landmarkDataset))
                
                break

            # Convert the BGR image to RGB format for MediaPipe processing
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False  # Optimize for performance

            # Perform pose detection on the image
            results = pose_with_landmarks.process(image)
            
            # Convert the image back to BGR format for display
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Draw pose landmarks if results are available
            if results.pose_landmarks:
                
                landmarks = results.pose_landmarks.landmark
                
                # Grabs the x,y values from the main body points and left arm
                leftShoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                #rightShoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                #rightHip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                #leftHip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                
                # Appends data to landmarks
                elbow_angle = calculateAngle(wrist, elbow, leftShoulder)
                current_time = time.time()
                elapsed_time = current_time - start_time
                landmarkDataset.append([elbow_angle, elapsed_time])  
            
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS, drawing_spec)
                    
            # Display the resulting frame
            cv2.imshow('MediaPipe Pose', image)
            
            # Exit on 'q' key press
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break
    except Exception as f:
        print(f)

    cap.release()
    cv2.destroyAllWindows()
    
frontBodyTracking("C:/Users/aland/OneDrive/Pictures/Camera Roll/MLRightCurls.mp4")