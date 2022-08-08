import matplotlib.pyplot as plt
import image
from typing import Any, Callable, List

def write_plot(data, pathname) -> None:
    plt.plot(data)
    plt.savefig(pathname)
    plt.close()


def batch_write_plots(
    batch_fn : Callable,
    path: str,
    data: List[Any],
    filename: str = "DVM22_Penetration",
    suffix="_plot",
    file_ending: str = ".png",
) -> None:
    """Batch write plot to disk"""

    count = 0
    image.create_path(path)

    for item in data:
        count += 1
        pathname: str = f"{path}{filename}_{count}{suffix}{file_ending}"
        batch_fn(item, pathname)
    return


def write_curve_fit(data, pathname) -> None:
    plt.plot(data)
    plt.savefig(pathname)
    plt.close()
