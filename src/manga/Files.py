import os
import shutil
import logging
from . import manga_config as mc
from . import manga_error as me
from . import Directory

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

class Files(Directory):
    def __init__(self, path):
        super().__init__(path)
        self.filenames = self.list_dir()
        self.count = self.num_files()

    def isfile(self, file = 0):
        return os.path.isfile(self.path + self.filenames[file])

    def ext(self, file = 0):
        if(self.filenames[file].rfind('.') != -1):
            return self.filenames[file][self.filenames[file].rfind('.'):]
        return -1

    def rename(self, dest_path, dest_filename, file = 0):
        if(self.num_files() == 0):
            return False
        src = self.path + "/" + self.filenames[file]
        dest = dest_path + "/" + dest_filename
        if(os.path.isfile(dest) == True):
            logger.warning("[" + dest + "] ALREADY EXISTS")
            me.error_write("[" + dest + "] ALREADY EXISTS")
            return False
        try:
            shutil.move(src,dest)
            shutil.chown(dest, user = int(os.getenv("PUID")), group = int(os.getenv("PGID")))
            logger.debug("Rename: " + src + " > " + dest)
        except FileNotFoundError:
            if(os.path.isfile(src) == False):
                logger.error("[" + src + "] NOT FOUND")
                me.error_write("[" + src + "] NOT FOUND")
                return False
        except PermissionError:
            logger.error("[" + src + ", " + dest + "] PERMISSION ERROR")
            me.error_write("[" + src + ", " + dest + "] PERMISSION ERROR")
            return False
        return True

    def copyfile(self, dest_path, dest_filename):
        #Meant to only copy 1 file so the File object shouldn't have more than 1 file
        if not(isinstance(dest_filename, str)):
            logger.error("INVALID DEST FILENAME")
            me.error_write("INVALID DEST FILENAME")
            return False
        if not(os.path.isdir(dest_path)):
            logger.warning("[" + dest_path + "] NOT FOUND")
            me.error_write("[" + dest_path + "] NOT FOUND")
            return False
        if(os.path.isfile(dest_path + "/" + dest_filename)):
            logger.warning("[" + dest_path + "/" + str(self.filenames) + "] ALREADY EXISTS")
            me.error_write("[" + dest_path + "/" + str(self.filenames) + "] ALREADY EXISTS")
            return False
        else:
            shutil.copyfile(self.path + "/" + self.filenames[0], dest_path + "/" + dest_filename)
            shutil.chown(dest_path + "/" + dest_filename, user = int(os.getenv("PUID")), group = int(os.getenv("PGID")))
            logger.debug("Copy: " + self.path + "/" + self.filenames[0] + " > " + dest_path + "/" + dest_filename)
            return True

    def pad_zero(self, preview = None):
        for file in range(0,self.num_files()):
            for char in range(0, len(self.filenames[file])):
                if(self.filenames[file][char].isnumeric()):
                    if(char == 0):
                        #First character
                        if(self.filenames[file][char+1].isnumeric()):
                            continue
                        else:
                            #Single numeric character at the beginning, add leading zero
                            dest_filenames = self.filenames[file][:char] + "0" + self.filenames[file][char:]
                            if preview == "Preview":
                                self.filenames[file] = dest_filenames
                            else:
                                self.rename(self.path, dest_filenames, file)
                                logger.debug("Pad Zero: " + self.filenames[file] + " > " + dest_filenames)
                            break
                    elif(char + 1 >= len(self.filenames[file])):
                        #Last character
                        dest_filenames = self.filenames[file][:char] + "0" + self.filenames[file][char:]
                        if preview == "Preview":
                            self.filenames[file] = dest_filenames
                        else:
                            self.rename(self.path, dest_filenames, file)
                            logger.debug("Pad Zero: " + self.filenames[file] + " > " + dest_filenames)
                        break
                    else:
                        #Middle character
                        if(self.filenames[file][char] != '0'):
                            if(self.filenames[file][char + 1].isnumeric()):
                                continue
                            elif(self.filenames[file][char - 1].isnumeric()):
                                continue
                            else:
                                dest_filenames = self.filenames[file][:char] + "0" + self.filenames[file][char:]
                                if preview == "Preview":
                                    self.filenames[file] = dest_filenames
                                else:
                                    self.rename(self.path, dest_filenames, file)
                                    logger.debug("Pad Zero: " + self.filenames[file] + " > " + dest_filenames)
                                break
                        else:
                            if(self.filenames[file][char + 1].isnumeric() and self.filenames[file][char +1] != '0'):
                                break
        #Update list
        if(preview == "Preview"):
            self.filenames = sorted(self.filenames)
        else:
            self.filenames = self.list_dir()
        return
