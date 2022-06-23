import pathlib
from os.path import join
from typing import Any, Callable, List, Optional

import cv2 as cv


def get_current_path() -> str:
    return str(pathlib.Path(__file__).parent.absolute())


def create_path(path: str) -> None:
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)


class Images:
    filename: str = "DVM22_Penetration_"
    file_ending: str = ".jpg"

    def __init__(
        self,
        filename: Optional[str] = None,
        path: Optional[str] = None,
    ) -> None:
        """
        Configure instance
        """

        if filename:
            self.filename = filename

        self.path: str = path if path else get_current_path()
        create_path(self.path)

        self.fullname = pathlib.Path(self.path, self.filename)

        self._images: List[Any] = []

    @property
    def images(self) -> List[Any]:
        """Return cached list from last operation"""
        return self._images

    def batch_read(self) -> List[Any]:
        self._images = []
        for child in pathlib.Path(self.path).rglob("*%s" % self.file_ending):
            if child.is_file() and child.name.startswith(self.filename):
                # Read image
                self._images.append(cv.imread(str(child)))

        return self._images

    def batch_transform(
        self,
        transformer_fn: Callable,
        replace: bool = False,
        transform_suffix: str = "_transform",
    ) -> List[Any]:
        file: Any
        name: str
        self._images = []

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

    def save(self, image: Any, name: str) -> None:
        """Save frame as image with name"""
        # save image
        cv.imwrite(name, image)
