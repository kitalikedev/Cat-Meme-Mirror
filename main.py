import cv2
import mediapipe as mp
import numpy as np
import os
from collections import deque, Counter

import config
from classifier import ExpressionClassifier

def load_meme_assets():
    """Preloads and resizes meme assets."""
    loaded_memes = {}
    for state, filename in config.MEME_MAP.items():
        img_path = os.path.join(config.MEME_DIR, filename)
        img = cv2.imread(img_path)

        if img is None:
            print(f"[WARN] Failed to load {filename}, creating placeholder.")
            img = np.zeros((config.FRAME_HEIGHT, config.FRAME_WIDTH, 3), dtype=np.uint8)
            cv2.putText(img, f"Missing: {filename}", (40, 250), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        else:
            img = cv2.resize(img, (config.FRAME_WIDTH, config.FRAME_HEIGHT))
            
        loaded_memes[state] = img
    return loaded_memes

def main():
    meme_assets = load_meme_assets()
    state_buffer = deque(maxlen=config.SMOOTHING_BUFFER_SIZE)

    mp_face_mesh = mp.solutions.face_mesh
    mp_hands = mp.solutions.hands

    face_mesh = mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.6,
        min_tracking_confidence=0.6
    )
    hands = mp_hands.Hands(
        max_num_hands=1,
        min_detection_confidence=0.6,
        min_tracking_confidence=0.6
    )

    cap = cv2.VideoCapture(0)
    current_state = "normal"
    debug_info = ""

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        face_results = face_mesh.process(rgb_frame)
        hand_results = hands.process(rgb_frame)

        hand_lms = None
        if hand_results.multi_hand_landmarks:
            hand_lms = hand_results.multi_hand_landmarks[0].landmark

        raw_state = "normal"

        if face_results.multi_face_landmarks:
            face_lms = face_results.multi_face_landmarks[0].landmark
            raw_state = ExpressionClassifier.classify(
                face_lms, 
                hand_landmarks=hand_lms, 
                prev_state=current_state
            )

            mar = ExpressionClassifier.calculate_mar(face_lms)
            w_ratio, lift = ExpressionClassifier.calculate_smile_metrics(face_lms)
            debug_info = f"MAR:{mar:.2f} | Smile:{w_ratio:.2f} | Lift:{lift:.3f}"

        # Sliding window smoothing
        state_buffer.append(raw_state)
        current_state = Counter(state_buffer).most_common(1)[0][0]

        # Left Panel (User)
        left_panel = cv2.resize(frame, (config.FRAME_WIDTH, config.FRAME_HEIGHT))
        cv2.putText(left_panel, f"State: {current_state.upper()}", (20, 45), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 255, 120), 2, cv2.LINE_AA)
        
        if debug_info:
            cv2.putText(left_panel, debug_info, (15, config.FRAME_HEIGHT - 20), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.48, (220, 220, 220), 1, cv2.LINE_AA)

        # Right Panel (Meme)
        right_panel = meme_assets.get(current_state, meme_assets["normal"])

        # Display side-by-side
        canvas = np.hstack((left_panel, right_panel))
        cv2.line(canvas, (config.FRAME_WIDTH, 0), (config.FRAME_WIDTH, config.FRAME_HEIGHT), 
                 (255, 255, 255), 2)

        cv2.imshow(config.WINDOW_NAME, canvas)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()