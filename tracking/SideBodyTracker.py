import cv2
import mediapipe as mp

def sideBodyTracking(leftLeg:bool = True, rightLeg:bool = True, leftArm:bool = True, rightArm:bool = True, face:bool = False, debug:bool = False):
    mp_pose = mp.solutions.pose

    # Create Pose solution with high accuracy (static image mode)
    pose_with_landmarks = mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.5, static_image_mode=False)

    # Use 0 for webcam, or provide video file path
    cap = cv2.VideoCapture(0)

    # Define the indices of the right leg landmarks
    left_leg_indices =  [25, 27, 29, 31]
    right_leg_indices = [26, 28, 30, 32]

    # contains both right and left arm [11,12,13,14,15,16,17,18,19,20]
    left_arm_indices = [11,13,15,17,19,21]
    right_arm_indices = [12,14,16,18,20,22]
    
    face_indicies = [1,2,3,4,5,6,7,8,9,10]
    

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
            image_height, image_width, _ = image.shape
            
            for idx, landmark in enumerate(landmarks):
                x = int(landmark.x * image_width)
                y = int(landmark.y * image_height)
                
                # Omits certain landmarks
                if not leftLeg and idx in left_leg_indices:
                    continue
                if not rightLeg and idx in right_leg_indices:
                    continue
                if not leftArm and idx in left_arm_indices:
                    continue
                if not rightArm and idx in right_arm_indices:
                    continue
                if not face and idx in face_indicies:
                    continue
                
                if debug:
                    print(f"Landmark: {idx}: x={x}, y={y}")
                
                # Draw point on the image
                cv2.circle(image, (x, y), 5, (0, 255, 0), -1)
            
        # Display the resulting frame
        cv2.imshow('MediaPipe Pose', image)
        
        # Exit on 'q' key press
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    
sideBodyTracking(leftArm=False)
