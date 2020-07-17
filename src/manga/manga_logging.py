#manga_logging.py
import os
import shutil
import logging
from datetime import datetime
from . import manga_config


def log_config():
    try:
        logs_filename = manga_config.LOGS_PATH + datetime.now().strftime("logs_%Y-%m-%d.log")
        logging.basicConfig(level = logging.DEBUG, filename = logs_filename, format = '%(asctime)s|%(levelname)-7s|%(message)s', datefmt='%Y/%m/%d %H:%M', )
        shutil.chown(logs_filename, user = int(os.getenv("PUID")), group = int(os.getenv("PGID")))
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

def message_read():
    try:
        with open(manga_config.LOGS_PATH + ".message.txt",'r', encoding = "utf8") as fp:
            message = fp.readline()
            fp.close
            return message
    except FileNotFoundError:
        return ""

def message_write(message):
    try:
        with open(manga_config.LOGS_PATH + ".message.txt", 'w', encoding = "utf8") as fp:
            fp.write(message)
            fp.close
            shutil.chown(manga_config.LOGS_PATH + ".message.txt", user = int(os.getenv("PUID")), group = int(os.getenv("PGID")))
    except FileNotFoundError:
        with open(".message.txt", 'w', encoding = "utf8") as fp:
            fp.write(message)
            fp.close
            shutil.chown(".message.txt", user = int(os.getenv("PUID")), group = int(os.getenv("PGID")))
