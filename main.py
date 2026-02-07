import cv2
import mediapipe as mp
import numpy as np
from piano_keys import draw_piano_keys

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.5)

cap = cv2.VideoCapture(0)

print("Piano Engine Started. Press 'q' to quit.")

while cap.isOpened():
    success, frame = cap.read()
    if not success: break

    frame = cv2.flip(frame, 1)
    
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            fingertip_ids = [4, 8, 12, 16, 20]

            for finger in fingertip_ids:
                finger_tip = hand_landmarks.landmark[finger]
                
                h, w, c = frame.shape
                cx, cy = int(finger_tip.x * w), int(finger_tip.y * h)
                
                cv2.circle(frame, (cx, cy), 15, (0, 255, 0), -1)

    cv2.imshow("Virtual Piano", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()