# test_auto_format.py
import shutil
import unittest
# Before
# import src.manga.SQLite as SQLite
# import src.manga.Files as Files
# import src.manga.manga_config as manga_config
# import src.manga.manga_format as manga_format
import sys
sys.path.append("..")
# from src.manga.SQLite import SQLite
# from src.manga.Files import Files
# from src.manga.manga_config import manga_config
# from src.manga.manga_format import manga_format
from src.manga import SQLite
from src.manga import Files
from src.manga import manga_config
from src.manga import manga_format



class TestAutoFormat(unittest.TestCase):

    def setUp(self):
        manga_config.DB_FILE_PATH = "./tests/data/test_format/db/test_manga.db"
        manga_config.SOURCE_PATH = "./tests/data/test_format/src/"
        manga_config.MANGA_PATH = "./tests/data/test_format/manga/"
        shutil.copytree("./tests/data/db/", "./tests/data/test_format/db/")
        shutil.copytree("./tests/data/manga/", "./tests/data/test_format/manga/")

    def tearDown(self):
        try:
            shutil.rmtree("./tests/data/test_format/db/")
            shutil.rmtree("./tests/data/test_format/manga/")
        except:
            pass

    def test_auto_chapter(self):
        shutil.copytree("./tests/data/test_format/auto_chapter/Not One Piece/src/", manga_config.SOURCE_PATH)
        manga_db = SQLite(manga_config.DB_FILE_PATH)
        result = manga_db.execute("SELECT current_chapter FROM manga_progress WHERE manga='Attack on Titan';")
        self.assertEqual(result[0], 139)
        manga_db.close()
        manga_format.auto_chapter_format("Attack on Titan", "Last Chapter")
        manga_db = SQLite(manga_config.DB_FILE_PATH)
        result = manga_db.execute("SELECT current_chapter FROM manga_progress WHERE manga='Attack on Titan';")
        self.assertEqual(result[0], 140)
        result = manga_db.execute("SELECT title FROM Attack_on_Titan_chapter WHERE ch = 140;")
        self.assertEqual(result[0], "Last Chapter")
        manga_db.close()
        nOP_chapter = Files("./tests/data/test_format/manga/Attack on Titan/Chapter Pages/Newly Released/140/")
        self.assertEqual(nOP_chapter.filenames[0], "Attack on Titan - CH140PG01 - Last Chapter.jpg")
        self.assertEqual(nOP_chapter.filenames[17], "Attack on Titan - CH140PG18 - Last Chapter.jpg")
        self.assertEqual(nOP_chapter.count, 18)
        shutil.rmtree(manga_config.SOURCE_PATH)

        shutil.copytree("./tests/data/test_format/auto_chapter/One Piece/src/", manga_config.SOURCE_PATH)
        manga_db = SQLite(manga_config.DB_FILE_PATH)
        result = manga_db.execute("SELECT current_chapter FROM manga_progress WHERE manga='One Piece';")
        self.assertEqual(result[0], 1013)
        manga_db.close()
        manga_format.auto_chapter_format("One Piece", "Cool Title Only")
        manga_db = SQLite(manga_config.DB_FILE_PATH)
        result = manga_db.execute("SELECT current_chapter FROM manga_progress WHERE manga='One Piece';")
        self.assertEqual(result[0], 1014)
        result = manga_db.execute("SELECT title FROM One_Piece_chapter WHERE ch = 1014;")
        self.assertEqual(result[0], "Cool Title Only")
        manga_db.close()
        OP_chapter = Files("./tests/data/test_format/manga/One Piece/Chapter Pages/Newly Released/1014/")
        self.assertEqual(OP_chapter.filenames[0], "One Piece - CH1014PG01 - Cool Title Only.jpeg")
        self.assertEqual(OP_chapter.filenames[13], "One Piece - CH1014PG14 - Cool Title Only.jpeg")
        self.assertEqual(OP_chapter.count, 14)
        OP_cover = Files("./tests/data/test_format/manga/One Piece/Cover Pages/1001-End/")
        self.assertEqual(OP_cover.filenames[13], "CH1014 Cover.jpeg")
        shutil.rmtree(manga_config.SOURCE_PATH)

    def test_auto_volume(self):
        shutil.copytree("./tests/data/test_format/auto_volume/Not One Piece/src/", manga_config.SOURCE_PATH)
        manga_db = SQLite(manga_config.DB_FILE_PATH)
        result = manga_db.execute("SELECT current_volume FROM manga_progress WHERE manga='Attack on Titan';")
        self.assertEqual(result[0], 33)
        manga_db.close()
        manga_format.auto_volume_format("Attack on Titan", 139, "Last Volume")
        manga_db = SQLite(manga_config.DB_FILE_PATH)
        result = manga_db.execute("SELECT current_volume FROM manga_progress WHERE manga='Attack on Titan';")
        self.assertEqual(result[0], 34)
        result = manga_db.execute("SELECT title FROM Attack_on_Titan_volume WHERE volume = 34;")
        self.assertEqual(result[0], "Last Volume")
        manga_db.close()
        nOP_volume = Files("./tests/data/test_format/manga/Attack on Titan/Chapter Pages/Volumes/Attack on Titan Volume 34 - Last Volume/")
        self.assertEqual(nOP_volume.filenames[0], "Attack on Titan - 34 - Last Volume.jpg")
        self.assertEqual(nOP_volume.filenames[233], "Attack on Titan - CH139PG55 - Toward the Tree on That Hill.png")
        self.assertEqual(nOP_volume.count, 234)
        shutil.rmtree(manga_config.SOURCE_PATH)

        shutil.copytree("./tests/data/test_format/auto_volume/One Piece/src/", manga_config.SOURCE_PATH)
        manga_db = SQLite(manga_config.DB_FILE_PATH)
        result = manga_db.execute("SELECT current_volume FROM manga_progress WHERE manga='One Piece';")
        self.assertEqual(result[0], 98)
        manga_db.close()
        manga_format.auto_volume_format("One Piece", 1004, "Straw Hat Luffy")
        manga_db = SQLite(manga_config.DB_FILE_PATH)
        result = manga_db.execute("SELECT current_volume FROM manga_progress WHERE manga='One Piece';")
        self.assertEqual(result[0], 99)
        result = manga_db.execute("SELECT title FROM One_Piece_volume WHERE volume = 99;")
        self.assertEqual(result[0], "Straw Hat Luffy")
        manga_db.close()
        OP_volume = Files("./tests/data/test_format/manga/One Piece/Chapter Pages/Volumes/One Piece Volume 099 - Straw Hat Luffy/")
        self.assertEqual(OP_volume.filenames[0], "One Piece - 099 - Straw Hat Luffy.jpeg")
        self.assertEqual(OP_volume.filenames[146], "One Piece - CH1004PG17 - Kibi Dango.png")
        self.assertEqual(OP_volume.count, 147)
        shutil.rmtree(manga_config.SOURCE_PATH)


if __name__ == '__main__':
    unittest.main()
