# Logging
from logger import get_logger, logging

# Image batch processing functions
from image import Images, image_read, image_write, image_to_gray

# Interval capturing and grey scaling
from capture import Capture

# Transformer functions
import transformer as tf

# set log level to debug
log = get_logger("capture")
#log.setLevel(logging.DEBUG)

c = Capture([(100, 10),(1000, 100)], path="../data/")
c.run_capture()