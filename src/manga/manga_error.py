# manga_error.py
import os
import shutil
# import manga_config as mc
from . import manga_config as mc

def error_read():
    try:
        with open(mc.ERROR_PATH + ".error_message.txt",'r', encoding = "utf8") as fp:
            message = fp.readline()
            fp.close
            return message
    except FileNotFoundError:
        return ""

def error_write(message):
    try:
        with open(mc.ERROR_PATH + ".error_message.txt", 'w', encoding = "utf8") as fp:
            fp.write(message)
            fp.close
            try:
                shutil.chown(mc.ERROR_PATH + ".error_message.txt", user = int(os.getenv("PUID")), group = int(os.getenv("PGID")))
            except PermissionError:
                pass
    except FileNotFoundError:
        with open(".error_message.txt", 'w', encoding = "utf8") as fp:
            fp.write(message)
            fp.close
            try:
                shutil.chown(".error_message.txt", user = int(os.getenv("PUID")), group = int(os.getenv("PGID")))
            except PermissionError:
                pass
