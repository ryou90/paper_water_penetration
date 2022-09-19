import pathlib
from typing import Any, Callable, Iterator, List, Optional

import cv2 as cv

from paper_water_penetration.logger import get_logger

log = get_logger("batch_process")


def _batch_generator(path: str, pattern: str) -> Iterator[Any]:
    for child in pathlib.Path(path).rglob(pattern):  # "*%s" % self.file_ending
        yield child


def batch_read(path: str, pattern: str, gray: bool = True) -> List[Any]:
    """Reads all images from path"""
    from . import image
    images: List[Any] = []
    for child in _batch_generator(path, pattern):
        # Read images
        if gray:
            images.append(image.image_read_gray(str(child)))
        else:
            images.append(image.image_read(str(child)))
    return images


def batch_write(
    path: str,
    images: List[Any],
    filename: str = "DVM22_Penetration",
    suffix="",
    file_ending: str = ".png",
    gray: bool = True,
) -> None:
    from . import image

    count = 0
    if suffix == "" and gray:
        suffix = "_gray"

    image.create_path(path)

    for img in images:
        count += 1
        pathname: str = f"{path}{filename}_{count}{suffix}{file_ending}"

        if gray:
            cv.imwrite(pathname, image.image_to_gray(img))
        else:
            cv.imwrite(pathname, img)

    return


def batch_transform_from_path(
    transformer_fn: Callable,
    path: str,
    pattern: str,
    gray: bool = False,
) -> List[Any]:
    from . import image
    file: Any
    images = []

    for child in _batch_generator(path, pattern):
        # Read image
        if gray:
            file = image.image_read_gray(str(child))
        else:
            file = image.image_read(str(child))

        # Call transformer function
        file = transformer_fn(file)

        # Add transformed image to list
        images.append(file)

    return images


def batch_transform(
    transformer_fn: Callable,
    images: Optional[List[Any]] = None,
    path: Optional[str] = None,
    pattern: Optional[str] = None,
    gray: bool = False,
) -> List[Any]:
    """
    Executes transformer function to all images from path or data.
    """

    result: Any

    if path and pattern:
        result = batch_transform_from_path(transformer_fn, path, pattern, gray)
    elif images:
        result = batch_process(transformer_fn, images)
    else:
        raise ValueError("Neither list of images nor path and pattern are given!")

    return result


def batch_process(batch_fn: Callable, data: List[Any]) -> List[Any]:
    """Simply executes function to all data elements"""
    new_data = []
    for child in data:
        new_data.append(batch_fn(child))
    return new_data
