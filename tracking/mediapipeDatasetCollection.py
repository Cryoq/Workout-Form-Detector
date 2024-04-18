import cv2
import mediapipe as mp
import numpy as np
import pandas as pd

def frontBodyTracking(videopath, debug:bool = False):
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    landmarkDataset = []
    
    # Column for csv file
    landmarkCol = ['LeftShoulder', 'RightShoulder','LeftHip','RightHip','Wrist','Elbow']

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
            
            df = pd.read_csv("workout_data.csv")
            datalist = df.values.tolist()
            print(datalist)
            
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
            rightShoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            rightHip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            leftHip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                        
            # Prints out the x,y values for each main point for debugging
            print(f'Left Shoulder: x:{leftShoulder[0]}\t y:{leftShoulder[1]}')
            print(f'Right Shoulder: x:{rightShoulder[0]}\t y:{rightShoulder[1]}')
            print(f'Right Hip: x:{rightHip[0]}\t y:{rightHip[1]}')
            print(f'Left Hip: x:{leftHip[0]}\t y:{leftHip[1]}')
            print(f'Wrist: x:{wrist[0]}\t y:{wrist[1]}')
            print(f'Elbow: x:{elbow[0]}\t y:{elbow[1]}')
            
            # Appends data to landmarks 
            landmarkDataset.append([leftShoulder,rightShoulder,leftHip,rightHip,wrist,elbow])
            
        # Converts the landmarkDataset list to pd dataframe and converts and appends it to csv file
        landmarks_df = pd.DataFrame(landmarkDataset)
        landmarks_df.columns = landmarkCol
        landmarks_df.to_csv("workout_data.csv", index=False, mode='a')
        
        # Resets the list each frame
        landmarkDataset = []
        
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS, drawing_spec)
                
        # Display the resulting frame
        cv2.imshow('MediaPipe Pose', image)
        
        # Exit on 'q' key press
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    
frontBodyTracking("C:/Users/aland/OneDrive/Documents/Test-Workout-Video.mp4")