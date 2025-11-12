# Game Control using Gestures (OpenCV + MediaPipe)

## Project Overview

This project uses a webcam, OpenCV and MediaPipe to implement hand-gesture controls for racing games (for example, Asphalt running in an emulator or PC). The program tracks a single hand, draws a simple skeleton for debugging, and maps gestures to keyboard inputs using `pyautogui`.

Key features

* Real-time hand tracking via MediaPipe.
* Visual skeleton (landmarks and connections) drawn on the feed.
* Steering based on palm horizontal position (left / centre / right zones).
* Acceleration and braking are controlled by the distance between the thumb tip (landmark 4) and index tip (landmark 8).
* Simple on-screen debug info for thresholds and distances.

---

## Files

* `app.py`
  Main Python script implementing hand tracking and keyboard control.

* `README.d`
  This documentation file.

---

## Requirements

* Python 3.8+ recommended
* Packages (install via pip):

  ```bash
  pip install opencv-python mediapipe pyautogui
  ```

Notes:

* On Windows, `pyautogui` may require additional permissions if the target game runs with elevated privileges.
* For stable MediaPipe performance, run in a well-lit environment and avoid busy backgrounds.

---

## How It Works (high-level)

1. Capture video frames from the default webcam using OpenCV.
2. Convert frames to RGB and feed them to MediaPipe Hands for landmark detection.
3. Build a list of (x, y) pixel coordinates for each landmark.
4. Draw landmarks and connections on the frame for visual feedback.
5. Compute palm horizontal position (x) and compare it to left/right thresholds to decide steering.
6. Compute the Euclidean distance between the thumb tip (landmark 4) and the index tip (landmark 8). Use that distance to choose brake/neutral/accelerate states.
7. Use `pyautogui` to press or release arrow keys based on gesture state.

---

## Controls / Mappings

* **Mapping**
* <img width="639" height="514" alt="Image" src="https://github.com/user-attachments/assets/1dc9b707-ad5e-45df-bd91-cfa978517c55" />

* <img width="638" height="517" alt="Image" src="https://github.com/user-attachments/assets/5d4f7a0f-d860-4d13-bc11-89b1a86db267" />
    
* **Steering**

  * Left movement means the points numbered 8 and 4 should move farther left from the particular distance from the centre
  * Right movement means the points numbered 8 and 4 should move farther right from the particular distance from the centre
  * Keep hand in centre zone → release left/right keys (neutral)

* **Speed control (thumb-index distance)**

  * Distance < 30 px → `Down Arrow` (brake)
  * Distance between 30 and 50 px → neutral (no up/down keys)
  * Distance > 50 px → `Up Arrow` (accelerate)

  **Demo Vedio**
  https://github.com/user-attachments/assets/1a494e15-eb2b-46d7-bdf3-4a9fb6ff7cb9
---

## Configuration / Tuning

* Resolution is set in the script:

  ```python
  cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
  ```

  Lower resolution reduces CPU load and may increase responsiveness.

* Thresholds to edit (in `app.py`):

  * `left_thresh` and `right_thresh` control steering zones. Default values in the code are tuned for 640x480.
  * `distance` thresholds (`30`, `50`) control brake/neutral/accelerate. Increase if your hand is farther from the camera.

* MediaPipe tuning:

  * `min_detection_confidence` and `min_tracking_confidence` can be adjusted for speed vs reliability.

---


## Author

Your name here
