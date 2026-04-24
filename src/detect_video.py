from __future__ import annotations

import sys
from pathlib import Path

import cv2
from ultralytics import YOLO

from config import (
    CONF_THRESHOLD,
    INPUT_VIDEO,
    MODEL_PATH,
    OUTPUT_VIDEO,
    PET_CLASSES,
    ROI,
    STAY_THRESHOLD_FRAMES,
)
from roi_rules import RoiTracker
from utils import ensure_parent_dir, format_timestamp, get_box_center
from visualize import draw_detection, draw_roi, draw_status


def select_best_pet_detection(results, model_names: dict[int, str]):
    best_detection = None

    for box in results.boxes:
        class_id = int(box.cls[0].item())
        class_name = model_names.get(class_id, "")
        if class_name not in PET_CLASSES:
            continue

        confidence = float(box.conf[0].item())
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
        detection = {
            "label": "pet",
            "confidence": confidence,
            "bbox": (x1, y1, x2, y2),
        }
        if best_detection is None or confidence > best_detection["confidence"]:
            best_detection = detection

    return best_detection


def main() -> int:
    if not INPUT_VIDEO.exists():
        print(f"Input video not found: {INPUT_VIDEO}")
        print("Please update INPUT_VIDEO in src/config.py before running.")
        return 1

    ensure_parent_dir(OUTPUT_VIDEO)

    model = YOLO(str(MODEL_PATH))
    cap = cv2.VideoCapture(str(INPUT_VIDEO))
    if not cap.isOpened():
        print(f"Failed to open video: {INPUT_VIDEO}")
        return 1

    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    writer = cv2.VideoWriter(
        str(OUTPUT_VIDEO),
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height),
    )

    roi_tracker = RoiTracker(ROI, STAY_THRESHOLD_FRAMES)
    frame_index = 0

    while True:
        success, frame = cap.read()
        if not success:
            break

        result = model.predict(frame, conf=CONF_THRESHOLD, verbose=False)[0]
        detection = select_best_pet_detection(result, model.names)

        center_point = None
        if detection is not None:
            center_point = get_box_center(detection["bbox"])

        state = roi_tracker.update(center_point)
        draw_roi(frame, ROI, state.status_text)
        draw_status(frame, state.status_text, state.stay_count)

        if detection is not None:
            draw_detection(
                frame,
                detection["bbox"],
                detection["label"],
                detection["confidence"],
                state.status_text,
            )
            cv2.circle(frame, center_point, 4, (255, 255, 255), -1)

        writer.write(frame)
        frame_index += 1

        if frame_index % 30 == 0:
            print(
                f"Processed frame {frame_index} "
                f"({format_timestamp(frame_index, fps)}), status={state.status_text}"
            )

    cap.release()
    writer.release()
    cv2.destroyAllWindows()

    print(f"Output video saved to: {OUTPUT_VIDEO}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
