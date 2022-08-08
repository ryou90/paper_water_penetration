from typing import Any, List

import numpy as np
from scipy.optimize import curve_fit

from batch_process import batch_process
from logger import get_logger

log = get_logger("transformer")


np.seterr(divide="ignore")
np.seterr(invalid="ignore")


def fft2_transformer(image: Any) -> Any:
    """Shift and Fast Fourier Transformation"""
    f: Any = np.fft.fft2(image)
    fshift: Any = np.fft.fftshift(f)
    return 20 * np.log(np.abs(fshift))


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
    y, x = np.indices((data.shape))

    r = np.sqrt((x - center[0]) ** 2 + (y - center[1]) ** 2)
    r = r.astype(np.int_)

    tbin = np.bincount(r.ravel(), data.ravel())
    nr = np.bincount(r.ravel())
    radialprofile = tbin / nr
    return radialprofile


def batch_calc_radial_profile(image_list: List[Any]) -> List[Any]:
    """
    Batch calculate radial profile of all images previously created
    or by list of images
    """
    return batch_process(
        batch_fn=calc_radial_profile,
        data=image_list,
    )

def _gaussian(x, amp1,cen1,sigma1):
    return amp1*(1/(sigma1*(np.sqrt(2*np.pi))))*(np.exp((-1.0/2.0)*(((x-cen1)/sigma1)**2)))

def calc_curve_fit(data) -> Any:
    length_x = np.shape(data)
    xdata = np.linspace(0, 1000, num=length_x[0], retstep=False)
    ydata = data

    popt_linear, pcov_linear = curve_fit(_gaussian, xdata, ydata, p0=[1, -0.5, 1], maxfev=1000)


def batch_calc_curve_fitting(data: List[Any]) -> List[Any]:
    """
    Batch calculate fitting curve for every data item
    """
    return batch_process(
        batch_fn=calc_curve_fit,
        data=data,
    )
