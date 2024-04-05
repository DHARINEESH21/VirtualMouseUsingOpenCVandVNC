import mediapipe as mp
import cv2
import pyautogui
from math import sqrt

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# For vedio capturing
video = cv2.VideoCapture(0)


SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()

with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while video.isOpened():
        _, frame = video.read()
        if not _:
            break

        frame = cv2.flip(frame, 1)
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(frameRGB)

        if results.multi_hand_landmarks:
            for handLandmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, handLandmarks, mp_hands.HAND_CONNECTIONS)
                landmarks = handLandmarks.landmark

                thumb_tip = landmarks[4]       # Thumb tip
                index_tip = landmarks[8]       # Index finger tip
                middle_tip = landmarks[12]     # Middle finger tip
                ring_tip = landmarks[16]       # Ring finger tip

                thumb_index_dist = sqrt((thumb_tip.x - index_tip.x) ** 2 + (thumb_tip.y - index_tip.y) ** 2)
                thumb_middle_dist = sqrt((thumb_tip.x - middle_tip.x) ** 2 + (thumb_tip.y - middle_tip.y) ** 2)
                index_ring_dist = sqrt((index_tip.x - ring_tip.x) ** 2 + (index_tip.y - ring_tip.y) ** 2)

                # Gesture recognition
                if thumb_index_dist < 0.05:
                    pyautogui.click()  # Left click
                    print("Left click")
                elif thumb_middle_dist < 0.05:
                    pyautogui.rightClick()  # Right click
                    print("Right click")
                elif index_ring_dist < 0.05:
                    pyautogui.doubleClick()  # Double click
                    print("Double click")

                # Cursor movement
                cursor_x = int(index_tip.x * SCREEN_WIDTH)
                cursor_y = int(index_tip.y * SCREEN_HEIGHT)
                pyautogui.moveTo(cursor_x, cursor_y, duration=0.1)

        cv2.imshow('Hand Tracking', frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

video.release()
