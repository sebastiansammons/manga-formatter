# test_epub.py
import os
import shutil
import unittest
import sys

sys.path.append("..")
from src.epub import epub_gen


class TestEPUB(unittest.TestCase):

    def test_split_images(self):
        src = "./tests/data/test_epub/split_images/src/"
        dest = "./tests/data/test_epub/split_images/dest/"
        os.mkdir(dest)
        epub_gen.split_images(src, dest)
        expected_result = ["One Piece - CH0998PG01 - Ancient Types.jpg", "One Piece - CH0998PG02 - Ancient Types.jpg", "One Piece - CH0998PG03 - Ancient Types.jpg", "One Piece - CH0998PG04_a - Ancient Types.jpg", "One Piece - CH0998PG04_b - Ancient Types.jpg", "One Piece - CH0998PG05_a - Ancient Types.jpg", "One Piece - CH0998PG05_b - Ancient Types.jpg", "One Piece - CH0998PG06 - Ancient Types.jpg", "One Piece - CH0998PG07 - Ancient Types.jpg", "One Piece - CH0998PG08_a - Ancient Types.jpg", "One Piece - CH0998PG08_b - Ancient Types.jpg", "One Piece - CH0998PG09_a - Ancient Types.jpg", "One Piece - CH0998PG09_b - Ancient Types.jpg", "One Piece - CH0998PG10_a - Ancient Types.jpg", "One Piece - CH0998PG10_b - Ancient Types.jpg", "One Piece - CH0998PG11_a - Ancient Types.jpg", "One Piece - CH0998PG11_b - Ancient Types.jpg"]
        result = sorted([f for f in os.listdir(dest) if not f.startswith('.')])
        self.assertEqual(result, expected_result)
        try:
            shutil.rmtree(dest)
        except:
            pass

    def test_check_spread(self):
        src = "./tests/data/test_epub/check_spread/src/"
        dest = "./tests/data/test_epub/check_spread/dest/"
        shutil.copytree(src,dest)
        epub_gen.check_spread(dest)
        result = sorted([f for f in os.listdir(dest) if not f.startswith('.')])
        expected_result = ['One Piece - CH0995PG01 - IGNORE check_spread starts on index 1.jpg', 'One Piece - CH0996PG01 - Island of the Strongest.jpg', 'One Piece - CH0996PG02 - Island of the Strongest.jpg', 'One Piece - CH0996PG03 - Island of the Strongest.jpg', 'One Piece - CH0996PG04 - Island of the Strongest.jpg', 'One Piece - CH0996PG05 - Island of the Strongest.jpg', 'One Piece - CH0996PG06 - Island of the Strongest.jpg', 'One Piece - CH0996PG07 - Island of the Strongest.jpg', 'One Piece - CH0996PG08 - Island of the Strongest.jpg', 'One Piece - CH0996PG09 - Island of the Strongest.jpg', 'One Piece - CH0996PG10 - Island of the Strongest.jpg', 'One Piece - CH0996PG11 - Island of the Strongest.jpg', 'One Piece - CH0996PG12 - Island of the Strongest.jpg', 'One Piece - CH0996PG13 - Island of the Strongest.jpg', 'One Piece - CH0996PG14 - Island of the Strongest.jpg', 'One Piece - CH0996PG15 - Island of the Strongest.jpg', 'One Piece - CH0996PG16 - Island of the Strongest.jpg', 'One Piece - CH0996PG17 - Island of the Strongest.jpg','One Piece - CH0997PG00 - Flames.jpg', 'One Piece - CH0997PG01 - Flames.jpg', 'One Piece - CH0997PG02 - Flames.jpg', 'One Piece - CH0997PG03 - Flames.jpg', 'One Piece - CH0997PG04 - Flames.jpg', 'One Piece - CH0997PG05 - Flames.jpg', 'One Piece - CH0997PG06 - Flames.jpg', 'One Piece - CH0997PG07 - Flames.jpg', 'One Piece - CH0997PG08 - Flames.jpg', 'One Piece - CH0997PG09 - Flames.jpg', 'One Piece - CH0997PG10 - Flames.jpg', 'One Piece - CH0997PG11 - Flames.jpg', 'One Piece - CH0997PG12 - Flames.jpg', 'One Piece - CH0997PG13 - Flames.jpg', 'One Piece - CH0997PG14 - Flames.jpg', 'One Piece - CH0997PG15 - Flames.jpg', 'One Piece - CH0997PG16_a - Flames.jpg', 'One Piece - CH0997PG16_b - Flames.jpg', 'One Piece - CH1006PG01_a - The Honorable Hyogoro The Flower.jpeg', 'One Piece - CH1006PG01_b - The Honorable Hyogoro The Flower.jpeg', 'One Piece - CH1006PG02 - The Honorable Hyogoro The Flower.png', 'One Piece - CH1006PG03 - The Honorable Hyogoro The Flower.png', 'One Piece - CH1006PG04 - The Honorable Hyogoro The Flower.png', 'One Piece - CH1006PG05 - The Honorable Hyogoro The Flower.png', 'One Piece - CH1006PG06 - The Honorable Hyogoro The Flower.png', 'One Piece - CH1006PG07 - The Honorable Hyogoro The Flower.png', 'One Piece - CH1006PG08 - The Honorable Hyogoro The Flower.png', 'One Piece - CH1006PG09 - The Honorable Hyogoro The Flower.png', 'One Piece - CH1006PG10 - The Honorable Hyogoro The Flower.png', 'One Piece - CH1006PG11 - The Honorable Hyogoro The Flower.png', 'One Piece - CH1006PG12 - The Honorable Hyogoro The Flower.png', 'One Piece - CH1006PG13 - The Honorable Hyogoro The Flower.png', 'One Piece - CH1006PG14 - The Honorable Hyogoro The Flower.jpeg', 'One Piece - CH1006PG15 - The Honorable Hyogoro The Flower.png', 'One Piece - CH1006PG16 - The Honorable Hyogoro The Flower.png', 'One Piece - CH1006PG17 - The Honorable Hyogoro The Flower.jpeg']
        self.assertEqual(result, expected_result)
        try:
            shutil.rmtree(dest)
        except:
            pass

    def test_generate_manifest_image(self):
        page_id = "CH555PG02"
        image = "CH555PG02.jpg"
        media_type = "jpeg"
        result = epub_gen.generate_manifest_image(page_id, image, media_type)
        expected_result = """<item id="CH555PG02_img" href="images/CH555PG02.jpg" media-type="image/jpeg"/>"""
        self.assertEqual(result, expected_result)
    
    def test_generate_manifest_xhtml(self):
        page_id = "CH555PG02"
        result = epub_gen.generate_manifest_xhtml(page_id)
        expected_result = """<item id="CH555PG02" href="xhtml/CH555PG02.xhtml" media-type="application/xhtml+xml"/>"""
        self.assertEqual(result, expected_result)

    def test_generate_spine(self):
        page_id = "CH555PG02"
        spread = "right"
        result = epub_gen.generate_spine(page_id, spread)
        expected_result = """<itemref idref="CH555PG02" linear="yes" properties="rendition:page-spread-right"/>"""
        self.assertEqual(result, expected_result)

    def test_generate_toc(self):
        page_id = "CH0555PG01"
        title = "Chapter Title.jpg"
        result = epub_gen.generate_toc(page_id, title)
        expected_result = """<li><a href="xhtml/CH0555PG01.xhtml">Chapter 555: Chapter Title</a></li>"""
        self.assertEqual(result, expected_result)

        page_id = "CH0555PG02"
        title = "Chapter Title.jpg"
        result = epub_gen.generate_toc(page_id, title)
        expected_result = ""
        self.assertEqual(result, expected_result)

    def test_mediatype(self):
        ext = ".png"
        result = epub_gen.get_mediatype(ext)
        expected_result = "png"
        self.assertEqual(result, expected_result)

        ext = ".jpg"
        result = epub_gen.get_mediatype(ext)
        expected_result = "jpeg"
        self.assertEqual(result, expected_result)

        ext = ".jpeg"
        result = epub_gen.get_mediatype(ext)
        expected_result = "jpeg"
        self.assertEqual(result, expected_result)

        ext = ".gif"
        result = epub_gen.get_mediatype(ext)
        expected_result = ".gif"
        self.assertEqual(result, expected_result)

    def test_next_page_spread(self):
        spread = "left"
        result = epub_gen.next_page_spread(spread)
        expected_result = "right"
        self.assertEqual(result, expected_result)
    
        spread = "right"
        result = epub_gen.next_page_spread(spread)
        expected_result = "left"
        self.assertEqual(result, expected_result)

        spread = "neither"
        result = epub_gen.next_page_spread(spread)
        expected_result = "left"
        self.assertEqual(result, expected_result)
