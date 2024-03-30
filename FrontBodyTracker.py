import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Create drawing spec for efficient drawing
drawing_spec = mp_drawing.DrawingSpec(thickness=int(2), circle_radius=int(2), color=(0, 255, 0))
# Create Pose solution with high accuracy (static image mode)
pose_with_landmarks = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5, static_image_mode=False)
cap = cv2.VideoCapture(0)  # Use 0 for webcam, or provide video file path

# Define a dictionary to store the previous positions of landmarks
previous_landmarks = {}

# Number of previous positions to consider for filtering
filter_window_size = 5

# Confidence threshold for detected landmarks
confidence_threshold = 0.2

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
            
            # Filter landmarks with confidence below the threshold
            if landmark.visibility < confidence_threshold:
                continue
            
            # Apply moving average filter to landmark positions
            if idx not in previous_landmarks:
                previous_landmarks[idx] = []
            
            previous_landmarks[idx].append((x, y))
            if len(previous_landmarks[idx]) > filter_window_size:
                previous_landmarks[idx].pop(0)
            
            avg_x = sum(pos[0] for pos in previous_landmarks[idx]) / len(previous_landmarks[idx])
            avg_y = sum(pos[1] for pos in previous_landmarks[idx]) / len(previous_landmarks[idx])
            
            print(f"Landmark: {idx}: x={avg_x}, y={avg_y}")
            cv2.circle(image, (int(avg_x), int(avg_y)), 5, (0, 255, 0), -1)
        
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS, drawing_spec)

    # Display the resulting frame
    cv2.imshow('MediaPipe Pose', image)
    
    # Exit on 'q' key press
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
