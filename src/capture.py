import pathlib
import time
from typing import Any, List, Optional, Tuple

import cv2 as cv

from image import Images, image_to_gray
from logger import get_logger

log = get_logger("capture")

def current_milli_time() -> int:
    return int(round(time.time() * 1000))


class Capture:
    """
    This class collects all functions for capturing and converting of images.
    """

    def __init__(
        self,
        intervals: List[Tuple[int, int]] = [(1000, 100)],
        image_handler: Images = Images(),
        resize_scale: int = 50,
        filename: Optional[str] = None,
        path: Optional[str] = None,
    ) -> None:
        """
        Configure instance

        interval: List of Tuple(capture duration, break between two images)
        image_handler: Handler for image operations, can be customised
        """
        self.intervals = intervals
        self.images = image_handler

        # Set custom filename
        if filename:
            self.images.filename = filename

        # Set custom path
        if path:
            self.images.path = path

        self.resize_scale : int = resize_scale

    def run_capture(self, convert: bool = False) -> None:
        """Run caputering and image creating process"""
        log.debug("Capture process started")
        # image counter
        image_count: int = 1

        duration: int
        interval: int
        dimension : Tuple[int, int] = (0,0) #only used if resize
        # start camera
        cap: Any = cv.VideoCapture(0)
        log.debug("Camera started")

        if self.resize_scale:
            # get cap property
            width : int = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))   # convert float `width`
            height : int = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))  # convert float `height`

            # Create Resize dimensions
            new_width :int = int(width * self.resize_scale / 100)
            new_height : int = int(height * self.resize_scale / 100)
            dimension = (new_width, new_height)

        log.debug("Resize dimensions: %d x %d" % (new_width, new_height))
        images = []
        # iterate intervals
        for duration, interval in self.intervals:
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
                    log.debug("capture new frame")
                    # if image capturing is success
                    if ret:
                        # Create name
                        name: str = "%s%d%s" % (
                            self.images.pathname,
                            image_count,
                            self.images.file_ending,
                        )
                        log.debug("frame name: %s" % name)
                        images.append((name, frame))


                        if self.resize_scale:
                            log.debug("resize frame")
                            frame = cv.resize(frame, dimension)

                        if convert:
                            log.debug("convert frame")
                            frame = image_to_gray(frame)
                        # convert and save image to disk
                        log.debug("save frame")
                        self.images.save(frame, name)
                        image_count += 1

                # calc difference from start to now
                current_time_ms = current_milli_time() - start_time_ms

        # Release camera
        cap.release()

    def run_convert(self, replace: bool = False) -> List[Any]:
        """Read image files and batch convert them"""
        return self.images.batch_transform(
            image_to_gray, replace = replace, transform_suffix="_gray"
        )
