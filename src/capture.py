import pathlib
import time
from typing import Any, List, Optional, Tuple

import cv2 as cv

from image import Images


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

    def run_capture(self, convert: bool = False) -> None:
        """Run caputering and image creating process"""
        # start camera
        cap: Any = cv.VideoCapture(0)
        # image counter
        image_count: int = 1

        duration: int
        interval: int
        # iterate intervals
        for duration, interval in self.intervals:
            # set start and end time in milliseconds
            start_time_ms: int = current_milli_time()
            current_time_ms: int = 0
            end_time_ms: int = duration
            ret: bool
            frame: Any
            while current_time_ms <= end_time_ms:
                # Create new image if break is over
                if current_time_ms % interval == 0:
                    ret, frame = cap.read()
                    # if image capturing is success
                    if ret:
                        # Create name
                        name: str = "%s%d%s" % (
                            self.images.pathname,
                            image_count,
                            self.images.file_ending,
                        )
                        if convert:
                            frame = Capture.convert_image_to_gray(frame)
                        # convert and save image to disk
                        self.images.save(frame, name)
                        image_count += 1

                # calc difference from start to now
                current_time_ms = current_milli_time() - start_time_ms

        # Release camera
        cap.release()

    def run_convert(self, replace: bool = False) -> List[Any]:
        """Read image files and batch convert them"""
        return self.images.batch_transform(
            Capture.convert_image_to_gray, replace, transform_suffix="_gray"
        )

    @classmethod
    def convert_image_to_gray(cls, image: Any) -> Any:
        """Convert image source to gray scale"""
        return cv.cvtColor(image, cv.COLOR_BGR2GRAY)
