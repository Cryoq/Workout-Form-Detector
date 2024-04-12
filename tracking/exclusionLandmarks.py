from mediapipe.python.solutions.pose import PoseLandmark

leftLegLandmarks = [
    PoseLandmark.LEFT_ANKLE,
    PoseLandmark.LEFT_HEEL,
    PoseLandmark.LEFT_HIP,
    PoseLandmark.LEFT_KNEE
]

rightLegLandmarks = [
    PoseLandmark.RIGHT_ANKLE,
    PoseLandmark.RIGHT_HEEL,
    PoseLandmark.RIGHT_HIP,
    PoseLandmark.RIGHT_KNEE
]

leftArmLandmarks = [
    PoseLandmark.LEFT_ELBOW,
    PoseLandmark.LEFT_PINKY,
    PoseLandmark.LEFT_SHOULDER,
    PoseLandmark.LEFT_THUMB,
    PoseLandmark.LEFT_WRIST
]

rightArmLandmarks = [
    PoseLandmark.RIGHT_ELBOW,
    PoseLandmark.RIGHT_PINKY,
    PoseLandmark.RIGHT_SHOULDER,
    PoseLandmark.RIGHT_THUMB,
    PoseLandmark.RIGHT_WRIST,
    PoseLandmark.RIGHT_INDEX
]

faceLandmarks = [
    PoseLandmark.LEFT_EYE, 
    PoseLandmark.RIGHT_EYE, 
    PoseLandmark.LEFT_EYE_INNER, 
    PoseLandmark.RIGHT_EYE_INNER, 
    PoseLandmark.LEFT_EAR,
    PoseLandmark.RIGHT_EAR,
    PoseLandmark.LEFT_EYE_OUTER,
    PoseLandmark.RIGHT_EYE_OUTER,
    PoseLandmark.MOUTH_LEFT,
    PoseLandmark.MOUTH_RIGHT
]