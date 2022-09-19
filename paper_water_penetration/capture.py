import time
from typing import Any, List, Tuple

import cv2 as cv

from paper_water_penetration.logger import get_logger, logging

log = get_logger("capture")
log.setLevel(logging.INFO)

def current_milli_time() -> int:
    return int(round(time.time() * 1000))


def capture(
    intervals: List[Tuple[int, int]] = [(1000, 100)],
    resolution: Tuple[int, int] = (640, 480),
    wait: bool = False
) -> List[Any]:
    """
    Run caputering and image creating process

    Configure instance
    interval: List of Tuple(capture duration, break between two images)
    """
    log.debug("Capture process started")
    # image counter
    image_count: int = 1

    duration: int
    interval: int

    images: List[Any] = []
    # start camera
    cap: Any = cv.VideoCapture(0)
    log.debug("Camera started")

    # Set new resolution
    cap.set(cv.CAP_PROP_FRAME_WIDTH, resolution[0])
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, resolution[1])

    log.debug(
        "Resize dimensions: %d x %d"
        % (
            cap.get(cv.CAP_PROP_FRAME_WIDTH),
            cap.get(cv.CAP_PROP_FRAME_HEIGHT),
        )
    )

    if wait:
        input("Ready for capturing, press Enter to continue...")

    # iterate intervals
    for duration, interval in intervals:
        log.debug("Start interval: Duration: %d, interval: %d" % (duration, interval))
        # set start and end time in milliseconds
        start_time_ms: int = current_milli_time()
        current_time_ms: int = 0
        end_time_ms: int = duration
        ret: bool
        frame: Any
        while current_time_ms <= end_time_ms:
            # Create new image if break is over
            log.debug(f"{current_time_ms} {interval}")
            if current_time_ms % interval == 0:
                ret, frame = cap.read()
                log.info(f"Capture new frame: {image_count}")
                # if image capturing is success
                if ret:
                    image_count += 1
                    log.debug(f"Cached new frame {image_count}")
                    images.append(frame)

            # calc difference from start to now
            current_time_ms = current_milli_time() - start_time_ms

    # Release camera
    cap.release()

    return images
