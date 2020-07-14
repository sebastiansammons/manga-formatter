import logging
import manga_config


#
#Gloabal Error Message:
#
ERROR_MSG = ""

def config():
    try:
        # logging.basicConfig(level=logging.DEBUG)
        #logging.basicConfig(level=logging.DEBUG, filename=manga_config.LOG_PATH + "logs.log")
        #logging.basicConfig(level=logging.DEBUG, format = '%(asctime)s:%(levelname)s:%(message)s', datefmt='%Y-%m-%d %H:%M:%S', )
        logging.basicConfig(level=logging.DEBUG, filename=manga_config.LOG_PATH + "testing_logs.log", format = '%(asctime)s|%(levelname)-7s|%(message)s', datefmt='%Y/%m/%d %H:%M', )
        # logging.basicConfig(level=logging.DEBUG, filename=manga_config.LOG_PATH + "testing_logs.log", format = '%(asctime)s|%(levelname)-7s| %(message)s', datefmt='%Y/%m/%d %H:%M', )
        #logging.basicConfig(level=logging.DEBUG, level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')
        #logging.basicConfig(level=logging.DEBUG, filename="test.log", format='%(asctime)s:%(levelname)s:%(message)s')
        #logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:%(module)s:%(funcName)s:%(levelname)s:%(lineno)s:%(message)s)' )
        #logging.basicConfig(level=logging.DEBUG, filename="test.log", filemode='a', format='%(asctime)s:%(module)s:%(funcName)s:%(levelname)s:%(lineno)s:%(message)s)' )
        logging.getLogger
    except FileNotFoundError:
        logging.basicConfig(level=logging.DEBUG)
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