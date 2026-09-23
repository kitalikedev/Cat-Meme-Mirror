# Real-Time Cat Meme Mirror 🐱

An interactive computer vision project using Google MediaPipe and OpenCV that tracks your facial expressions and hand gestures in real-time, matching them side-by-side with iconic cat memes.

## Features
- Real-time facial landmark tracking via MediaPipe Face Mesh (468 points).
- Gesture detection via MediaPipe Hands.
- Heuristic-based classification (Mouth Aspect Ratio, Eye Aspect Ratio, Smile Ratio).
- Debounced state transitions for jitter-free visual experience.

## Installation & Setup
```bash
# Clone the repository
git clone <>
cd cat-meme-mirror

# Install dependencies
pip install -r requirements.txt

# Run the app
python main.py