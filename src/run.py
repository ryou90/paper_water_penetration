from logger import get_logger, logging
from pwp import PaperWaterPenetration

log = get_logger("Script")
log.setLevel(logging.INFO)

def start():
    log.info("Start Paper Water Pentration")
    pwp = PaperWaterPenetration()
    pwp.run()
    log.info("Finish")


def capture():
    log.info("Start Paper Water Pentration Capturing")
    pwp = PaperWaterPenetration()
    pwp.capture()
    log.info("Finish capturing")


if __name__ == "__main__":
    start()
