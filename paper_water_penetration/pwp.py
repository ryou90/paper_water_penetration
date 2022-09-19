from typing import Any, Callable, List, Optional

from paper_water_penetration import calc, image, plot
from paper_water_penetration.cache import Cache
from paper_water_penetration.capture import capture
from paper_water_penetration.logger import get_logger, logging
from paper_water_penetration.options import Options

log = get_logger("PaperWaterPenetration")
log.setLevel(logging.INFO)

class PaperWaterPenetration:

    _options: Options
    _cache: Cache

    def __init__(self, options: Options = Options(), cache: Cache = Cache()) -> None:
        """Initial with options and cache class"""
        self._options = options
        self._cache = cache

    @property
    def options(self) -> Options:
        """Get options class as property"""
        return self._options

    @property
    def cache(self) -> Cache:
        """Get cache class as property"""
        return self._cache

    @property
    def default_pipeline(self) -> List[Callable]:
        """Default order of process executing"""
        return [
            self.capture,
            self.convertToGray,
            self.fft2_transform,
            self.radial_transform,
        ]

    def clear_cache(self, name: str) -> None:
        """Remove entries from cache"""
        del self._cache[name]

    def batch_write_images(self, images: List[Any], suffix: str = "") -> None:
        image.batch_write_images(
            path=self.options.data_path,
            images=images,
            filename=self.options.filename,
            suffix=suffix,
            file_ending=self.options.file_ending,
        )

    def batch_write_plots(
        self,
        data: List[Any],
        suffix: str = "",
        batch_fn: Callable = plot.write_plot,
    ) -> None:
        plot.batch_write_plots(
            batch_fn=batch_fn,
            path=self.options.data_path,
            data=data,
            filename=self.options.filename,
            suffix=suffix,
            file_ending=self.options.file_ending,
        )

    def run(
        self, custom_pipeline: Optional[List[Callable]] = None, *args, **kwargs
    ) -> bool:
        """Execute process pipeline"""
        pip = custom_pipeline if custom_pipeline else self.default_pipeline

        result: Any = None

        current : int  = 1
        total : int = len(pip)
        log.info(f"# Total process steps: {total}")
        for fn in pip:
            try:
                log.info(f"# Start pipeline process {current}/{total}: {fn.__name__.upper()}")
                result = fn(result, *args, **kwargs)
                log.info(f"# Finish pipeline process: {fn.__name__.upper()}")
            except Exception as err:
                print(f"Error in executing pipeline: {err}")
            current += 1

        return True

    def capture(self, *args, **kwargs) -> List[Any]:
        """Start capturing and return list if captured images."""
        self.cache["pre_capture"] = capture(
            self.options.intervals, self.options.resolution, self.options.wait_for_key
        )
        self.cache["capture"] = image.batch_resize(
            self.cache["pre_capture"], new_size=self.options.resize
        )

        # Write images to disk if enabled
        if self.options.write_capture:
            log.info("Write images to store...")
            self.batch_write_images(self.cache["capture"])

        return self.cache["capture"]

    def convertToGray(
        self, images: Optional[List[Any]] = None, *args, **kwargs
    ) -> List[Any]:
        """Convert list of given images to gray scale."""
        if not images:
            images = self.cache["capture"]

        self.cache["convertToGray"] = image.batch_convert_to_gray(images)

        # Write images to disk if enabled
        if self.options.write_convertToGray:
            self.batch_write_images(self.cache["convertToGray"], "_gray")

        return self.cache["convertToGray"]

    def fft2_transform(
        self, images: Optional[List[Any]] = None, *args, **kwargs
    ) -> List[Any]:
        """Transform list of given images by fft2 transformer."""
        if not images:
            images = self.cache["convertToGray"]

        self.cache["fft2_transform"] = calc.batch_fft2_transform(images)

        # Write images to disk if enabled
        if self.options.write_fft2_transform:
            log.info("Write images to store...")
            self.batch_write_images(
                self.cache["fft2_transform"], suffix="_fft2_transform"
            )

            # We can't use cache here, due to a subsequent unknown processing error
            # in image : cv.applyColorMap(image, cv.COLORMAP_JET)
            # Solved this by first write to disk and reread afterwards
            if self.options.use_jet_colormap:
                pattern: str = f"{self.options.filename}_*_fft2_transform{self.options.file_ending}"
                tmp_images: List[Any] = image.batch_convert_to_jet(
                    path=self.options.data_path, pattern=pattern
                )

                image.batch_write_images(
                    path=self.options.data_path,
                    images=tmp_images,
                    filename=self.options.filename,
                    suffix="_fft2_transform_jet",
                    file_ending=self.options.file_ending,
                )

        return self.cache["fft2_transform"]

    def radial_transform(
        self, images: Optional[List[Any]] = None, *args, **kwargs
    ) -> List[Any]:
        """Transform list of given images by radial profile calculation."""
        if not images:
            images = self.cache["fft2_transform"]

        self.cache["radial_transform"] = calc.batch_calc_radial_profile(images)

        # Write images to disk if enabled
        if self.options.write_radial_transform:
            log.info("Write images to store...")
            self.batch_write_plots(
                self.cache["radial_transform"], "_radial_transform_plot"
            )

        return self.cache["radial_transform"]