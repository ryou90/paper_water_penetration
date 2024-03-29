from math import cos, sin
from typing import Any, List

import numpy as np
from scipy.optimize import curve_fit

from paper_water_penetration.batch_process import batch_process
from paper_water_penetration.logger import get_logger

log = get_logger("transformer")


np.seterr(divide="ignore")
np.seterr(invalid="ignore")


def fft2_transformer(image: Any) -> Any:
    """Shift and Fast Fourier Transformation"""
    f: Any = np.fft.fft2(image)
    fshift: Any = np.fft.fftshift(f)
    return np.log(np.abs(fshift))


def batch_fft2_transform(image_list: List[Any]) -> List[Any]:
    """
    Batch fft transform all images previously created
    or by list of images
    """
    return batch_process(
        batch_fn=fft2_transformer,
        data=image_list,
    )


def calc_radial_profile(data):
    """Calculate Radial Profile"""
    (h, w) = data.shape[:2]
    center = (w // 2, h // 2)
    # x, y for
    y, x = np.indices((data.shape))
    # create radius steps and reverse order
    radius = np.arange(0,x.max()/2,2)[::-1]

    rad = np.radians(np.arange(90))
    # x = math.cos(xr)
    # y = math.sin(xr)
    profile = []
    for r in radius:
        xy = np.around(r *np.array([[sin(xr), cos(xr)] for xr in rad])).astype(int)
        # Get circle data values and calc mean
        profile.append(np.array([data[coord[0], coord[1]] for coord in xy]).mean())

    # Convert back to numpy array
    return np.asarray(profile)


def batch_calc_radial_profile(image_list: List[Any]) -> List[Any]:
    """
    Batch calculate radial profile of all images previously created
    or by list of images
    """
    return batch_process(
        batch_fn=calc_radial_profile,
        data=image_list,
    )