import logging
from logging import Logger
# create logger

def get_logger(name: str) -> Logger:
    """Get logger by name."""
    logger = logging.getLogger(name)

    if not logger.handlers:
        # create console handler and set level to debug
        # best for development or debugging
        handler = logging.StreamHandler()
        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        # add formatter to ch
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

###################
# USE LOGGER
###################

# example usage
#logger.debug('debug message')
#logger.info('info message')
#logger.warning('warn message')
#logger.error('error message')
#logger.critical('critical message')