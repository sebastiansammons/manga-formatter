# Directory.py
import os
import shutil
# import manga_error as me
from . import manga_error as me

class Directory:
    def __init__(self, path):
        self.path = path

    def isdir(self):
        return os.path.isdir(self.path)

    def list_dir(self):
        if(self.isdir()):
            return sorted([f for f in os.listdir(self.path) if not f.startswith('.')])
        else:
            me.error_write("[" + self.path + "] IS NOT A DIRECTORY.")
            return False

    def num_files(self):
        if self.list_dir() is False:
            return -1
        return len(self.list_dir())

    def rm_dir(self):
        if(self.num_files() == 0):
            shutil.rmtree(self.path)
            return True
        else:
            me.error_write("[" + self.path + "] COULD NOT BE REMOVED.")
            return False

    def mk_dir(self):
        if(not(self.isdir())):
            try:
                os.mkdir(self.path)
                try:
                    shutil.chown(self.path, user = int(os.getenv("PUID")), group = int(os.getenv("PGID")))
                except PermissionError:
                    pass
                return True
            except FileExistsError:
                me.error_write("[" + self.path + "] ALREADY EXISTS")
                return False
        elif(self.num_files() > 0):
            me.error_write("[" + self.path + "] ALREADY EXISTS")
            return False
        else:
            return True
