import pathlib
from functools import partial
from typing import Any, Callable, List, Optional

import cv2 as cv
import numpy as np

from batch_process import batch_read, batch_transform, batch_write
from logger import get_logger

log = get_logger("image")


def create_path(path: str) -> None:
    """Create Path if not exists"""
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)


def image_read(path: str) -> Any:
    """Read color image from path in BGR 3D array"""
    return cv.imread(path, cv.IMREAD_COLOR)


def image_read_gray(path: str) -> Any:
    """Read image from path as gray 2D array"""
    return cv.imread(path, cv.IMREAD_GRAYSCALE)


def image_write(image: Any, pathname: str) -> Any:
    """Write image to path"""
    create_path(pathname)
    cv.imwrite(pathname, image)


def image_to_gray(image: Any) -> Any:
    """Convert image source to gray scale"""
    return cv.cvtColor(image, cv.COLOR_BGR2GRAY)


def image_to_jet(image: Any) -> Any:
    """Convert image source to jet color map"""
    return cv.applyColorMap(image, cv.COLORMAP_JET)


def bgr_to_rgb(image: Any) -> Any:
    return cv.cvtColor(image, cv.COLOR_BGR2RGB)


def batch_convert_to_gray(
    images: Optional[List[Any]] = None,
    path: Optional[str] = None,
    pattern: Optional[str] = None,
) -> List[Any]:
    """Read image files and batch convert to gray"""
    return batch_transform(image_to_gray, images, path, pattern, True)


def batch_convert_to_jet(
    images: Optional[List[Any]] = None,
    path: Optional[str] = None,
    pattern: Optional[str] = None,
) -> List[Any]:
    """Read image files and batch convert to jet colormap"""
    return batch_transform(image_to_jet, images, path, pattern, True)


def batch_read_images(path: str, pattern: str) -> List[Any]:
    """Reads all images from path"""
    return batch_read(path, pattern, False)


def batch_read_images_gray(path: str, pattern: str) -> List[Any]:
    """Reads all images from path in gray"""
    return batch_read(path, pattern, True)


def batch_write_images(
    path: str,
    images: List[Any],
    filename: str = "DVM22_Penetration",
    suffix="",
    file_ending: str = ".png",
) -> None:
    """Batch write images to disk"""
    batch_write(path, images, filename, suffix, file_ending, False)


def batch_write_images_gray(
    path: str,
    images: List[Any],
    filename: str = "DVM22_Penetration",
    suffix="_gray",
    file_ending: str = ".png",
) -> None:
    """Batch write images to disk in gray"""
    batch_write(path, images, filename, suffix, file_ending, True)


def crop_square(image: Any, size: int):
    h, w = image.shape[:2]
    min_size = np.amin([h, w])

    # Centralize and crop
    crop_img = image[
        int(h / 2 - min_size / 2) : int(h / 2 + min_size / 2),
        int(w / 2 - min_size / 2) : int(w / 2 + min_size / 2),
    ]
    resized = cv.resize(crop_img, (size, size), interpolation=cv.INTER_AREA)

    return resized


def batch_resize(
    images: Optional[List[Any]] = None,
    path: Optional[str] = None,
    pattern: Optional[str] = None,
    new_size: int = 300,
) -> List[Any]:
    """Read image files and batch resize"""
    resize_fn: Callable = partial(crop_square, size=new_size)

    return batch_transform(resize_fn, images, path, pattern, False)
