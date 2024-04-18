import cv2
import mediapipe as mp
from exclusionLandmarks import *
from mediapipe.python.solutions.drawing_utils import DrawingSpec

def sideBodyTracking(leftLeg=True, rightLeg=True, leftArm=True, rightArm=True, face=False, debug=False):
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    # Create Pose solution with high accuracy (static image mode)
    pose_with_landmarks = mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.5, static_image_mode=False)

    customStyle = mp_drawing_styles.get_default_pose_landmarks_style()
    customConnections = list(mp_pose.POSE_CONNECTIONS)
    
    # Use 0 for webcam, or provide video file path
    cap = cv2.VideoCapture(0)
    
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

    for landmark in excludedLandmarks:
        customStyle[landmark] = DrawingSpec(color=(0,0,0), thickness=None, circle_radius=0)
        customConnections = [connection_tuple for connection_tuple in customConnections if landmark.value not in connection_tuple]
        
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
            image_Height, image_Width, _ = image.shape
            
            for idx, landm in enumerate(landmarks):
                mp_drawing.draw_landmarks(image, results.pose_landmarks, connections=customConnections, landmark_drawing_spec=customStyle)
            
        # Display the resulting frame
        cv2.imshow('MediaPipe Pose', image)
        
        # Exit on 'q' key press
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    
