# test_auto_preview.py
import shutil
import unittest
# Before
# import src.manga.manga_config as manga_config
# import src.manga.manga_preview as manga_preview
import sys
sys.path.append("..")
# from src.manga.manga_config import manga_config
# from src.manga.manga_preview import manga_preview
from src.manga import manga_config
from src.manga import manga_preview



class TestAutoPreview(unittest.TestCase):

    def setUp(self):
        manga_config.SOURCE_PATH = "./tests/data/test_preview/src/"
        manga_config.DESTINATION_PATH = "./tests/data/test_preview/dest/"
        manga_config.MANGA_PATH = "./tests/data/test_preview/manga/"
        manga_config.DB_FILE_PATH = "./tests/data/test_preview/db/test_manga.db"
        shutil.copytree("./tests/data/db/", "./tests/data/test_preview/db/")
        shutil.copytree("./tests/data/manga/", "./tests/data/test_preview/manga/")

    def tearDown(self):
        try:
            shutil.rmtree("./tests/data/test_preview/db/")
            shutil.rmtree("./tests/data/test_preview/manga/")
            shutil.rmtree(manga_config.SOURCE_PATH)
        except:
            pass

    def test_auto_chapter_preview(self):
        shutil.copytree("./tests/data/test_preview/auto_chapter/Not One Piece/src/", manga_config.SOURCE_PATH)
        result = manga_preview.auto_chapter_preview("Attack on Titan", "Last Chapter")
        expected_result = ['Rename: 01.jpg to Attack on Titan - CH140PG01 - Last Chapter.jpg', 'Rename: 02.jpg to Attack on Titan - CH140PG02 - Last Chapter.jpg', 'Rename: 03.jpg to Attack on Titan - CH140PG03 - Last Chapter.jpg', 'Rename: 04.jpg to Attack on Titan - CH140PG04 - Last Chapter.jpg', 'Rename: 05.jpg to Attack on Titan - CH140PG05 - Last Chapter.jpg', 'Rename: 06.jpg to Attack on Titan - CH140PG06 - Last Chapter.jpg', 'Rename: 07.jpg to Attack on Titan - CH140PG07 - Last Chapter.jpg', 'Rename: 08.jpg to Attack on Titan - CH140PG08 - Last Chapter.jpg', 'Rename: 09.jpg to Attack on Titan - CH140PG09 - Last Chapter.jpg', 'Rename: 10.jpg to Attack on Titan - CH140PG10 - Last Chapter.jpg', 'Rename: 11.jpg to Attack on Titan - CH140PG11 - Last Chapter.jpg', 'Rename: 12.jpg to Attack on Titan - CH140PG12 - Last Chapter.jpg', 'Rename: 13.jpg to Attack on Titan - CH140PG13 - Last Chapter.jpg', 'Rename: 14.jpg to Attack on Titan - CH140PG14 - Last Chapter.jpg', 'Rename: 15.jpg to Attack on Titan - CH140PG15 - Last Chapter.jpg', 'Rename: 16.jpg to Attack on Titan - CH140PG16 - Last Chapter.jpg', 'Rename: 17.jpg to Attack on Titan - CH140PG17 - Last Chapter.jpg', 'Rename: 18.jpg to Attack on Titan - CH140PG18 - Last Chapter.jpg']
        self.assertEqual(result, expected_result)
        shutil.rmtree(manga_config.SOURCE_PATH)

        shutil.copytree("./tests/data/test_preview/auto_chapter/One Piece/src/", manga_config.SOURCE_PATH)
        result = manga_preview.auto_chapter_preview("One Piece", "Great Stuff")
        expected_result = ['Rename: page01.jpeg to One Piece - CH1014PG01 - Great Stuff.jpeg', 'Rename: page02.jpeg to One Piece - CH1014PG02 - Great Stuff.jpeg', 'Rename: page03.jpeg to One Piece - CH1014PG03 - Great Stuff.jpeg', 'Rename: page04.jpeg to One Piece - CH1014PG04 - Great Stuff.jpeg', 'Rename: page05.jpeg to One Piece - CH1014PG05 - Great Stuff.jpeg', 'Rename: page06.jpeg to One Piece - CH1014PG06 - Great Stuff.jpeg', 'Rename: page07.jpeg to One Piece - CH1014PG07 - Great Stuff.jpeg', 'Rename: page08.jpeg to One Piece - CH1014PG08 - Great Stuff.jpeg', 'Rename: page09.jpeg to One Piece - CH1014PG09 - Great Stuff.jpeg', 'Rename: page10.jpeg to One Piece - CH1014PG10 - Great Stuff.jpeg', 'Rename: page11.jpeg to One Piece - CH1014PG11 - Great Stuff.jpeg', 'Rename: page12.jpeg to One Piece - CH1014PG12 - Great Stuff.jpeg', 'Rename: page13.jpeg to One Piece - CH1014PG13 - Great Stuff.jpeg', 'Rename: page14.jpeg to One Piece - CH1014PG14 - Great Stuff.jpeg']
        self.assertEqual(result, expected_result)
        shutil.rmtree(manga_config.SOURCE_PATH)

    def test_auto_volume_preview(self):
        shutil.copytree("./tests/data/test_preview/auto_volume/Not One Piece/src/", manga_config.SOURCE_PATH)
        result = manga_preview.auto_volume_preview("Attack on Titan", 139, "Last Volume")
        expected_result = ['Rename: 135/ to Attack on Titan Volume 034 - Last Volume/', 'Rename: 136/ to Attack on Titan Volume 034 - Last Volume/', 'Rename: 137/ to Attack on Titan Volume 034 - Last Volume/', 'Rename: 138/ to Attack on Titan Volume 034 - Last Volume/', 'Rename: 139/ to Attack on Titan Volume 034 - Last Volume/']
        self.assertEqual(result, expected_result)
        shutil.rmtree(manga_config.SOURCE_PATH)

        shutil.copytree("./tests/data/test_preview/auto_volume/One Piece/src/", manga_config.SOURCE_PATH)
        result = manga_preview.auto_volume_preview("One Piece", 1004, "Straw Hat Luffy")
        expected_result = ['Rename: 0995/ to One Piece Volume 099 - Straw Hat Luffy/', 'Rename: 0996/ to One Piece Volume 099 - Straw Hat Luffy/', 'Rename: 0997/ to One Piece Volume 099 - Straw Hat Luffy/', 'Rename: 0998/ to One Piece Volume 099 - Straw Hat Luffy/', 'Rename: 0999/ to One Piece Volume 099 - Straw Hat Luffy/', 'Rename: 1000/ to One Piece Volume 099 - Straw Hat Luffy/', 'Rename: 1001/ to One Piece Volume 099 - Straw Hat Luffy/', 'Rename: 1002/ to One Piece Volume 099 - Straw Hat Luffy/', 'Rename: 1003/ to One Piece Volume 099 - Straw Hat Luffy/', 'Rename: 1004/ to One Piece Volume 099 - Straw Hat Luffy/']
        self.assertEqual(result, expected_result)
        shutil.rmtree(manga_config.SOURCE_PATH)


if __name__ == '__main__':
    unittest.main()
