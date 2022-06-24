from typing import Any, List, Optional

import numpy as np

from image import Images

np.seterr(divide="ignore")
np.seterr(invalid="ignore")


def fft_transformer(image: Any) -> Any:
    """Shift and Fast Fourier Transformation"""
    f: Any = np.fft.fft2(image)
    fshift: Any = np.fft.fftshift(f)
    return 20 * np.log(np.abs(fshift))


def batch_fft_transform(
    image_handler: Images, image_list: Optional[List[Any]] = None, save: bool = False
) -> List[Any]:
    """
    Batch fft transform all images previously created
    or by list of images
    """
    if save:
        return image_handler.batch_transform(
            transformer_fn=fft_transformer,
            image_list=image_list,
            transform_suffix="_fft",
        )
    else:
        return image_handler.batch_process(
            batch_fn=fft_transformer,
            image_list=image_list,
        )


def calc_radial_profile(data):
    """Calculate Radial Profile"""
    (h, w) = data.shape[:2]
    center = (w//2, h//2)
    y, x = np.indices((data.shape))
    r = np.sqrt((x - center[0]) ** 2 + (y - center[1]) ** 2)
    r = r.astype(np.int_)

    tbin = np.bincount(r.ravel(), data.ravel())
    nr = np.bincount(r.ravel())
    radialprofile = tbin / nr
    return radialprofile


def batch_calc_radial_profile(
    image_handler: Images, image_list: Optional[List[Any]] = None
) -> List[Any]:
    """
    Batch calculate radial profile of all images previously created
    or by list of images
    """
    return image_handler.batch_process(
        batch_fn=calc_radial_profile,
        image_list=image_list,
    )
