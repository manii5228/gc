import cv2
import mediapipe as mp 
import pyautogui
import time
import math

# Setup
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
screen_width, screen_height = pyautogui.size()

# MediaPipe hands setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.75)

# Gesture helper
def get_distance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

# Control Flags
prev_direction = ""
speed_zone = ""

# Main loop
while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    h, w, _ = frame.shape

    # Draw reference lines (center & control zones)
    center_x = w // 2
    left_thresh = 250
    right_thresh = 400

    # Center, Left, and Right Zones
    cv2.line(frame, (center_x, 0), (center_x, h), (255, 255, 0), 2)
    cv2.line(frame, (left_thresh, 0), (left_thresh, h), (0, 255, 0), 1)
    cv2.line(frame, (right_thresh, 0), (right_thresh, h), (0, 0, 255), 1)
    cv2.putText(frame, 'Left Zone', (left_thresh - 100, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
    cv2.putText(frame, 'Right Zone', (right_thresh + 10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)
    cv2.putText(frame, 'Center', (center_x - 30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,0), 2)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            lm_list = []
            for id, lm in enumerate(hand_landmarks.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append((cx, cy))

            # ✅ Draw skeleton (green points, blue connections)
            for i, lm in enumerate(lm_list):
                cv2.circle(frame, lm, 5, (0, 255, 0), cv2.FILLED)  # Green dots
            for connection in mp_hands.HAND_CONNECTIONS:
                start_idx, end_idx = connection
                if start_idx < len(lm_list) and end_idx < len(lm_list):
                    cv2.line(frame, lm_list[start_idx], lm_list[end_idx], (255, 0, 0), 2)  # Blue lines

            if lm_list:
               # Calculate better center of palm
                x_center = lm_list[6][0]


                if x_center < left_thresh and prev_direction != "left":
                    print("Left")
                    pyautogui.keyDown('left')
                    pyautogui.keyUp('right')
                    prev_direction = "left"
                elif x_center > right_thresh and prev_direction != "right":
                    print("Right")
                    pyautogui.keyDown('right')
                    pyautogui.keyUp('left')
                    prev_direction = "right"
                elif left_thresh <= x_center <= right_thresh and prev_direction != "center":
                    pyautogui.keyUp('left')
                    pyautogui.keyUp('right')
                    print("Center")
                    prev_direction = "center"


                # 🚀 Acceleration/Brake based on thumb-index distance
                distance = get_distance(lm_list[4], lm_list[8])
                cv2.line(frame, lm_list[4], lm_list[8], (0, 255, 255), 2)  # Yellow line
                cv2.putText(frame, f"Thumb-Index Distance: {int(distance)}", (10, h - 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

                if distance < 30 and speed_zone != "brake":
                    print("Brake")
                    pyautogui.keyDown('down')
                    pyautogui.keyUp('up')
                    speed_zone = "brake"
                elif distance > 50 and speed_zone != "accelerate":
                    print("Accelerate")
                    pyautogui.keyDown('up')
                    pyautogui.keyUp('down')
                    speed_zone = "accelerate"
                elif 30 <= distance <= 50 and speed_zone != "neutral":
                    # Neither accelerate nor brake
                    pyautogui.keyUp('up')
                    pyautogui.keyUp('down')
                    print("Neutral Zone")
                    speed_zone = "neutral"

    cv2.imshow("Hand Control - Racing", frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
