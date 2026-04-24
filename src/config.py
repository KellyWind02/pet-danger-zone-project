from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

MODEL_PATH = PROJECT_ROOT / "weights" / "yolov8n.pt"
INPUT_VIDEO = PROJECT_ROOT / "demo_videos" / "input" / "demo.mp4"
OUTPUT_VIDEO = PROJECT_ROOT / "demo_videos" / "output" / "demo_result.mp4"
LOG_PATH = PROJECT_ROOT / "results" / "logs" / "event_log.csv"

CONF_THRESHOLD = 0.25
STAY_THRESHOLD_FRAMES = 60

# ROI format: (x1, y1, x2, y2)
ROI = (100, 80, 420, 260)
PET_CLASSES = {"cat", "dog"}
