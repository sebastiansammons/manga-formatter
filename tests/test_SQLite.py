#test_SQLite.py
import unittest
import os
import shutil
import sqlite3
from ..src.manga import SQLite
from ..src.manga import manga_config


class TestSQLite(unittest.TestCase):

    def setUp(self):
        shutil.copyfile("./manga-formatter/tests/data/db/test_manga.db", "./manga-formatter/tests/data/test_SQLite/test_manga.db")
        self.manga_db = SQLite("./manga-formatter/tests/data/test_SQLite/test_manga.db")

    def tearDown(self):
        self.manga_db.close()
        os.remove("./manga-formatter/tests/data/test_SQLite/test_manga.db")

    def test_sqlite(self):
        not_a_db = SQLite("./manga-formatter/tests/data/test_SQLite/notadb.txt")
        dir_db = SQLite("./manga-formatter/tests/data/test_SQLite/")
        fake_db = SQLite("./manga-formatter/tests/data/test_SQLite/fakedb.db")
        empty_db = SQLite("./manga-formatter/tests/data/test_SQLite/empty.db")
        double_db = SQLite("./manga-formatter/tests/data/test_SQLite/test_manga.db")
        self.assertEqual(not_a_db.connection, None)
        self.assertEqual(not_a_db.cursor, None)
        self.assertEqual(dir_db.connection, None)
        self.assertEqual(dir_db.cursor, None)
        self.assertEqual(fake_db.connection, None)
        self.assertEqual(fake_db.cursor, None)
        self.assertIsInstance(empty_db.connection, sqlite3.Connection)  
        self.assertIsInstance(empty_db.cursor, sqlite3.Cursor)
        self.assertIsInstance(double_db.connection, sqlite3.Connection)  
        self.assertIsInstance(double_db.cursor, sqlite3.Cursor)
        empty_db.close()
        double_db.close()

    def test_execute_no_input(self):
        #no query_input
        result = self.manga_db.execute("SELECT current_chapter FROM manga_progress WHERE manga='Attack on Titan';") #Single value back
        self.assertEqual(result, [139])

        result = self.manga_db.execute("SELECT current_chapter FROM manga_progress ORDER BY current_chapter ASC;") #multiple values back
        self.assertEqual(result, [6, 54, 58, 139, 188, 313, 1013])
        result = self.manga_db.execute("SELECT manga FROM manga_progress WHERE manga = 'Shingeki no Kyojin';") #no values back
        self.assertEqual(result, []) 
        result = self.manga_db.execute("Select * from fake_table") #invalid execute
        self.assertEqual(result, False)
        #add query isn't string test?

        #bad db
        not_a_db = SQLite("./manga-formatter/tests/data/test_SQLite/notadb.txt")
        result = not_a_db.execute("SELECT * FROM FAKETABLE")
        self.assertEqual(result, False)

        dir_db = SQLite("./manga-formatter/tests/data/test_SQLite/")
        result = dir_db.execute("SELECT * FROM FAKETABLE")
        self.assertEqual(result, False)

        #more to add (maybe make seperate unittests?)

    def test_execute_with_input(self):
        #with query_input
        query_input = ("Attack on Titan", ) #(probably put in exeucte instead)
        result = self.manga_db.execute("SELECT current_chapter FROM manga_progress WHERE manga = ?", query_input) #Single value back
        self.assertEqual(result, [139])

        query_input = (60, )
        result = self.manga_db.execute("SELECT manga FROM manga_progress WHERE current_chapter < ?;", query_input) #multiple values back
        self.assertEqual(result, ["Boruto", "Platinum End", "Blue Box"])

        query_input = ("Shingeki no Kyojin", )
        result = self.manga_db.execute("SELECT manga FROM manga_progress WHERE manga = ?;", query_input) #no values back
        self.assertEqual(result, []) 

        result = self.manga_db.execute("invalid execute", query_input) #invalid execute/input
        self.assertEqual(result, False)

        query_input = (7, ) #value to insert
        result = self.manga_db.execute("SELECT current_chapter FROM manga_progress WHERE manga = 'Blue Box';")
        #check before
        self.assertEqual(result, [6])
        result = self.manga_db.execute("UPDATE manga_progress SET current_chapter = ? WHERE manga = 'Blue Box'", query_input) #insert row
        result = self.manga_db.execute("SELECT current_chapter FROM manga_progress WHERE manga = 'Blue Box';")
        self.assertEqual(result, [7])

        query_input = (8, "Blue Box") #insert multiple values
        result = self.manga_db.execute("UPDATE manga_progress SET current_chapter = ? WHERE manga = ?", query_input)
        result = self.manga_db.execute("SELECT current_chapter FROM manga_progress WHERE manga = 'Blue Box';")
        self.assertEqual(result, [8])

        #add query with invalid _input
        query_input = ("Shingeki no Kyojin", )
        result = self.manga_db.execute("SELECT manga FROM manga_progress WHERE manga = ?;", query_input)
        self.assertEqual(result, []) 

        query_input = "Invalit input"
        result = self.manga_db.execute("Select * from fake_table") #invalid execute
        self.assertEqual(result, False)

    def test_commit(self):
        #commit
        result = self.manga_db.execute("SELECT current_chapter FROM manga_progress WHERE manga = 'Blue Box';")
        self.assertEqual(result, [6])
        result = self.manga_db.execute("UPDATE manga_progress SET current_chapter = 7 WHERE manga = 'Blue Box';")
        result = self.manga_db.execute("SELECT current_chapter FROM manga_progress WHERE manga = 'Blue Box';")
        self.assertEqual(result, [7])
        self.manga_db.commit()
        self.manga_db.close()
        self.manga_db = SQLite("./manga-formatter/tests/data/test_SQLite/test_manga.db")
        result = self.manga_db.execute("SELECT current_chapter FROM manga_progress WHERE manga = 'Blue Box';")
        self.assertEqual(result, [7])


        #don't commit
        result = self.manga_db.execute("UPDATE manga_progress SET current_chapter = 8 WHERE manga = 'Blue Box';")
        result = self.manga_db.execute("SELECT current_chapter FROM manga_progress WHERE manga = 'Blue Box';")
        self.assertEqual(result, [8])
        self.manga_db.close()
        self.manga_db = SQLite("./manga-formatter/tests/data/test_SQLite/test_manga.db")
        result = self.manga_db.execute("SELECT current_chapter FROM manga_progress WHERE manga = 'Blue Box';")
        self.assertNotEqual(result, [8])

        #commit bad .db
        not_a_db = SQLite("./manga-formatter/tests/data/test_SQLite/notadb.txt")
        result = not_a_db.commit()
        self.assertEqual(result, False)
        dir_db = SQLite("./manga-formatter/tests/data/test_SQLite/")
        result = dir_db.commit()
        self.assertEqual(result, False)

    def test_close(self):
        result = self.manga_db.execute("SELECT current_chapter FROM manga_progress WHERE manga='Attack on Titan';") #get any data
        self.assertEqual(result, [139])
        self.manga_db.close()
        result = self.manga_db.execute("SELECT current_chapter FROM manga_progress WHERE manga='Attack on Titan';") #try again after close
        self.assertEqual(result, False)
        self.manga_db = SQLite("path/to/place/sqlite")

        self.manga_db.close()
        result = self.manga_db.close()
        self.assertEqual(result, False)

        #close bad db
        not_a_db = SQLite("./manga-formatter/tests/data/test_SQLite/notadb.txt")
        result = not_a_db.close()
        self.assertEqual(result, False)
        dir_db = SQLite("./manga-formatter/tests/data/test_SQLite/")
        result = dir_db.close()
        self.assertEqual(result, False)



if __name__=='__main__':
    unittest.main()