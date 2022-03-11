# test_manual_format.py
import shutil
import os
import unittest
import sys

sys.path.append("..")
from src.manga import Files
from src.manga import manga_config as mc
from src.manga import manga_format


class TestManualFormat(unittest.TestCase):

    def setUp(self):
        mc.SOURCE_PATH = "./tests/data/test_format/src/"
        mc.DESTINATION_PATH = "./tests/data/test_format/dest/"
        os.mkdir("./tests/data/test_format/dest/")

    def tearDown(self):
        try:
            shutil.rmtree("./tests/data/test_format/dest/")
            shutil.rmtree("./tests/data/test_format/src/")
        except:
            pass

    def test_single_chapter(self):
        # Working with title
        shutil.copytree("./tests/data/test_format/manual_single_chapter/src/", mc.SOURCE_PATH)
        manga_format.manual_single_chapter_format(mc.SOURCE_PATH, mc.DESTINATION_PATH, "Blue Box", 6, "Good Manga")
        new_chapter = Files(mc.DESTINATION_PATH + "006/")
        self.assertEqual(new_chapter.filenames[0], "Blue Box - CH006PG01 - Good Manga.jpg")
        self.assertEqual(new_chapter.filenames[16], "Blue Box - CH006PG17 - Good Manga.jpg")
        self.assertEqual(new_chapter.count, 17)
        shutil.rmtree(mc.SOURCE_PATH)

        # Working without title
        shutil.copytree("./tests/data/test_format/manual_single_chapter/src - no_title/", mc.SOURCE_PATH)
        manga_format.manual_single_chapter_format(mc.SOURCE_PATH, mc.DESTINATION_PATH, "Blue Box", 6, "Good Manga")
        new_chapter = Files(mc.DESTINATION_PATH + "006/")
        self.assertEqual(new_chapter.filenames[0], "Blue Box - CH006PG01 - Good Manga.jpg")
        self.assertEqual(new_chapter.filenames[16], "Blue Box - CH006PG17 - Good Manga.jpg")
        self.assertEqual(new_chapter.count, 17)
        shutil.rmtree(mc.SOURCE_PATH)

        # Single "Multi Chapter" format with a title
        shutil.copytree("./tests/data/test_format/manual_single_chapter/src - multi - title/", mc.SOURCE_PATH)
        manga_format.manual_multiple_chapter_format(mc.SOURCE_PATH, mc.DESTINATION_PATH, "Naruto")
        new_chapter = Files(mc.DESTINATION_PATH + "138/")
        self.assertEqual(new_chapter.filenames[0], "Naruto - CH138PG01 - Single Chapter.jpg")
        self.assertEqual(new_chapter.filenames[45], "Naruto - CH138PG46 - Single Chapter.jpg")
        self.assertEqual(new_chapter.count, 46)
        shutil.rmtree(mc.SOURCE_PATH)

        # Single "Multi Chapter" format with no title
        shutil.copytree("./tests/data/test_format/manual_single_chapter/src - multi - no_title/", mc.SOURCE_PATH)
        manga_format.manual_multiple_chapter_format(mc.SOURCE_PATH, mc.DESTINATION_PATH, "Naruto")
        new_chapter = Files(mc.DESTINATION_PATH + "139/")
        self.assertEqual(new_chapter.filenames[0], "Naruto - CH139PG01.jpg")
        self.assertEqual(new_chapter.filenames[45], "Naruto - CH139PG46.jpg")
        self.assertEqual(new_chapter.count, 46)

    def test_multi_chapter(self):
        shutil.copytree("./tests/data/test_format/manual_multi_chapter/src/", mc.SOURCE_PATH)
        manga_format.manual_multiple_chapter_format(mc.SOURCE_PATH, mc.DESTINATION_PATH, "Bleach")
        new_chapter = Files(mc.DESTINATION_PATH + "001/")
        self.assertEqual(new_chapter.filenames[0], "Bleach - CH001PG01 - New Series.jpeg")
        self.assertEqual(new_chapter.filenames[43], "Bleach - CH001PG44 - New Series.jpeg")
        self.assertEqual(new_chapter.count, 44)

        new_chapter = Files(mc.DESTINATION_PATH + "015/")
        self.assertEqual(new_chapter.filenames[0], "Bleach - CH015PG01.jpg")
        self.assertEqual(new_chapter.filenames[44], "Bleach - CH015PG45.jpg")
        self.assertEqual(new_chapter.count, 45)

        new_chapter = Files(mc.DESTINATION_PATH + "133/")
        self.assertEqual(new_chapter.filenames[0], "Bleach - CH133PG01 - Battle of Heaven and Earth.jpg")
        self.assertEqual(new_chapter.filenames[45], "Bleach - CH133PG46 - Battle of Heaven and Earth.jpg")
        self.assertEqual(new_chapter.count, 46)
        shutil.rmtree(mc.SOURCE_PATH)

    def test_manual_volume(self):
        shutil.copytree("./tests/data/test_format/manual_volume/src no_cover/", mc.SOURCE_PATH)
        manga_format.manual_volume_format(mc.SOURCE_PATH, mc.DESTINATION_PATH, "One Piece", 23, "Best Volume Ever!")
        new_volume = Files(mc.DESTINATION_PATH + "One Piece Volume 23 - Best Volume Ever!/")
        self.assertEqual(new_volume.filenames[0], "One Piece - CH096PG01 - New.jpg")
        self.assertEqual(new_volume.filenames[102], "One Piece - CH102PG14 - The End.jpeg")
        self.assertEqual(new_volume.count, 103)
        shutil.rmtree(mc.DESTINATION_PATH + "One Piece Volume 23 - Best Volume Ever!/")
        shutil.rmtree(mc.SOURCE_PATH)

        shutil.copytree("./tests/data/test_format/manual_volume/src cover/", mc.SOURCE_PATH)
        manga_format.manual_volume_format(mc.SOURCE_PATH, mc.DESTINATION_PATH, "Bleach", 26, "")
        new_volume = Files(mc.DESTINATION_PATH + "Bleach Volume 26/")
        self.assertEqual(new_volume.filenames[0], "Bleach - 26.jpg")
        self.assertEqual(new_volume.filenames[103], "Bleach - CH102PG14 - The End.jpeg")
        self.assertEqual(new_volume.count, 104)


if __name__ == '__main__':
    unittest.main()
