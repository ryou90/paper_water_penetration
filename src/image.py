import pathlib
from os.path import join
from typing import Any, Callable, Iterator, List, Optional

import cv2 as cv

from logger import get_logger

log = get_logger("image")

def get_current_path() -> str:
    return str(pathlib.Path(__file__).parent.absolute())


def create_path(path: str) -> None:
    """Create Path if not exists"""
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)


def image_read(path: str) -> Any:
    """Read color image from path in BGR 3D array"""
    return cv.imread(path)

def image_read_gray(path: str) -> Any:
    """Read image from path as gray 2D array"""
    return cv.imread(path, 0)

def image_write(image: Any, pathname: str) -> Any:
    """Write image to path"""
    cv.imwrite(pathname, image)

def image_to_gray(image: Any) -> Any:
    """Convert image source to gray scale"""
    return cv.cvtColor(image, cv.COLOR_BGR2GRAY)

def bgr_to_rgb(image: Any) -> Any:
    return cv.cvtColor(image, cv.COLOR_BGRA2RGB)


class Images:
    default_filename: str = "DVM22_Penetration_"
    file_ending: str = ".png"

    def __init__(
        self,
        filename: Optional[str] = None,
        path: Optional[str] = None,
    ) -> None:
        """
        Configure instance
        """
        self._path: str = ""
        self._filename: str = ""

        self.filename = filename if filename else self.default_filename
        self.path = path if path else get_current_path()
        self._images: List[Any] = []

    @property
    def path(self) -> str:
        """Return path"""
        return self._path

    @path.setter
    def path(self, value: str) -> None:
        self._path = value
        create_path(self._path)

        self.pathname = pathlib.Path(self._path, self.filename)

    @property
    def filename(self) -> str:
        """Return filename"""
        return self._filename

    @filename.setter
    def filename(self, value: str) -> None:
        self._filename = value
        self.pathname = pathlib.Path(self.path, self._filename)

    @property
    def images(self) -> List[Any]:
        """Return cached list from last operation"""
        return self._images

    def _batch_generator(self) -> Iterator[Any]:
        for child in pathlib.Path(self.path).rglob("*%s" % self.file_ending):
            if child.is_file() and child.name.startswith(self.filename):
                yield child

    def batch_read(self, gray: bool = True) -> List[Any]:
        """Reads all images from path"""
        self._images = []
        for child in self._batch_generator():
            # Read images
            if gray:
                self._images.append(image_read_gray(str(child)))
            else:
                self._images.append(image_read(str(child)))

        return self._images

    def batch_transform(
        self,
        transformer_fn: Callable,
        image_list: Optional[List[Any]] = None,
        replace: bool = False,
        transform_suffix: str = "_transform",
    ) -> List[Any]:
        """
        Executes transformer function to all images from path.
        Save transformed images.
        """
        file: Any
        name: str
        self._images = []

        iterator: Any = image_list if image_list else self._batch_generator()
        for child in iterator:
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
                    transform_suffix,
                    self.file_ending,
                )

                # Call transformer function
                file = transformer_fn(file)
                # Add transformed image to list
                self._images.append(file)
                # save image
                self.save(file, name)

        # return list
        return self._images

    def batch_process(
        self, batch_fn: Callable, image_list: Optional[List[Any]] = None
    ) -> List[Any]:
        """Simply executes function to all images from path"""
        self._images = []
        iterator: Any = image_list if image_list else self._batch_generator()
        for child in iterator:
            self._images.append(batch_fn(child))

        return self._images

    def save(self, image: Any, name: str) -> None:
        """Save frame as image with name"""
        # save image
        self._images.append(image)
        image_write(image, name)
