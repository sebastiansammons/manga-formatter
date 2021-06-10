# test_manual_format.py
import shutil
import os
import unittest
from ..src.manga import Files
from ..src.manga import manga_config
from ..src.manga import manga_format


class TestManualFormat(unittest.TestCase):

    def setUp(self):
        manga_config.SOURCE_PATH = "./manga-formatter/tests/data/test_format/src/"
        manga_config.DESTINATION_PATH = "./manga-formatter/tests/data/test_format/dest/"
        os.mkdir("./manga-formatter/tests/data/test_format/dest/")

    def tearDown(self):
        try:
            shutil.rmtree("./manga-formatter/tests/data/test_format/dest/")
            shutil.rmtree("./manga-formatter/tests/data/test_format/src/")
        except:
            pass

    def test_single_chapter(self):
        shutil.copytree("./manga-formatter/tests/data/test_format/manual_single_chapter/src/", manga_config.SOURCE_PATH)
        manga_format.manual_single_chapter_format("Blue Box", 6, "Good Manga")
        new_chapter = Files(manga_config.DESTINATION_PATH + "006/")
        self.assertEqual(new_chapter.filenames[0], "Blue Box - CH006PG01 - Good Manga.jpg")
        self.assertEqual(new_chapter.filenames[16], "Blue Box - CH006PG17 - Good Manga.jpg")
        self.assertEqual(new_chapter.count, 17)
        shutil.rmtree(manga_config.SOURCE_PATH)

        shutil.copytree("./manga-formatter/tests/data/test_format/manual_single_chapter/src - multi/", manga_config.SOURCE_PATH)
        manga_format.manual_multiple_chapter_format("Naruto")
        new_chapter = Files(manga_config.DESTINATION_PATH + "138/")
        self.assertEqual(new_chapter.filenames[0], "Naruto - CH138PG01 - Single Chapter.jpg")
        self.assertEqual(new_chapter.filenames[45], "Naruto - CH138PG46 - Single Chapter.jpg")
        self.assertEqual(new_chapter.count, 46)


    def test_multi_chapter(self):
        shutil.copytree("./manga-formatter/tests/data/test_format/manual_multi_chapter/src/", manga_config.SOURCE_PATH)
        manga_format.manual_multiple_chapter_format("Bleach")
        new_chapter = Files(manga_config.DESTINATION_PATH + "001/")
        self.assertEqual(new_chapter.filenames[0], "Bleach - CH001PG01 - New Series.jpeg")
        self.assertEqual(new_chapter.filenames[43], "Bleach - CH001PG44 - New Series.jpeg")
        self.assertEqual(new_chapter.count, 44)

        new_chapter = Files(manga_config.DESTINATION_PATH + "015/")
        self.assertEqual(new_chapter.filenames[0], "Bleach - CH015PG01 - Kinda Cool.jpg")
        self.assertEqual(new_chapter.filenames[44], "Bleach - CH015PG45 - Kinda Cool.jpg")
        self.assertEqual(new_chapter.count, 45)

        new_chapter = Files(manga_config.DESTINATION_PATH + "133/")
        self.assertEqual(new_chapter.filenames[0], "Bleach - CH133PG01 - Battle of Heaven and Earth.jpg")
        self.assertEqual(new_chapter.filenames[45], "Bleach - CH133PG46 - Battle of Heaven and Earth.jpg")
        self.assertEqual(new_chapter.count, 46)
        shutil.rmtree(manga_config.SOURCE_PATH)

    def test_manual_volume(self):
        shutil.copytree("./manga-formatter/tests/data/test_format/manual_volume/src/", manga_config.SOURCE_PATH)
        manga_format.manual_volume_format("One Piece", 23, "Best Volume Ever!")
        new_volume = Files(manga_config.DESTINATION_PATH + "One Piece Volume 23 - Best Volume Ever!/")
        self.assertEqual(new_volume.filenames[0], "One Piece - CH096PG01 - New.jpg")
        self.assertEqual(new_volume.filenames[102], "One Piece - CH102PG14 - The End.jpeg")
        self.assertEqual(new_volume.count, 103)



if __name__ == '__main__':
    unittest.main()

