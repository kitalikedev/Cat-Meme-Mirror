# Real-Time Cat Meme Mirror 🐱

An interactive computer vision project using Google MediaPipe and OpenCV that tracks your facial expressions and hand gestures in real-time, matching them side-by-side with iconic cat memes.

<p align="center">
  <img src="memes/hmmmm.jpg" width="400" alt="Demo Cat Meme" />
</p>

## Features
- Real-time facial landmark tracking via MediaPipe Face Mesh (468 points).
- Gesture detection via MediaPipe Hands.
- Heuristic-based classification (Mouth Aspect Ratio, Eye Aspect Ratio, Smile Ratio).
- Debounced state transitions for jitter-free visual experience.

## Prerequisites
- Python **3.9 - 3.12** recommended.

## Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/kitalikedev/Cat-Meme-Mirror.git
cd Cat-Meme-Mirror
```

### 2. Create and activate a virtual environment
- **macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

- **Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate
```

- **Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
python src/main.py
```

> Press `q` to quit the application window.