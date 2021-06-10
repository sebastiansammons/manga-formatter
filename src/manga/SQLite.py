import os
import shutil
import logging
import sqlite3
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

class SQLite:
    def __init__(self, path):
        if(os.path.isfile(path) == False):
            self.connection = None
            self.cursor = None
            logger.error("[" + path + "] IS NOT A .db FILE")
        else:
            self.connection = sqlite3.connect(path)
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute("pragma integrity_check;")
        except AttributeError:
            self.connection = None
            self.cursor = None
            logger.error("NO VALID SQLite CONNECTION")
        except sqlite3.DatabaseError:
            self.connection = None
            self.cursor = None
            logger.error("NO VALID SQLite CONNECTION")

    def execute(self, query, query_input = None):
        if(self.connection is None or self.cursor is None):
            return False
        if(query_input == None):
            try:
                query_output = [query_data[0] for query_data in self.cursor.execute(query)]
            except sqlite3.OperationalError:
                logger.error("[" + query + "] IS NOT A VALID OPERATION")
                me.error_write("[" + query + "] IS NOT A VALID OPERATION")
                return False
            except sqlite3.ProgrammingError:
                logger.error("CAN'T RUN QUERY. CONNECTION IS CLOSED")
                me.error_write("CAN'T RUN QUERY. CONNECTION IS CLOSED")
                return False
        else:
            try:
                query_output = [query_data[0] for query_data in self.cursor.execute(query, query_input)]
            except sqlite3.OperationalError:
                logger.error("[" + query + " with data: " + str(query_input) + "] IS NOT A VALID OPERATION")
                me.error_write("[" + query + " with data: " + str(query_input) + "] IS NOT A VALID OPERATION")
                return False
            except sqlite3.IntegrityError:
                logger.error("[" + query_input + "] CANNOT BE USED TO INSERT/UPDATE")
                me.error_write("[" + query_input + "] CANNOT BE USED TO INSERT/UPDATE")
                return False
            except sqlite3.ProgrammingError:
                logger.error("CAN'T RUN QUERY. CONNECTION IS CLOSED")
                me.error_write("CAN'T RUN QUERY. CONNECTION IS CLOSED")
                return False    
        return query_output
                
    def commit(self):
        if(self.connection is None or self.cursor is None):
            return False
        try:
            self.connection.commit()
        except AttributeError:
            logger.error("NO VALID SQLite CONNECTION GIVEN")
            me.error_write("NO VALID SQLite CONNECTION GIVEN")
            return False

    def close(self):
        if(self.connection is None or self.cursor is None):
            return False
        try:
            self.connection.close()
        except AttributeError:
            logger.error("NO VALID SQLite CONNECTION GIVEN")
            me.error_write("NO VALID SQLite CONNECTION GIVEN")
            return False
