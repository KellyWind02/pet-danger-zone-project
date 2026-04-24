from dataclasses import dataclass


Roi = tuple[int, int, int, int]
Point = tuple[int, int]


def point_in_roi(point: Point, roi: Roi) -> bool:
    x, y = point
    x1, y1, x2, y2 = roi
    return x1 <= x <= x2 and y1 <= y <= y2


@dataclass
class RoiEventState:
    intrusion: bool
    abnormal_stay: bool
    stay_count: int
    status_text: str


class RoiTracker:
    def __init__(self, roi: Roi, stay_threshold_frames: int) -> None:
        self.roi = roi
        self.stay_threshold_frames = stay_threshold_frames
        self.stay_count = 0

    def reset(self) -> RoiEventState:
        self.stay_count = 0
        return RoiEventState(
            intrusion=False,
            abnormal_stay=False,
            stay_count=0,
            status_text="safe",
        )

    def update(self, point: Point | None) -> RoiEventState:
        if point is None or not point_in_roi(point, self.roi):
            return self.reset()

        self.stay_count += 1
        abnormal_stay = self.stay_count >= self.stay_threshold_frames
        status_text = "abnormal_stay" if abnormal_stay else "intrusion"
        return RoiEventState(
            intrusion=True,
            abnormal_stay=abnormal_stay,
            stay_count=self.stay_count,
            status_text=status_text,
        )
