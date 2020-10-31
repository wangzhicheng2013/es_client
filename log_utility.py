#!/usr/bin/python
import logging
from logging.handlers import RotatingFileHandler, SysLogHandler
def get_logger(log_file = "../log/es_client.log", verbose = True):
    logger = logging.getLogger(name = 'cmdLineLog')
    set_log_level(logger, verbose)
    try:
        handler = RotatingFileHandler(log_file, mode = 'a', maxBytes = 1024 * 1024 * 10, backupCount = 10)
    except:
        handler = SysLogHandler()
    handler.setFormatter(logging.Formatter("[%(asctime)s -%(levelname)5s -%(filename)20s:%(lineno)3s]    %(message)s"))
    logger.addHandler(handler)
    return logger
def set_log_level(logger, verbose):
    if (verbose):
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)