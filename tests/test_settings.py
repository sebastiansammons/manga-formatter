# test_settings.py
import unittest
from unittest.case import SkipTest
import sys

sys.path.append("..")
from src.manga import manga_config
from src.manga import manga_sql


@SkipTest
class TestSettings(unittest.TestCase):

    def setUp(self):
        manga_config.DB_FILE_PATH = "./tests/data/db/test_manga.db"

    def test_active_manga(self):
        expected_active_manga = ["Attack on Titan", "Blue Box", "My Hero Academia", "One Piece"]
        active_manga = manga_sql.get_active_manga()
        self.assertEqual(active_manga, expected_active_manga)

    def test_chapter_status(self):
        expected_active_manga = ["Attack on Titan", "Blue Box", "My Hero Academia", "One Piece"]
        expected_manga_chapter = [139, 6, 313, 1013]
        active_manga, manga_chapter = manga_sql.get_chapter_status()
        self.assertEqual(active_manga, expected_active_manga)
        self.assertEqual(manga_chapter, expected_manga_chapter)

    def test_volume_status(self):
        expected_active_manga = ["Attack on Titan", "Blue Box", "My Hero Academia", "One Piece"]
        expected_manga_volume = [33, 0, 30, 98]
        active_manga, manga_volume = manga_sql.get_volume_status()
        self.assertEqual(active_manga, expected_active_manga)
        self.assertEqual(manga_volume, expected_manga_volume)

if __name__ == '__main__':
    unittest.main()
