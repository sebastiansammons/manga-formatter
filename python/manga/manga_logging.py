import logging
from datetime import datetime
import manga_config


#
#Gloabal Error Message:
#
ERROR_MSG = ""

def log_config():
    try:
        

        logging.basicConfig(level = logging.DEBUG, filename = manga_config.LOGS_PATH + datetime.now().strftime("logs_%Y-%m-%d.log"), format = '%(asctime)s|%(levelname)-7s|%(message)s', datefmt='%Y/%m/%d %H:%M', )
        logging.getLogger
    except FileNotFoundError:
        logging.basicConfig(level = logging.DEBUG, filename = datetime.now().strftime("logs_%Y-%m-%d.log"), format = '%(asctime)s|%(levelname)-7s|%(message)s', datefmt='%Y/%m/%d %H:%M', )
        logging.getLogger

def log_debug(message):
    return logging.debug(message)

def log_info(message):
    return logging.info(message)

def log_warning(message):
    return logging.warning(message)

def log_error(message):
    return logging.error(message)

def log_critical(message):
    return logging.critical(message)