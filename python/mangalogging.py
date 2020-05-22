import logging
import mangaconfig


#
#Error Message:
#
ERROR_MSG = ""

def config():
    # logging.basicConfig(level=logging.DEBUG)
    #logging.basicConfig(level=logging.DEBUG, filename=mangaconfig.LOGPATH + "logs.log")
    #logging.basicConfig(level=logging.DEBUG, format = '%(asctime)s:%(levelname)s:%(message)s', datefmt='%Y-%m-%d %H:%M:%S',)
    logging.basicConfig(level=logging.DEBUG, filename=mangaconfig.LOGPATH + "logs.log", format = '%(asctime)s:%(levelname)s:%(message)s', datefmt='%Y-%m-%d %H:%M:%S',)
    #logging.basicConfig(level=logging.DEBUG,level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')
    #logging.basicConfig(level=logging.DEBUG, filename="test.log", format='%(asctime)s:%(levelname)s:%(message)s')
    #logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:%(module)s:%(funcName)s:%(levelname)s:%(lineno)s:%(message)s)' )
    #logging.basicConfig(level=logging.DEBUG, filename="test.log",filemode='a', format='%(asctime)s:%(module)s:%(funcName)s:%(levelname)s:%(lineno)s:%(message)s)' )
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