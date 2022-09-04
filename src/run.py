from logger import get_logger, logging
from pwp import PaperWaterPenetration

log = get_logger("Script")
log.setLevel(logging.INFO)

def start():
    log.info("Start Paper Water Pentration Script")
    pwp = PaperWaterPenetration()
    pwp.run()
    log.info("Finish")


if __name__ == "__main__":
    start()
