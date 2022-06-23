import pathlib
from os.path import join
from typing import Any, Callable, Iterator, List, Optional

import cv2 as cv


def get_current_path() -> str:
    return str(pathlib.Path(__file__).parent.absolute())


def create_path(path: str) -> None:
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)


class Images:
    default_filename: str = "DVM22_Penetration_"
    file_ending: str = ".jpg"

    def __init__(
        self,
        filename: Optional[str] = None,
        path: Optional[str] = None,
    ) -> None:
        """
        Configure instance
        """

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

    def batch_read(self) -> List[Any]:
        """Reads all images from path"""
        self._images = []
        for child in self._batch_generator():
            # Read image
            self._images.append(cv.imread(str(child)))

        return self._images

    def batch_transform(
        self,
        transformer_fn: Callable,
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

        for child in self._batch_generator():
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
        self,
        batch_fn: Callable,
    ) -> None:
        """Simply executes function to all images from path"""
        for child in self._batch_generator():
            batch_fn(child)

    def save(self, image: Any, name: str) -> None:
        """Save frame as image with name"""
        # save image
        cv.imwrite(name, image)
