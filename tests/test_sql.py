# test_status.py
import os
import shutil
import unittest
import sys

sys.path.append("..")
from src.manga import manga_config as mc
from src.manga import manga_sql as msql


class TestStatus(unittest.TestCase):

    def setUp(self):
        mc.DB_FILE_PATH = "./tests/data/test_sql/test_manga.db"
        shutil.copy("./tests/data/test_sql/db/test_manga.db", "./tests/data/test_sql/test_manga.db")

    def tearDown(self):
        try:
            os.remove("./tests/data/test_sql/test_manga.db")
        except:
            pass

    def test_active_manga(self):
        expected_active_manga = ["Attack on Titan", "Blue Box", "My Hero Academia", "One Piece"]
        active_manga = msql.get_active_manga()
        self.assertEqual(active_manga, expected_active_manga)

    def test_chapter_status(self):
        expected_active_manga = ["Attack on Titan", "Blue Box", "My Hero Academia", "One Piece"]
        expected_manga_chapter = [139, 6, 313, 1013]
        active_manga, manga_chapter = msql.get_chapter_status()
        self.assertEqual(active_manga, expected_active_manga)
        self.assertEqual(manga_chapter, expected_manga_chapter)

    def test_volume_status(self):
        expected_active_manga = ["Attack on Titan", "Blue Box", "My Hero Academia", "One Piece"]
        expected_manga_volume = [33, 0, 30, 98]
        active_manga, manga_volume = msql.get_volume_status()
        self.assertEqual(active_manga, expected_active_manga)
        self.assertEqual(manga_volume, expected_manga_volume)

    def test_get_manga(self):
        expected_manga = ["Attack on Titan", "Bleach", "Blue Box", "Boruto", "Dr. STONE", "My Hero Academia", "Naruto", "One Piece", "Platinum End", "Samurai 8", "The Promised Neverland", "Yu Yu Hakusho"]
        manga = msql.get_manga()
        self.assertEqual(manga, expected_manga)

    def test_inactive_manga(self):
        expected_manga = ["Bleach", "Boruto", "Dr. STONE", "Naruto", "Platinum End", "Samurai 8", "The Promised Neverland", "Yu Yu Hakusho"]
        inactive_manga = msql.get_inactive_manga()
        self.assertEqual(inactive_manga, expected_manga)

    def test_get_new_chapter_number(self):
        expected_new_chapter_number = 1014
        new_chapter_number = msql.get_new_chapter_number("One Piece")
        self.assertEqual(new_chapter_number, expected_new_chapter_number)

    def test_update_new_chapter(self):
        expected_next_chapter_number = 8
        msql.update_new_chapter("Blue Box", 7, "TEST")
        new_chapter_number = msql.get_new_chapter_number("Blue Box")
        # Inserting new chapter which is 7, chapter after that is 8
        self.assertEqual(new_chapter_number, expected_next_chapter_number)

    def test_get_new_volume_nubmer(self):
        expected_new_volume_number = 34
        expected_first_chapter_in_volume = 135
        new_volume_number, first_chapter_in_volume = msql.get_new_volume_number("Attack on Titan")
        self.assertEqual(new_volume_number, expected_new_volume_number)
        self.assertEqual(first_chapter_in_volume, expected_first_chapter_in_volume)

    def test_update_new_volume(self):
        expected_new_volume_number = 35
        expected_first_chapter_in_volume = 140
        msql.update_new_volume("Attack on Titan", 34, 139, "Freedom")
        new_volume_number, first_chapter_in_volume = msql.get_new_volume_number("Attack on Titan")
        self.assertEqual(new_volume_number, expected_new_volume_number)
        self.assertEqual(first_chapter_in_volume, expected_first_chapter_in_volume)

    def test_check_auto_chapter_sql(self):
        # Bad manga
        self.assertEqual(msql.check_auto_chapter_sql("One Punch Man"), False)
        # Good manga
        self.assertEqual(msql.check_auto_chapter_sql("One Piece"), True)

    def test_check_auto_volume_sql(self):
        # Bad manga
        self.assertEqual(msql.check_auto_volume_sql("One Punch Man", 10), False)
        # Bad last_chapter_of_new_volume
        self.assertEqual(msql.check_auto_volume_sql("One Piece", 10), False)
        # Good manga
        self.assertEqual(msql.check_auto_volume_sql("One Piece", 1022), True)

    def test_new_manga(self):
        manga = "One Punch Man"
        writer = "One"
        illustrator = "Other guy"
        completed = False
        msql.new_manga(manga, writer, illustrator, completed)
        expected_chapter_number = 1
        new_chapter_number = msql.get_new_chapter_number("One Punch Man")
        self.assertEqual(new_chapter_number, expected_chapter_number)
        expected_volume_number = 1
        expected_first_chapter_in_volume = 1
        new_volume_number, first_chapter_in_volume = msql.get_new_volume_number("One Punch Man")
        self.assertEqual(new_volume_number, expected_volume_number)
        self.assertEqual(first_chapter_in_volume, expected_first_chapter_in_volume)
        writer_result = msql.get_manga_author("One Punch Man")
        self.assertEqual(writer, writer_result)
        illustrator_result = msql.get_manga_illustrator("One Punch Man")
        self.assertEqual(illustrator, illustrator_result)


if __name__ == '__main__':
    unittest.main()
