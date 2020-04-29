import logging



def config():
    logging.basicConfig(level=logging.DEBUG)
    #logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')
    #logging.basicConfig(level=logging.DEBUG, filename="test.log", format='%(asctime)s:%(levelname)s:%(message)s')
    #logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:%(module)s:%(funcName)s:%(levelname)s:%(lineno)s:%(message)s)' )
    #logging.basicConfig(level=logging.DEBUG, filename="test.log",filemode='a', format='%(asctime)s:%(module)s:%(funcName)s:%(levelname)s:%(lineno)s:%(message)s)' )



def log_debug(message):
    logging.debug(message)

def log_info(message):
    logging.info(message)

def log_warning(message):
    logging.warning(message)

def log_error(message):
    logging.error(message)

def log_critical(message):
    logging.critical(message)