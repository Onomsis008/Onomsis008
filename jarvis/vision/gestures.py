import cv2
import numpy as np
import os
import sys

# Attempt to import mediapipe and its solutions
try:
    import mediapipe as mp
    from mediapipe.python.solutions import hands as mp_hands
    from mediapipe.python.solutions import face_mesh as mp_face_mesh
    from mediapipe.python.solutions import drawing_utils as mp_draw
    MEDIAPIPE_AVAILABLE = True
except (ImportError, AttributeError):
    MEDIAPIPE_AVAILABLE = False

# Optional import for pyautogui to avoid crash in headless environments
PYAUTOGUI_AVAILABLE = False
if "DISPLAY" in os.environ:
    try:
        import pyautogui
        PYAUTOGUI_AVAILABLE = True
    except ImportError:
        pass

class VisionSystem:
    def __init__(self):
        if MEDIAPIPE_AVAILABLE:
            # Initialize MediaPipe Hands
            self.hands = mp_hands.Hands(
                static_image_mode=False,
                max_num_hands=1,
                min_detection_confidence=0.7,
                min_tracking_confidence=0.5
            )

            # Initialize MediaPipe Face Mesh for eye tracking
            self.face_mesh = mp_face_mesh.FaceMesh(
                max_num_faces=1,
                refine_landmarks=True,
                min_detection_confidence=0.7,
                min_tracking_confidence=0.5
            )

        if PYAUTOGUI_AVAILABLE:
            self.screen_width, self.screen_height = pyautogui.size()
        else:
            self.screen_width, self.screen_height = 1920, 1080

        # Landmarks for eyes (MediaPipe Face Mesh)
        self.LEFT_EYE = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
        self.RIGHT_EYE = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
        self.LEFT_IRIS = [474, 475, 476, 477]
        self.RIGHT_IRIS = [469, 470, 471, 472]

        self.last_iris_pos = None

    def process_gestures(self, frame):
        """Processes hand gestures for mouse control."""
        if not MEDIAPIPE_AVAILABLE:
            return "Vision module not available"

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Get index finger tip (8) and thumb tip (4)
                index_tip = hand_landmarks.landmark[8]
                thumb_tip = hand_landmarks.landmark[4]

                # Screen coordinates
                x = int(index_tip.x * self.screen_width)
                y = int(index_tip.y * self.screen_height)

                if PYAUTOGUI_AVAILABLE:
                    # Smooth movement
                    pyautogui.moveTo(x, y, _pause=False)

                    # Simple click gesture: distance between thumb and index tip
                    distance = np.sqrt((index_tip.x - thumb_tip.x)**2 + (index_tip.y - thumb_tip.y)**2)
                    if distance < 0.05:
                        pyautogui.click()
                        return "Click Detected"

                return f"Moving to {x}, {y}"
        return "No hand detected"

    def process_eyes(self, frame):
        """Processes eye movement/gaze for scrolling."""
        if not MEDIAPIPE_AVAILABLE:
            return "Eye tracking not available"

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            mesh_coords = results.multi_face_landmarks[0].landmark
            # Get iris center
            left_iris_center = np.mean([[mesh_coords[i].x, mesh_coords[i].y] for i in self.LEFT_IRIS], axis=0)

            if self.last_iris_pos is not None and PYAUTOGUI_AVAILABLE:
                # Detect vertical movement for scrolling
                dy = left_iris_center[1] - self.last_iris_pos[1]
                if dy > 0.01: # Looking down
                    pyautogui.scroll(-10)
                    status = "Scrolling Down"
                elif dy < -0.01: # Looking up
                    pyautogui.scroll(10)
                    status = "Scrolling Up"
                else:
                    status = "Eyes steady"
            else:
                status = "Eyes tracked"

            self.last_iris_pos = left_iris_center
            return status

        return "No face detected"

    def run_vision_loop(self):
        """Generator that yields status from camera frames."""
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            yield "Error: Could not open camera."
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Flip frame for natural movement
            frame = cv2.flip(frame, 1)

            gesture_status = self.process_gestures(frame)
            eye_status = self.process_eyes(frame)

            yield f"Vision: {gesture_status} | {eye_status}"

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
