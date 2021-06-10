import os
import shutil
import logging
from . import manga_config as mc
from . import manga_error as me

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s|%(funcName)-30s|%(levelname)-7s|%(message)s')
file_handler = logging.FileHandler(mc.LOGS_PATH + "manga.log")
shutil.chown(mc.LOGS_PATH + "manga.log", user = int(os.getenv("PUID")), group = int(os.getenv("PGID")))
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.WARNING)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

class Directory:
    def __init__(self, path):
        self.path = path

    def isdir(self):
        return os.path.isdir(self.path)

    def list_dir(self):
        if(self.isdir()):
            return sorted([f for f in os.listdir(self.path) if not f.startswith('.')])
        else:
            logger.warning("[" + self.path + "] IS NOT A DIRECTORY.")
            me.error_write("[" + self.path + "] IS NOT A DIRECTORY.")
            return False

    def num_files(self):
        if self.list_dir() is False:
            return -1
        return len(self.list_dir())

    def rm_dir(self):
        if(self.num_files() == 0):
            shutil.rmtree(self.path)
            logger.debug("[" + self.path + "] REMOVED.")
            return True
        else:
            logger.warning("[" + self.path + "] COULD NOT BE REMOVED.")
            me.error_write("[" + self.path + "] COULD NOT BE REMOVED.")
            return False

    def mk_dir(self):
        if(not(self.isdir())):
            try:
                os.mkdir(self.path)
                shutil.chown(self.path, user = int(os.getenv("PUID")), group = int(os.getenv("PGID")))
                logger.debug("[" + self.path + "] CREATED")
                return True
            except FileExistsError:
                logger.error("[" + self.path + "] ALREADY EXISTS")
                me.error_write("[" + self.path + "] ALREADY EXISTS")
                return False
        elif(self.num_files() > 0):
            logger.error("[" + self.path + "] ALREADY EXISTS")
            me.error_write("[" + self.path + "] ALREADY EXISTS")
            return False
        else:
            return True
