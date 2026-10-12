# Gesture Assistant 🖐️

A Python-based, hands-free desktop controller that uses real-time hand tracking to interact with your computer through gestures.

## Features
- **Air Mouse:** Move the cursor using your index finger, with smoothing for more controlled movement.
- **Gesture Click:** Pinch your thumb and index finger to click and hold.
- **Volume Control:** Adjust system volume using hand gestures (thumbs up/ down).
- **Quick Actions:** Open Spotify and capture screenshots with specific gestures (peace and palm up gesture).
- **Toggle Control:** Enable or disable gesture-based controls using a hand (closed fist) gesture.

## Tech Stack
Python · OpenCV · MediaPipe · PyAutoGUI

## Getting Started

Install the dependencies:

```bash
pip install opencv-python mediapipe pyautogui
```

Run the script:

```bash
python main.py
```

Allow camera access when prompted. Press `q` in the camera window to exit.

**Note:** System volume control uses macOS-specific AppleScript commands, so this feature requires macOS.

## How It Works
OpenCV captures live camera frames, MediaPipe detects hand landmarks, and Python interprets their positions to trigger cursor movements and system actions.

Built as a hands-on project to explore computer vision, gesture recognition, and desktop automation.