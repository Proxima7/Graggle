import logging
import os

logger = logging.getLogger('graggle_logger')
def configure_logging():
    # configure logger
    my_loglevel = os.getenv("LOG_LEVEL")
    if my_loglevel == None:
        my_loglevel = "INFO"
    logger.setLevel(logging.getLevelName(my_loglevel))

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.getLevelName(my_loglevel))
    ch.setFormatter(formatter)      # add formatter to ch
    logger.addHandler(ch)           # add ch to logger

    logger.warning(f'logging initialized with: {my_loglevel}')
