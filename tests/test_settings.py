# test_status.py
import os
import shutil
import unittest
import sys

sys.path.append("..")
from src.manga import manga_config as mc
from src.manga import manga_sql as msql
from src.manga import manga_settings


class TestSettings(unittest.TestCase):

    def setUp(self):
        mc.DB_FILE_PATH = "./tests/data/test_settings/test_manga.db"
        shutil.copy("./tests/data/test_settings/db/test_manga.db", "./tests/data/test_settings/test_manga.db")

    def tearDown(self):
        try:
            os.remove("./tests/data/test_settings/test_manga.db")
        except:
            pass

    def test_active_to_inactive(self):
        active_manga_before = ["Attack on Titan", "Blue Box", "My Hero Academia", "One Piece"]
        active_manga_after = ["Blue Box", "My Hero Academia", "One Piece"]
        inactive_manga_before = ["Bleach", "Boruto", "Dr. STONE", "Naruto", "Platinum End", "Samurai 8", "The Promised Neverland", "Yu Yu Hakusho"]
        inactive_manga_after = ["Attack on Titan", "Bleach", "Boruto", "Dr. STONE", "Naruto", "Platinum End", "Samurai 8", "The Promised Neverland", "Yu Yu Hakusho"]
        active_manga = msql.get_active_manga()
        inactive_manga = msql.get_inactive_manga()
        self.assertEqual(active_manga, active_manga_before)
        self.assertEqual(inactive_manga, inactive_manga_before)
        manga_settings.active_to_inactive("Attack on Titan")
        active_manga = msql.get_active_manga()
        inactive_manga = msql.get_inactive_manga()
        self.assertEqual(active_manga, active_manga_after)
        self.assertEqual(inactive_manga, inactive_manga_after)

    def test_inactive_to_active(self):
        active_manga_before = ["Attack on Titan", "Blue Box", "My Hero Academia", "One Piece"]
        active_manga_after = ["Attack on Titan", "Bleach", "Blue Box", "My Hero Academia", "One Piece"]
        inactive_manga_before = ["Bleach", "Boruto", "Dr. STONE", "Naruto", "Platinum End", "Samurai 8", "The Promised Neverland", "Yu Yu Hakusho"]
        inactive_manga_after = ["Boruto", "Dr. STONE", "Naruto", "Platinum End", "Samurai 8", "The Promised Neverland", "Yu Yu Hakusho"]
        active_manga = msql.get_active_manga()
        inactive_manga = msql.get_inactive_manga()
        self.assertEqual(active_manga, active_manga_before)
        self.assertEqual(inactive_manga, inactive_manga_before)
        manga_settings.inactive_to_active("Bleach")
        active_manga = msql.get_active_manga()
        inactive_manga = msql.get_inactive_manga()
        self.assertEqual(active_manga, active_manga_after)
        self.assertEqual(inactive_manga, inactive_manga_after)


if __name__ == '__main__':
    unittest.main()
