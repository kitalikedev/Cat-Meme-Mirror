import os

# --- Layout Configuration ---
FRAME_WIDTH = 550
FRAME_HEIGHT = 550
WINDOW_NAME = "Meme Mirror: You vs Cat Meme"

# --- Asset Paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEME_DIR = os.path.join(BASE_DIR, "memes")

# Mapping expression states to exact filenames
MEME_MAP = {
    "normal": "hmmmm.jpg",        # Relaxed / default face
    "smile": "flowers.jpg",        # Smiling
    "thumbs_up": "nice.jpg",       # Thumb up gesture 👍
    "silly_hand": "ye.jpg",        # Hand up + mouth open/tongue
    "punch": "punch.jpg",          # Fist / hand close to face
    "surprised": "suprise.jpg",    # Open mouth surprise
    "wtf": "wtf.jpg",              # Extreme wide jaw shock
    "ummm": "ummm.jpg",            # Tight pressed lips / awkward
}

# --- Threshold Tuning Parameters ---
MAR_WTF_THRESHOLD = 0.55          # Extreme mouth drop
MAR_SURPRISE_THRESHOLD = 0.38     # Moderate mouth open
MAR_TONGUE_OPEN_THRESHOLD = 0.16  # Slight mouth parting for tongue/silly
MAR_TIGHT_LIP_THRESHOLD = 0.08    # Tightly compressed lips for 'ummm'

SMILE_RATIO_THRESHOLD = 0.56

# Smoothing buffer size
SMOOTHING_BUFFER_SIZE = 7