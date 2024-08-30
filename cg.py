import cv2
import mediapipe as mp
from math import hypot
import screen_brightness_control as sbc
import numpy as np

# Initializing the Model
mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.75,
    min_tracking_confidence=0.75,
    max_num_hands=2
)
Draw = mp.solutions.drawing_utils

# Start capturing video from webcam
cap = cv2.VideoCapture(0)
while True:
    # Read video frame by frame
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    Process = hands.process(frameRGB)

    landmarkList = []
    # If hands are present in image (frame)
    if Process.multi_hand_landmarks:
        # Detect hand landmarks
        for handlm in Process.multi_hand_landmarks:
            for _id, landmarks in enumerate(handlm.landmark):
                # Store height and width of image
                height, width, color_channels = frame.shape
                # Calculate and append x, y coordinates of hand landmarks from image (frame) to landmarkList
                x, y = int(landmarks.x * width), int(landmarks.y * height)
                landmarkList.append([_id, x, y])
            Draw.draw_landmarks(frame, handlm, mpHands.HAND_CONNECTIONS)

    if landmarkList:
        # Store x, y coordinates of (tip of) thumb and index finger
        x_1, y_1 = landmarkList[4][1], landmarkList[4][2]
        x_2, y_2 = landmarkList[8][1], landmarkList[8][2]
        cv2.circle(frame, (x_1, y_1), 7, (8, 255, 0), cv2.FILLED)
        cv2.circle(frame, (x_2, y_2), 7, (8, 255, 0), cv2.FILLED)
        cv2.line(frame, (x_1, y_1), (x_2, y_2), (8, 255, 0), 3)
        L = hypot(x_2 - x_1, y_2 - y_1)
        b_level = np.interp(L, [15, 220], [0, 100])
        sbc.set_brightness(int(b_level))

    # Display Video and when 'q' is entered, destroy the window
    cv2.imshow("Image", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
