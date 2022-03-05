#test_Directory.py
import unittest
import sys

sys.path.append("..")
from src.manga import Directory


class TestDirectory(unittest.TestCase):

    def test_Directory(self):
        dir_1 = Directory("/path/to/a/directory/")
        self.assertEqual(dir_1.path, "/path/to/a/directory/")
        dir_1.path = "/new/path/to/new/directory"
        self.assertEqual(dir_1.path, "/new/path/to/new/directory")

    def test_isdir(self):
        dir_1 = Directory("./tests/data/")
        dir_2 = Directory("./tests/data/test_Directory")
        dir_3 = Directory("./tests/test_Directory.py")
        self.assertEqual(dir_1.isdir(), True)
        self.assertEqual(dir_2.isdir(), True)
        self.assertEqual(dir_3.isdir(), False)
        dir_3.path = "."
        self.assertEqual(dir_3.isdir(), True)

    def test_list_dir(self):
        dir_1 = Directory("./tests/data/test_Directory/dir_1")
        dir_2 = Directory("./tests/data/test_Directory/dir_2")
        dir_3 = Directory("./tests/data/test_Directory/dir_3")
        dir_4 = Directory("./tests/data/test_Directory/dir_4")
        dir_1_items = ["dir_1_1", "file_1.jpg"]
        dir_2_items = []
        self.assertEqual(dir_1.list_dir(), dir_1_items)
        self.assertEqual(dir_2.list_dir(), dir_2_items)
        self.assertEqual(dir_3.list_dir(), False)
        self.assertEqual(dir_4.list_dir(), False)

    def test_num_files(self):
        dir_1 = Directory("./tests/data/test_Directory/dir_1")
        dir_2 = Directory("./tests/data/test_Directory/dir_2")
        dir_3 = Directory("./tests/data/test_Directory/dir_3")
        dir_4 = Directory("./tests/data/test_Directory/dir_4")
        dir_1_files = 2
        dir_2_files = 0
        self.assertEqual(dir_1.num_files(), dir_1_files)
        self.assertEqual(dir_2.num_files(), dir_2_files)
        self.assertEqual(dir_3.num_files(), -1)
        self.assertEqual(dir_4.num_files(), -1)

    def test_rm_dir(self):
        dir_1 = Directory("./tests/data/test_Directory/dir_1")
        dir_3 = Directory("./tests/data/test_Directory/dir_3")
        dir_4 = Directory("./tests/data/test_Directory/dir_4")
        dir_5 = Directory("./tests/data/test_Directory/dir_5")
        dir_5.mk_dir()
        self.assertEqual(dir_1.rm_dir(), False)
        self.assertEqual(dir_3.rm_dir(), False)
        self.assertEqual(dir_4.rm_dir(), False)
        self.assertEqual(dir_5.rm_dir(), True)

    def test_mk_dir(self):
        dir_1 = Directory("./tests/data/test_Directory/dir_1")
        dir_2 = Directory("./tests/data/test_Directory/dir_2")
        dir_3 = Directory("./tests/data/test_Directory/dir_3")
        dir_6 = Directory("./tests/data/test_Directory/dir_6")
        self.assertEqual(dir_1.mk_dir(), False)
        self.assertEqual(dir_2.mk_dir(), True)
        self.assertEqual(dir_3.mk_dir(), False)
        self.assertEqual(dir_6.isdir(), False)
        self.assertEqual(dir_6.mk_dir(), True)
        dir_6.rm_dir()


if __name__ == '__main__':
    unittest.main()
