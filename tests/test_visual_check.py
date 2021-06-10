# test_visual_check
import unittest
import shutil
import os
from ..src.manga import manga_config
from ..src.manga import manga_format



class TestVisualCheck(unittest.TestCase):

    def setUp(self):
        manga_config.DB_FILE_PATH = "./manga-formatter/tests/data/test_visual_check/db/test_manga.db"
        manga_config.SOURCE_PATH = "./manga-formatter/tests/data/test_visual_check/src/"        
        manga_config.MANGA_PATH = "./manga-formatter/tests/data/test_visual_check/manga/"
        try:
            shutil.copytree("./manga-formatter/tests/data/db/", "./manga-formatter/tests/data/test_visual_check/db/")
            shutil.copytree("./manga-formatter/tests/data/manga/", "./manga-formatter/tests/data/test_visual_check/manga/")
        except:
            pass

    def tearDown(self):
        try:
            shutil.rmtree("./manga-formatter/tests/data/test_visual_check/db/")
            shutil.rmtree(manga_config.SOURCE_PATH)
        except:
            pass

    def test_auto_chapter(self):
        shutil.copytree("./manga-formatter/tests/data/test_visual_check/auto_chapter/Not One Piece/src/", manga_config.SOURCE_PATH)
        
        manga_format.auto_chapter_format("Attack on Titan", "Last Chapter")
        shutil.rmtree(manga_config.SOURCE_PATH)

        shutil.copytree("./manga-formatter/tests/data/test_visual_check/auto_chapter/One Piece/src/", manga_config.SOURCE_PATH)
        manga_format.auto_chapter_format("One Piece", "Great Stuff")
        shutil.rmtree(manga_config.SOURCE_PATH)



    def test_auto_volume(self):
        shutil.copytree("./manga-formatter/tests/data/test_visual_check/auto_volume/Not One Piece/src/", manga_config.SOURCE_PATH)
        manga_format.auto_volume_format("Attack on Titan", 139, "Last Volume")
        shutil.rmtree(manga_config.SOURCE_PATH)

        shutil.copytree("./manga-formatter/tests/data/test_visual_check/auto_volume/One Piece/src/", manga_config.SOURCE_PATH)
        manga_format.auto_volume_format("One Piece", 1004, "Straw Hat Luffy")
        shutil.rmtree(manga_config.SOURCE_PATH)


    def test_single_chapter(self):
        try:
            os.mkdir("./manga-formatter/tests/data/test_visual_check/dest/")
        except:
            pass
        manga_config.DESTINATION_PATH = "./manga-formatter/tests/data/test_visual_check/dest/single_chapter/"
        os.mkdir(manga_config.DESTINATION_PATH)
        shutil.copytree("./manga-formatter/tests/data/test_visual_check/manual_single_chapter/src/", manga_config.SOURCE_PATH)
        manga_format.manual_single_chapter_format("Blue Box", 6, "Good Manga")
        
        shutil.rmtree(manga_config.SOURCE_PATH)
        manga_config.DESTINATION_PATH = "./manga-formatter/tests/data/test_visual_check/dest/single_multi_chapter/"
        os.mkdir(manga_config.DESTINATION_PATH)
        shutil.copytree("./manga-formatter/tests/data/test_visual_check/manual_single_chapter/src - multi/", manga_config.SOURCE_PATH)
        manga_format.manual_multiple_chapter_format("Naruto")
        


    def test_multi_chapter(self):
        try:
            os.mkdir("./manga-formatter/tests/data/test_visual_check/dest/")
        except:
            pass
        manga_config.DESTINATION_PATH = "./manga-formatter/tests/data/test_visual_check/dest/multi_chapter/"
        os.mkdir(manga_config.DESTINATION_PATH)
        shutil.copytree("./manga-formatter/tests/data/test_visual_check/manual_multi_chapter/src/", manga_config.SOURCE_PATH)
        manga_format.manual_multiple_chapter_format("Bleach")
        

    def test_manual_volume(self):
        try:
            os.mkdir("./manga-formatter/tests/data/test_visual_check/dest/")
        except:
            pass
        manga_config.DESTINATION_PATH = "./manga-formatter/tests/data/test_visual_check/dest/manual_volume/"
        os.mkdir(manga_config.DESTINATION_PATH)
        shutil.copytree("./manga-formatter/tests/data/test_visual_check/manual_volume/src/", manga_config.SOURCE_PATH)
        manga_format.manual_volume_format("One Piece", 23, "Best Volume Ever!")


if __name__ == '__main__':
    unittest.main()

