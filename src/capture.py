import pathlib
import time
from os import listdir
from os.path import isfile, join
from typing import Any, List, Optional, Tuple

import cv2 as cv


def current_milli_time() -> int:
    return int(round(time.time() * 1000))


def get_current_path() -> str:
    return str(pathlib.Path(__file__).parent.absolute())


def create_path(path: str) -> None:
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)


class Capture:
    """
    This class collects all functions for capturing and converting of images.
    """

    filename: str = "DVM22_Penetration_"
    file_ending: str = ".jpg"

    def __init__(
        self,
        intervals: List[Tuple[int, int]] = [(1000, 100)],
        filename: Optional[str] = None,
        path: Optional[str] = None,
    ) -> None:
        """
        Configure instance

        interval: List of Tuple(capture duration, break between two images)
        """
        self.intervals = intervals
        if filename:
            self.filename = filename

        self.path: str = path if path else get_current_path()
        create_path(self.path)

        self.fullname = pathlib.Path(self.path, self.filename)

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
                            self.fullname,
                            image_count,
                            self.file_ending,
                        )
                        if convert:
                            frame = Capture.convert_image_to_gray(frame)
                        # convert and save image to disk
                        Capture.save_image(frame, name)
                        image_count += 1

                # calc difference from start to now
                current_time_ms = current_milli_time() - start_time_ms

        # Release camera
        cap.release()

    def run_convert(self, replace: bool = False) -> None:
        """Read image files and batch convert them"""
        # First get all file names
        files = [
            join(self.path, f)
            for f in listdir(self.path)
            if isfile(join(self.path, f)) and f.startswith(self.filename)
        ]

        file: Any
        name: str
        for child in pathlib.Path(self.path).rglob("*%s" % self.file_ending):
            if child.is_file() and child.name.startswith(self.filename):
                # Read image
                file = cv.imread(str(child))
                # if replace image with converted image
                if replace:
                    # convert and replace image data
                    name = child.name
                else:
                    # create new name from child
                    name = join(
                        self.path,
                        child.name.replace(self.file_ending, ""),
                        "_gray",
                        self.file_ending,
                    )
                    Capture.save_image(Capture.convert_image_to_gray(file), name)

    @classmethod
    def save_image(cls, frame: Any, name: str) -> None:
        """Save frame as image with name"""
        # save image
        cv.imwrite(name, frame)

    @classmethod
    def convert_image_to_gray(cls, image: Any) -> Any:
        """Convert image source to gray scale"""
        return cv.cvtColor(image, cv.COLOR_BGR2GRAY)
