# test_check.py
import shutil
import unittest
from ..src.manga import SQLite
from ..src.manga import manga_config
from ..src.manga import manga_check

class TestCheck(unittest.TestCase):

    def setUp(self):
        manga_config.LOGS_PATH = "./tests/data/logs/"
        manga_config.DB_FILE_PATH = "./tests/data/test_check/db/test_manga.db"
        manga_config.SOURCE_PATH = "./tests/data/test_check/src/"
        manga_config.DESTINATION_PATH = "./tests/data/test_check/dest/"
        manga_config.MANGA_PATH = "./tests/data/test_check/manga/"
        shutil.copytree("./tests/data/db/", "./tests/data/test_check/db/")
        shutil.copytree("./tests/data/manga/", "./tests/data/test_check/manga/")

    def tearDown(self):
        try:
            shutil.rmtree("./tests/data/test_check/db/")
            shutil.rmtree("./tests/data/test_check/manga/")
            shutil.rmtree(manga_config.SOURCE_PATH)
        except:
            pass
        try:
            shutil.rmtree(manga_config.DESTINATION_PATH)
        except:
            pass

    def test_auto_chapter_check(self):
        self.assertEqual(manga_check.check_auto_chapter("", "Title Only"), False)
        self.assertEqual(manga_check.check_auto_chapter("manga only", ""), False)
        shutil.copytree("./tests/data/test_check/auto_chapter/Empty src/src/", manga_config.SOURCE_PATH)
        self.assertEqual(manga_check.check_auto_chapter("One Piece", "Empty Volume"), False)
        shutil.rmtree(manga_config.SOURCE_PATH)

        shutil.copytree("./tests/data/test_check/auto_chapter/No ext/src/", manga_config.SOURCE_PATH)
        self.assertEqual(manga_check.check_auto_chapter("One Piece", "Missing .ext Volume"), False)
        shutil.rmtree(manga_config.SOURCE_PATH)

        shutil.copytree("./tests/data/test_check/auto_chapter/No file/src/", manga_config.SOURCE_PATH)
        self.assertEqual(manga_check.check_auto_chapter("One Piece", "Not all files Volume"), False)
        shutil.rmtree(manga_config.SOURCE_PATH)

        shutil.copytree("./tests/data/test_check/auto_chapter/Working src/src/", manga_config.SOURCE_PATH)
        self.assertEqual(manga_check.check_auto_chapter("One Piece", "Working Volume"), True)
        shutil.rmtree(manga_config.SOURCE_PATH)
        #DB Checks
        self.assertEqual(manga_check.check_auto_chapter("Test", "Not in Progress"), False)
        manga_db = SQLite(manga_config.DB_FILE_PATH)
        manga_db.execute("INSERT INTO manga_progress (manga, current_chapter, current_volume, first_chapter_of_new_volume) VALUES(""Test"", 0, 0, 0)")
        manga_db.commit()
        manga_db.close()
        self.assertEqual(manga_check.check_auto_chapter("Test", "No Chapter Table"), False)

    def test_auto_volume_check(self):
        self.assertEqual(manga_check.check_auto_volume("", 78, "Title"), False)
        self.assertEqual(manga_check.check_auto_volume("manga", "", "Title"), False)
        self.assertEqual(manga_check.check_auto_volume("manga only", 78, ""), False)
        shutil.copytree("./tests/data/test_check/auto_volume/Empty src/src/", manga_config.SOURCE_PATH)
        self.assertEqual(manga_check.check_auto_volume("Blue Box", 9,  "Empty Chapter"), False)
        shutil.rmtree(manga_config.SOURCE_PATH)

        shutil.copytree("./tests/data/test_check/auto_volume/No ext/src/", manga_config.SOURCE_PATH)
        self.assertEqual(manga_check.check_auto_volume("Blue Box", 9,  "Missing .ext Chapter"), False)
        shutil.rmtree(manga_config.SOURCE_PATH)

        shutil.copytree("./tests/data/test_check/auto_volume/No file/src/", manga_config.SOURCE_PATH)
        self.assertEqual(manga_check.check_auto_volume("Blue Box", 9,  "Not all files Chapter"), False)
        shutil.rmtree(manga_config.SOURCE_PATH)

        shutil.copytree("./tests/data/test_check/auto_volume/too many src/src/", manga_config.SOURCE_PATH)
        self.assertEqual(manga_check.check_auto_volume("Blue Box", 9,  "Working Chapter"), False)
        shutil.rmtree(manga_config.SOURCE_PATH)

        shutil.copytree("./tests/data/test_check/auto_volume/Working src/src/", manga_config.SOURCE_PATH)
        self.assertEqual(manga_check.check_auto_volume("Attack on Titan", 139,  "Working Chapter"), True)
        shutil.rmtree(manga_config.SOURCE_PATH)
        #DB Checks
        self.assertEqual(manga_check.check_auto_volume("Test", 8, "Not in Progress"), False)
        #gets passed above case
        manga_db = SQLite(manga_config.DB_FILE_PATH)
        manga_db.execute("INSERT INTO manga_progress (manga, current_chapter, current_volume, first_chapter_of_new_volume) VALUES(""Test"", 0, 0, 0)")
        manga_db.commit()
        manga_db.close()
        self.assertEqual(manga_check.check_auto_volume("Test", 8, "No Chapter Table"), False)
        self.assertEqual(manga_check.check_auto_volume("One Piece", 9,  "FCONV invalid"), False)

    def test_manual_single_chapter(self):
        self.assertEqual(manga_check.check_manual_single_chapter("", 78, "Title"), False)
        self.assertEqual(manga_check.check_manual_single_chapter("manga", "", "Title"), False)
        self.assertEqual(manga_check.check_manual_single_chapter("manga only", 78, ""), False)
        shutil.copytree("./tests/data/test_check/manual_single_chapter/Empty src/src/", manga_config.SOURCE_PATH)
        self.assertEqual(manga_check.check_manual_single_chapter("Blue Box", 9,  "Empty Chapter"), False)
        shutil.rmtree(manga_config.SOURCE_PATH)

        shutil.copytree("./tests/data/test_check/manual_single_chapter/No ext/src/", manga_config.SOURCE_PATH)
        self.assertEqual(manga_check.check_manual_single_chapter("Blue Box", 9,  "Missing .ext Chapter"), False)
        shutil.rmtree(manga_config.SOURCE_PATH)

        shutil.copytree("./tests/data/test_check/manual_single_chapter/No file/src/", manga_config.SOURCE_PATH)
        self.assertEqual(manga_check.check_manual_single_chapter("Blue Box", 9,  "Not all files Chapter"), False)
        shutil.rmtree(manga_config.SOURCE_PATH)

        #Dest
        shutil.copytree("./tests/data/test_check/manual_single_chapter/Non empty dest/dest/", manga_config.DESTINATION_PATH)
        self.assertEqual(manga_check.check_manual_single_chapter("Blue Box", 9,  "Non empty dest"), False)
        shutil.rmtree(manga_config.DESTINATION_PATH)

        shutil.copytree("./tests/data/test_check/manual_single_chapter/Working src/src/", manga_config.SOURCE_PATH)
        shutil.copytree("./tests/data/test_check/manual_single_chapter/empty dest/dest/", manga_config.DESTINATION_PATH)
        self.assertEqual(manga_check.check_manual_single_chapter("Attack on Titan", 139,  "Working Chapter"), True)
        shutil.rmtree(manga_config.SOURCE_PATH)
        shutil.rmtree(manga_config.DESTINATION_PATH)

    def test_manual_multiple_chapter(self):
        self.assertEqual(manga_check.check_manual_multiple_chapter(""), False)
        self.assertEqual(manga_check.check_manual_multiple_chapter("manga"), False)
        shutil.copytree("./tests/data/test_check/manual_multi_chapter/Empty src/src/", manga_config.SOURCE_PATH)
        self.assertEqual(manga_check.check_manual_multiple_chapter("Blue Box"), False)
        shutil.rmtree(manga_config.SOURCE_PATH)

        shutil.copytree("./tests/data/test_check/manual_multi_chapter/No ext/src/", manga_config.SOURCE_PATH)
        self.assertEqual(manga_check.check_manual_multiple_chapter("Blue Box"), False)
        shutil.rmtree(manga_config.SOURCE_PATH)

        shutil.copytree("./tests/data/test_check/manual_multi_chapter/No file/src/", manga_config.SOURCE_PATH)
        self.assertEqual(manga_check.check_manual_multiple_chapter("Blue Box"), False)
        shutil.rmtree(manga_config.SOURCE_PATH)

        shutil.copytree("./tests/data/test_check/manual_multi_chapter/bad directory names/src/", manga_config.SOURCE_PATH)
        self.assertEqual(manga_check.check_manual_multiple_chapter("Blue Box"), False)
        shutil.rmtree(manga_config.SOURCE_PATH)

        shutil.copytree("./tests/data/test_check/manual_multi_chapter/file dir src/src/", manga_config.SOURCE_PATH)
        self.assertEqual(manga_check.check_manual_multiple_chapter("Blue Box"), False)
        shutil.rmtree(manga_config.SOURCE_PATH)

        #Dest
        shutil.copytree("./tests/data/test_check/manual_multi_chapter/Non empty dest/dest/", manga_config.DESTINATION_PATH)
        self.assertEqual(manga_check.check_manual_multiple_chapter("Blue Box"), False)
        shutil.rmtree(manga_config.DESTINATION_PATH)

        shutil.copytree("./tests/data/test_check/manual_multi_chapter/Working src/src/", manga_config.SOURCE_PATH)
        shutil.copytree("./tests/data/test_check/manual_multi_chapter/empty dest/dest/", manga_config.DESTINATION_PATH)
        self.assertEqual(manga_check.check_manual_multiple_chapter("Attack on Titan"), True)
        shutil.rmtree(manga_config.SOURCE_PATH)
        shutil.rmtree(manga_config.DESTINATION_PATH)

    def test_manual_volume(self):
        self.assertEqual(manga_check.check_manual_volume("manga", "", "Title"), False)
        self.assertEqual(manga_check.check_manual_volume("manga", 15, ""), False)


if __name__ == '__main__':
    unittest.main()

