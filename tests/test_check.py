# test_check.py
import shutil
import unittest
import sys

sys.path.append("..")
from src.manga import SQLite
from src.manga import manga_config as mc
from src.manga import manga_check


class TestCheck(unittest.TestCase):

    def setUp(self):
        mc.DB_FILE_PATH = "./tests/data/test_check/db/test_manga.db"
        mc.SOURCE_PATH = "./tests/data/test_check/src/"
        mc.DESTINATION_PATH = "./tests/data/test_check/dest/"
        mc.MANGA_PATH = "./tests/data/test_check/manga/"
        shutil.copytree("./tests/data/db/", "./tests/data/test_check/db/")
        shutil.copytree("./tests/data/manga/", "./tests/data/test_check/manga/")

    def tearDown(self):
        try:
            shutil.rmtree("./tests/data/test_check/db/")
            shutil.rmtree("./tests/data/test_check/manga/")
            shutil.rmtree(mc.SOURCE_PATH)
        except:
            pass
        try:
            shutil.rmtree(mc.DESTINATION_PATH)
        except:
            pass

    def test_auto_chapter_check(self):
        self.assertEqual(manga_check.check_auto_chapter("", "Title Only"), False)
        self.assertEqual(manga_check.check_auto_chapter("manga only", ""), False)
        shutil.copytree("./tests/data/test_check/auto_chapter/Empty src/src/", mc.SOURCE_PATH)
        self.assertEqual(manga_check.check_auto_chapter("One Piece", "Empty Volume"), False)
        shutil.rmtree(mc.SOURCE_PATH)

        shutil.copytree("./tests/data/test_check/auto_chapter/No ext/src/", mc.SOURCE_PATH)
        self.assertEqual(manga_check.check_auto_chapter("One Piece", "Missing .ext Volume"), False)
        shutil.rmtree(mc.SOURCE_PATH)

        shutil.copytree("./tests/data/test_check/auto_chapter/No file/src/", mc.SOURCE_PATH)
        self.assertEqual(manga_check.check_auto_chapter("One Piece", "Not all files Volume"), False)
        shutil.rmtree(mc.SOURCE_PATH)

        shutil.copytree("./tests/data/test_check/auto_chapter/Working src/src/", mc.SOURCE_PATH)
        self.assertEqual(manga_check.check_auto_chapter("One Piece", "Working Volume"), True)
        shutil.rmtree(mc.SOURCE_PATH)
        # DB Checks
        self.assertEqual(manga_check.check_auto_chapter("Test", "Not in Progress"), False)
        manga_db = SQLite(mc.DB_FILE_PATH)
        manga_db.execute("INSERT INTO manga_progress (manga, current_chapter, current_volume, first_chapter_of_new_volume) VALUES(""Test"", 0, 0, 0)")
        manga_db.commit()
        manga_db.close()
        self.assertEqual(manga_check.check_auto_chapter("Test", "No Chapter Table"), False)

    def test_auto_volume_check(self):
        self.assertEqual(manga_check.check_auto_volume("", 78), False)
        self.assertEqual(manga_check.check_auto_volume("manga", ""), False)
        self.assertEqual(manga_check.check_auto_volume("manga only", 78), False)
        shutil.copytree("./tests/data/test_check/auto_volume/Empty src/src/", mc.SOURCE_PATH)
        self.assertEqual(manga_check.check_auto_volume("Blue Box", 9), False)
        shutil.rmtree(mc.SOURCE_PATH)

        shutil.copytree("./tests/data/test_check/auto_volume/No ext/src/", mc.SOURCE_PATH)
        self.assertEqual(manga_check.check_auto_volume("Blue Box", 9), False)
        shutil.rmtree(mc.SOURCE_PATH)

        shutil.copytree("./tests/data/test_check/auto_volume/No file/src/", mc.SOURCE_PATH)
        self.assertEqual(manga_check.check_auto_volume("Blue Box", 9), False)
        shutil.rmtree(mc.SOURCE_PATH)

        shutil.copytree("./tests/data/test_check/auto_volume/too many src/src/", mc.SOURCE_PATH)
        self.assertEqual(manga_check.check_auto_volume("Blue Box", 9), False)
        shutil.rmtree(mc.SOURCE_PATH)

        shutil.copytree("./tests/data/test_check/auto_volume/Working src/src/", mc.SOURCE_PATH)
        self.assertEqual(manga_check.check_auto_volume("Attack on Titan", 139), True)
        shutil.rmtree(mc.SOURCE_PATH)
        # DB Checks
        self.assertEqual(manga_check.check_auto_volume("Test", 8), False)
        # gets passed above case
        manga_db = SQLite(mc.DB_FILE_PATH)
        manga_db.execute("INSERT INTO manga_progress (manga, current_chapter, current_volume, first_chapter_of_new_volume) VALUES(""Test"", 0, 0, 0)")
        manga_db.commit()
        manga_db.close()
        self.assertEqual(manga_check.check_auto_volume("Test", 8), False)
        self.assertEqual(manga_check.check_auto_volume("One Piece", 9), False)

    def test_manual_single_chapter(self):
        # Bad manga title
        self.assertEqual(manga_check.check_manual_single_chapter(mc.SOURCE_PATH, "", 78), False)
        # Bad manga number
        self.assertEqual(manga_check.check_manual_single_chapter(mc.SOURCE_PATH, "manga", ""), False)
        
        # Bad source, empty
        shutil.copytree("./tests/data/test_check/manual_single_chapter/Empty src/src/", mc.SOURCE_PATH)
        self.assertEqual(manga_check.check_manual_single_chapter(mc.SOURCE_PATH, "Blue Box", 9), False)
        shutil.rmtree(mc.SOURCE_PATH)
        # Bad source, file with no extension
        shutil.copytree("./tests/data/test_check/manual_single_chapter/No ext/src/", mc.SOURCE_PATH)
        self.assertEqual(manga_check.check_manual_single_chapter(mc.SOURCE_PATH, "Blue Box", 9), False)
        shutil.rmtree(mc.SOURCE_PATH)
        # Bad source, not all items in directory are files
        shutil.copytree("./tests/data/test_check/manual_single_chapter/No file/src/", mc.SOURCE_PATH)
        self.assertEqual(manga_check.check_manual_single_chapter(mc.SOURCE_PATH, "Blue Box", 9), False)
        shutil.rmtree(mc.SOURCE_PATH)

        #Working manual chapter
        shutil.copytree("./tests/data/test_check/manual_single_chapter/Working src/src/", mc.SOURCE_PATH)
        self.assertEqual(manga_check.check_manual_single_chapter(mc.SOURCE_PATH, "Attack on Titan", 139), True)
        shutil.rmtree(mc.SOURCE_PATH)

    def test_manual_multiple_chapter(self):
        # Bad manga entry
        self.assertEqual(manga_check.check_manual_multiple_chapter(mc.SOURCE_PATH, ""), False)
        # Empty source
        shutil.copytree("./tests/data/test_check/manual_multi_chapter/Empty src/src", mc.SOURCE_PATH)
        shutil.copytree("./tests/data/test_check/manual_multi_chapter/empty dest/dest/", mc.DESTINATION_PATH)
        self.assertEqual(manga_check.check_manual_multiple_chapter(mc.SOURCE_PATH, "Blue Box"), False)
        shutil.rmtree(mc.SOURCE_PATH)
        shutil.rmtree(mc.DESTINATION_PATH)
        # bad file
        shutil.copytree("./tests/data/test_check/manual_multi_chapter/No ext/src/", mc.SOURCE_PATH)
        shutil.copytree("./tests/data/test_check/manual_multi_chapter/empty dest/dest/", mc.DESTINATION_PATH)
        self.assertEqual(manga_check.check_manual_multiple_chapter(mc.SOURCE_PATH, "Blue Box"), False)
        shutil.rmtree(mc.SOURCE_PATH)
        shutil.rmtree(mc.DESTINATION_PATH)
        # directory in chapter, invalid
        shutil.copytree("./tests/data/test_check/manual_multi_chapter/No file/src/", mc.SOURCE_PATH)
        shutil.copytree("./tests/data/test_check/manual_multi_chapter/empty dest/dest/", mc.DESTINATION_PATH)
        self.assertEqual(manga_check.check_manual_multiple_chapter(mc.SOURCE_PATH, "Blue Box"), False)
        shutil.rmtree(mc.SOURCE_PATH)
        shutil.rmtree(mc.DESTINATION_PATH)
        # invalid directory names
        shutil.copytree("./tests/data/test_check/manual_multi_chapter/bad directory names/src/", mc.SOURCE_PATH)
        shutil.copytree("./tests/data/test_check/manual_multi_chapter/empty dest/dest/", mc.DESTINATION_PATH)
        self.assertEqual(manga_check.check_manual_multiple_chapter(mc.SOURCE_PATH, "Blue Box"), False)
        shutil.rmtree(mc.SOURCE_PATH)
        shutil.rmtree(mc.DESTINATION_PATH)
        # files in src, ignore files
        shutil.copytree("./tests/data/test_check/manual_multi_chapter/file dir src/src/", mc.SOURCE_PATH)
        shutil.copytree("./tests/data/test_check/manual_multi_chapter/empty dest/dest/", mc.DESTINATION_PATH)
        self.assertEqual(manga_check.check_manual_multiple_chapter(mc.SOURCE_PATH, "Blue Box"), True)
        shutil.rmtree(mc.SOURCE_PATH)
        shutil.rmtree(mc.DESTINATION_PATH)
        # one directory is empty
        shutil.copytree("./tests/data/test_check/manual_multi_chapter/empty dir/src/", mc.SOURCE_PATH)
        shutil.copytree("./tests/data/test_check/manual_multi_chapter/empty dest/dest/", mc.DESTINATION_PATH)
        self.assertEqual(manga_check.check_manual_multiple_chapter(mc.SOURCE_PATH, "Blue Box"), False)
        shutil.rmtree(mc.SOURCE_PATH)
        shutil.rmtree(mc.DESTINATION_PATH)

        # Working chapters
        shutil.copytree("./tests/data/test_check/manual_multi_chapter/Working src/src/", mc.SOURCE_PATH)
        shutil.copytree("./tests/data/test_check/manual_multi_chapter/empty dest/dest/", mc.DESTINATION_PATH)
        self.assertEqual(manga_check.check_manual_multiple_chapter(mc.SOURCE_PATH, "Attack on Titan"), True)
        shutil.rmtree(mc.SOURCE_PATH)
        shutil.rmtree(mc.DESTINATION_PATH)

    def test_manual_volume(self):
        # Bad number entry
        self.assertEqual(manga_check.check_manual_volume(mc.SOURCE_PATH, mc.DESTINATION_PATH, "Blue Box", ""), False)
        
        # too many files
        shutil.copytree("./tests/data/test_check/manual_volume/too many files/src/", mc.SOURCE_PATH)
        shutil.copytree("./tests/data/test_check/manual_volume/empty dest/dest/", mc.DESTINATION_PATH)
        self.assertEqual(manga_check.check_manual_volume(mc.SOURCE_PATH, mc.DESTINATION_PATH, "Naruto", 15), False)
        shutil.rmtree(mc.SOURCE_PATH)
        shutil.rmtree(mc.DESTINATION_PATH)

        # non empty dest
        shutil.copytree("./tests/data/test_check/manual_volume/Working src/src/", mc.SOURCE_PATH)
        shutil.copytree("./tests/data/test_check/manual_volume/non empty dest/dest/", mc.DESTINATION_PATH)
        self.assertEqual(manga_check.check_manual_volume(mc.SOURCE_PATH, mc.DESTINATION_PATH, "Naruto", 15), False)
        shutil.rmtree(mc.SOURCE_PATH)
        shutil.rmtree(mc.DESTINATION_PATH)
        
        
        # working
        shutil.copytree("./tests/data/test_check/manual_volume/Working src/src/", mc.SOURCE_PATH)
        shutil.copytree("./tests/data/test_check/manual_volume/empty dest/dest/", mc.DESTINATION_PATH)
        self.assertEqual(manga_check.check_manual_volume(mc.SOURCE_PATH, mc.DESTINATION_PATH, "Bleach", 30), True)
        shutil.rmtree(mc.SOURCE_PATH)
        shutil.rmtree(mc.DESTINATION_PATH)

if __name__ == '__main__':
    unittest.main()
