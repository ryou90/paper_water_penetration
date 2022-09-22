from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import List, Tuple

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR: str = str(Path(__file__).resolve().parent.parent)
TODAY = date.today().isoformat()


@dataclass
class Options:
    data_path: str = f"{BASE_DIR}/data/{TODAY}/"
    filename: str = "DVM22_Penetration"
    file_ending: str = ".png"
    wait_for_key: bool = False
    write_capture: bool = True
    write_convertToGray: bool = False
    write_fft2_transform: bool = True
    use_jet_colormap : bool = True
    write_radial_transform: bool = True
    intervals: List[Tuple[int, int]] = field(default_factory=lambda: [(3000, 300)])
    """
        Camera Options - must be higher than resize size
        width x height
        160.0 x 120.0
        176.0 x 144.0
        320.0 x 240.0
        352.0 x 288.0
        640.0 x 480.0
        1024.0 x 768.0
        1280.0 x 1024.0
    """
    resolution: Tuple[int, int] = field(default_factory=lambda: (640, 480))
    """
        Square resize and cropping.

    """
    resize: int = 300
