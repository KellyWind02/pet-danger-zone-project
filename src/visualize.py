import cv2


SAFE_COLOR = (0, 255, 0)
INTRUSION_COLOR = (0, 255, 255)
ABNORMAL_COLOR = (0, 0, 255)


def get_status_color(status_text: str) -> tuple[int, int, int]:
    if status_text == "abnormal_stay":
        return ABNORMAL_COLOR
    if status_text == "intrusion":
        return INTRUSION_COLOR
    return SAFE_COLOR


def draw_roi(frame, roi: tuple[int, int, int, int], status_text: str) -> None:
    x1, y1, x2, y2 = roi
    color = get_status_color(status_text)
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
    cv2.putText(
        frame,
        f"ROI: {status_text}",
        (x1, max(25, y1 - 10)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        color,
        2,
        cv2.LINE_AA,
    )


def draw_detection(
    frame,
    bbox: tuple[int, int, int, int],
    label: str,
    confidence: float,
    status_text: str,
) -> None:
    x1, y1, x2, y2 = bbox
    color = get_status_color(status_text)
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
    cv2.putText(
        frame,
        f"{label} {confidence:.2f}",
        (x1, max(25, y1 - 10)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        color,
        2,
        cv2.LINE_AA,
    )


def draw_status(frame, status_text: str, stay_count: int) -> None:
    color = get_status_color(status_text)
    message = f"Status: {status_text}"
    if status_text != "safe":
        message += f" | stay_count={stay_count}"

    cv2.putText(
        frame,
        message,
        (20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        color,
        2,
        cv2.LINE_AA,
    )
