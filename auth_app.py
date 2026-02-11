import warnings
import os
warnings.filterwarnings("ignore")
os.environ["NO_ALBUMENTATIONS_UPDATE"] = "1"
os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GLOG_minloglevel"] = "3"

import cv2
import mediapipe as mp
import numpy as np
import math
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from gesture_auth import GestureAuth

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

cap = cv2.VideoCapture(0)

model_path = 'gesture_recognizer.task' 

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.IMAGE)

recognizer = GestureRecognizer.create_from_options(options)

# TODO: Create a GestureAuth instance


while cap.isOpened():
    success, frame = cap.read()
    if not success: break

    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape
    
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        
    recognition_result = recognizer.recognize(mp_image)
        
    gesture = "None"
    score = 0.0
        
    if recognition_result.gestures:
        top_gesture = recognition_result.gestures[0][0]
        gesture = top_gesture.category_name
        score = top_gesture.score

    color = (0, 0, 255) if score < 0.5 else (0, 255, 0)
        
    text = f"Gesture: {gesture} ({int(score * 100)}%)"
    cv2.putText(frame, text, (50, 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 3)
    
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # TODO: Pass the detected gesture and score to your GestureAuth instance every frame


    # TODO: Handle keyboard input
    #   'e' → prompt for username, start enrollment
    #   'v' → prompt for username, start verification
    #   SPACE (key == 32) → signal sequence is complete
    #   ESC (key == 27) → cancel current operation


    # TODO: Draw UI overlay on the frame
    #   - Status message (what should the user do next?)
    #   - Current sequence progress (which gestures have been registered so far?)
    #   - Hold progress bar (how close is the current gesture to registering?)
    #   - Result display (ACCESS GRANTED / ACCESS DENIED)


    cv2.imshow("Gesture Auth", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
