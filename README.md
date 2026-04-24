# Pet Danger Zone Project

Minimal EE5811 project scaffold for:

- pet detection with `YOLOv8n`
- rectangular ROI intrusion judgment
- annotated output video with `safe` / `intrusion` / `abnormal_stay`

## Quick Start

1. Put a test video at `demo_videos/input/demo.mp4`
2. Put `yolov8n.pt` at `weights/yolov8n.pt`
3. Update `src/config.py` if needed
4. Run:

```bash
cd /Users/xuwenyi/Temp/pet-danger-zone-project/src
python detect_video.py
```

Output video is written to `demo_videos/output/demo_result.mp4`.
