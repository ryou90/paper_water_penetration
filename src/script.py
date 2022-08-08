from logger import get_logger
from main import PaperWaterPenetration

log = get_logger("Script")


def script():
    pwp = PaperWaterPenetration()
    pwp.run()


if __name__ == "__main__":
    script()
