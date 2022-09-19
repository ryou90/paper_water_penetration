from typing import Optional

from paper_water_penetration.logger import get_logger, logging
from paper_water_penetration.options import Options
from paper_water_penetration.pwp import PaperWaterPenetration

log = get_logger("Script")
log.setLevel(logging.INFO)


def start(opts: Options = Options(), wait: Optional[bool] = None):
    log.info("+++ Start Paper Water Pentration +++")
    if wait != None:
        opts.wait_for_key = wait
    pwp = PaperWaterPenetration(options=opts)
    pwp.run()
    log.info("+++ Finish process +++")


def wait_start():
    start(wait=True)


def capture(opts: Options = Options(), wait: Optional[bool] = None):
    log.info("+++ Start Paper Water Pentration Capturing +++")
    if wait != None:
        opts.wait_for_key = wait

    pwp = PaperWaterPenetration(options=opts)
    pwp.capture()
    log.info("+++ Finish capturing +++")


def wait_capture():
    capture(wait=True)


if __name__ == "__main__":
    start()
