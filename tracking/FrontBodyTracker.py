import cv2
import mediapipe as mp
import numpy as np
from statistics import mean

def calculateAngle(a,b,c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    
    rad = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(rad*180.0/np.pi)
    
    if angle > 180.0:
        angle = 360 - angle
    
    return angle


def frontBodyTracking(debug:bool = False):
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    buffer = 0
    Angles = []
    rep = 0
    curlUp = False

    # Create drawing spec for efficient drawing
    drawing_spec = mp_drawing.DrawingSpec(thickness=int(2), circle_radius=int(2), color=(0, 255, 0))

    # Create Pose solution with high accuracy (static image mode)
    pose_with_landmarks = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5, static_image_mode=False)

    # Use 0 for webcam, or provide video file path
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        success, image = cap.read()

        if not success:
            print("Ignoring empty camera frame.")
            continue

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
            
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            
            #if debug:
            #    print(f'Shoulder: x:{shoulder[0]}\t y:{shoulder[1]}')
            #    print(f'Wrist: x:{wrist[0]}\t y:{wrist[1]}')
            #    print(f'Elbow: x:{elbow[0]}\t y:{elbow[1]}')
            
            
            angle = calculateAngle(shoulder,elbow,wrist)
            
            if buffer < 3:
                Angles.append(angle)
                buffer += 1
        
            if buffer >= 3:
                if mean(Angles) > Angles[0]:
                    print("Down")
                else:
                    print("Up")
                Angles = []
                buffer = 0
                
            if angle <= 35.0 and not curlUp:
                rep += 1
                curlUp = True
            elif angle >= 160 and curlUp:
                curlUp = False
                
            
            if debug:
                print(f"The angle is: {calculateAngle(shoulder,elbow,wrist)}")
            
            print(f"You are on rep: {rep}")

            
            
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS, drawing_spec)
                
        # Display the resulting frame
        cv2.imshow('MediaPipe Pose', image)
        
        # Exit on 'q' key press
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    
frontBodyTracking()