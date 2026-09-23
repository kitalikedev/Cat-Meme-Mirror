import math
from config import (
    MAR_WTF_THRESHOLD,
    MAR_SURPRISE_THRESHOLD,
    MAR_TONGUE_OPEN_THRESHOLD,
    MAR_TIGHT_LIP_THRESHOLD,
    SMILE_RATIO_THRESHOLD,
)

class ExpressionClassifier:
    """
    Computes biometric facial features and hand gestures to match meme states.
    """

    @staticmethod
    def _euclidean_distance(p1, p2):
        return math.hypot(p1.x - p2.x, p1.y - p2.y)

    @classmethod
    def calculate_mar(cls, lm):
        """Mouth Aspect Ratio: vertical lip distance over horizontal."""
        mouth_height = cls._euclidean_distance(lm[13], lm[14])
        mouth_width = cls._euclidean_distance(lm[61], lm[291])
        return mouth_height / (mouth_width + 1e-6)

    @classmethod
    def calculate_smile_metrics(cls, lm):
        """Measures mouth width and upward elevation of lip corners."""
        mouth_width = cls._euclidean_distance(lm[61], lm[291])
        eye_width = cls._euclidean_distance(lm[33], lm[263])
        width_ratio = mouth_width / (eye_width + 1e-6)

        avg_corner_y = (lm[61].y + lm[291].y) / 2.0
        lip_center_y = lm[0].y
        corner_lift = lip_center_y - avg_corner_y

        return width_ratio, corner_lift

    @classmethod
    def is_thumb_up(cls, hand_lm):
        """
        Detects thumbs up gesture:
        Thumb tip (4) is significantly higher (lower y) than thumb MCP (2),
        and other 4 fingers are curled down (tips lower than PIP joints).
        """
        # Thumb: tip 4 is higher than joint 2
        thumb_is_up = hand_lm[4].y < hand_lm[2].y

        # Other 4 fingers curled in: tip y is below (larger y) pip joints
        fingers_curled = (
            hand_lm[8].y > hand_lm[6].y and    # Index
            hand_lm[12].y > hand_lm[10].y and  # Middle
            hand_lm[16].y > hand_lm[14].y and  # Ring
            hand_lm[20].y > hand_lm[18].y      # Pinky
        )

        return thumb_is_up and fingers_curled

    @classmethod
    def classify(cls, landmarks, hand_landmarks=None, prev_state="normal"):
        """
        Hierarchical classification matching the meme priority.
        """
        mar = cls.calculate_mar(landmarks)
        width_ratio, corner_lift = cls.calculate_smile_metrics(landmarks)

        # 1. Hand gesture priorities
        if hand_landmarks:
            if cls.is_thumb_up(hand_landmarks):
                return "thumbs_up"
            if mar > MAR_TONGUE_OPEN_THRESHOLD:
                return "silly_hand"
            return "punch"

        # 2. Extreme shock -> WTF Miles Morales
        if mar > MAR_WTF_THRESHOLD:
            return "wtf"

        # 3. Standard open mouth shock -> Surprise cat
        if mar > MAR_SURPRISE_THRESHOLD:
            return "surprised"

        # 4. Smile with Hysteresis
        if prev_state == "smile":
            is_smiling = (width_ratio > SMILE_RATIO_THRESHOLD - 0.05) and (corner_lift > -0.015)
        else:
            is_smiling = (width_ratio > SMILE_RATIO_THRESHOLD) and (corner_lift > -0.005)

        if is_smiling and mar < 0.35:
            return "smile"

        # 5. Pressed tight lips -> Ummm cat
        if mar < MAR_TIGHT_LIP_THRESHOLD:
            return "ummm"

        # 6. Default
        return "normal"