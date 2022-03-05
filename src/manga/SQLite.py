# SQLite.py
import os
import sqlite3
# import manga_error as me
from . import manga_error as me

class SQLite:
    def __init__(self, path):
        if(os.path.isfile(path) == False):
            self.connection = None
            self.cursor = None
        else:
            self.connection = sqlite3.connect(path)
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute("pragma integrity_check;")
        except AttributeError:
            self.connection = None
            self.cursor = None
        except sqlite3.DatabaseError:
            self.connection = None
            self.cursor = None

    def execute(self, query, query_input = None):
        if(self.connection is None or self.cursor is None):
            return False
        if(query_input == None):
            try:
                query_output = [query_data[0] for query_data in self.cursor.execute(query)]
            except sqlite3.OperationalError:
                me.error_write("[" + query + "] IS NOT A VALID OPERATION")
                return False
            except sqlite3.ProgrammingError:
                me.error_write("CAN'T RUN QUERY. CONNECTION IS CLOSED")
                return False
        else:
            try:
                query_output = [query_data[0] for query_data in self.cursor.execute(query, query_input)]
            except sqlite3.OperationalError:
                me.error_write("[" + query + " with data: " + str(query_input) + "] IS NOT A VALID OPERATION")
                return False
            except sqlite3.IntegrityError:
                me.error_write("[" + query_input + "] CANNOT BE USED TO INSERT/UPDATE")
                return False
            except sqlite3.ProgrammingError:
                me.error_write("CAN'T RUN QUERY. CONNECTION IS CLOSED")
                return False    
        return query_output
                
    def commit(self):
        if(self.connection is None or self.cursor is None):
            return False
        try:
            self.connection.commit()
        except AttributeError:
            me.error_write("NO VALID SQLite CONNECTION GIVEN")
            return False

    def close(self):
        if(self.connection is None or self.cursor is None):
            return False
        try:
            self.connection.close()
        except AttributeError:
            me.error_write("NO VALID SQLite CONNECTION GIVEN")
            return False
