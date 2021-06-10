# test_Files.py
import unittest
import shutil
import os
# from ..src.manga import Files
# from ..src.manga import manga_config
import src.manga.Files as Files
import src.manga.manga_config as manga_config


class TestFiles(unittest.TestCase):

    def test_Files(self):
        Files01 = Files("./tests/data/test_Files/Files/Files01")
        Files02 = Files("./tests/data/test_Files/Files/Files02")
        Files03 = Files("./tests/data/test_Files/Files/Files03")
        Files04 = Files("./tests/data/test_Files/Files/Files04")
        list01 = ["file01.jpg", "file02.jpg", "file03.jpg"]
        list02 = []
        list03 = ["file01.jpg", "file02.jpg", "path01", "path02"]
        list04 = ["path01", "path02", "path03"]
        self.assertEqual(Files01.path, "./tests/data/test_Files/Files/Files01")
        self.assertEqual(Files02.path, "./tests/data/test_Files/Files/Files02")
        self.assertEqual(Files03.path, "./tests/data/test_Files/Files/Files03")
        self.assertEqual(Files04.path, "./tests/data/test_Files/Files/Files04")
        self.assertEqual(Files01.filenames, list01)
        self.assertEqual(Files02.filenames, list02)
        self.assertEqual(Files03.filenames, list03)
        self.assertEqual(Files04.filenames, list04)
        self.assertEqual(Files01.count, 3)
        self.assertEqual(Files02.count, 0)
        self.assertEqual(Files03.count, 4)
        self.assertEqual(Files04.count, 3)
        self.assertEqual(Files01.filenames[1], list01[1])
        self.assertEqual(Files03.filenames[3], list03[3])
        self.assertEqual(Files04.filenames[2], list04[2])

    def test_isfile(self):
        file_obj = Files("./tests/data/test_Files/isfile/")
        self.assertEqual(file_obj.isfile(), True)
        self.assertEqual(file_obj.isfile(1), False)
            
    def test_ext(self):
        file_obj = Files("./tests/data/test_Files/ext/")
        self.assertEqual(file_obj.ext(), ".txt")
        self.assertEqual(file_obj.ext(1), ".txt")
        self.assertEqual(file_obj.ext(2), -1)
        self.assertEqual(file_obj.ext(3), -1)

    def test_pad_zero(self):
        src01 = "./tests/data/test_Files/pad_zero/src/test01/"
        src02 = "./tests/data/test_Files/pad_zero/src/test02/"
        src03 = "./tests/data/test_Files/pad_zero/src/test03/"
        dest01 = "./tests/data/test_Files/pad_zero/dest/test01/"
        dest02 = "./tests/data/test_Files/pad_zero/dest/test02/"
        dest03 = "./tests/data/test_Files/pad_zero/dest/test03/"
        dest04 = "./tests/data/test_Files/pad_zero/dest/test04/"
        try:
            shutil.copytree(src01, dest01)
            shutil.copytree(src02, dest02)
            shutil.copytree(src03, dest03)
            shutil.copytree(src01, dest04)
        except:
            pass
        test01 = Files(dest01)
        test02 = Files(dest02)
        test03 = Files(dest03)
        test01_preview = Files(dest01)
        before_list01 = ['004.jpg', '004page.jpg', '02.jpg', '02page.jpg', '1.jpg', '1page.jpg', '33.jpg', '33page.jpg', 'hey02.jpg', 'hey1.jpg', 'hey33.jpg', 'page02here.jpg', 'page1here.jpg', 'page33here.jpg']
        after_list01 = ['004.jpg', '004page.jpg', '01.jpg', '01page.jpg', '02.jpg', '02page.jpg', '33.jpg', '33page.jpg', 'hey01.jpg', 'hey02.jpg', 'hey33.jpg', 'page01here.jpg', 'page02here.jpg', 'page33here.jpg']
        before_list02 = ['1.jpg', '10.jpg', '11.jpg', '12.jpg', '13.jpg', '14.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg', '6.jpg', '7.jpg', '8.jpg', '9.jpg']
        after_list02 = ['01.jpg', '02.jpg', '03.jpg', '04.jpg', '05.jpg', '06.jpg', '07.jpg', '08.jpg', '09.jpg', '10.jpg', '11.jpg', '12.jpg', '13.jpg', '14.jpg']
        before_list03 = ['0.jpg', '01.jpg', '02.jpg', '03.jpg', '04.jpg', '05.jpg', '06.jpg', '07.jpg', '08.jpg', '09.jpg', '10.jpg', '11.jpg', '12.jpg', '13.jpg']
        after_list03 = ['00.jpg', '01.jpg', '02.jpg', '03.jpg', '04.jpg', '05.jpg', '06.jpg', '07.jpg', '08.jpg', '09.jpg', '10.jpg', '11.jpg', '12.jpg', '13.jpg']
        self.assertEqual(test01.list_dir(), before_list01)
        self.assertEqual(test02.list_dir(), before_list02)
        self.assertEqual(test03.list_dir(), before_list03)
        test01_preview.pad_zero("Preview")
        self.assertEqual(test01_preview.list_dir(), before_list01)
        test01.pad_zero()
        test02.pad_zero()
        test03.pad_zero()
        self.assertEqual(test01.list_dir(), after_list01)
        self.assertEqual(test02.list_dir(), after_list02)
        self.assertEqual(test03.list_dir(), after_list03)

        try:
            shutil.rmtree(dest01)
            shutil.rmtree(dest02)
            shutil.rmtree(dest03)
            shutil.rmtree(dest04)
        except:
            pass

    def test_copyfile(self):
        working_src = "./tests/data/test_Files/copyfile/src/working/" #Working copy
        fileexist_src = "./tests/data/test_Files/copyfile/src/fileexist/" #File Existst already
        destpath_src = "./tests/data/test_Files/copyfile/src/destpath/" #Dest filename is a path
        working_dest = "./tests/data/test_Files/copyfile/dest/working/" #Working copy
        fileexist_dest = "./tests/data/test_Files/copyfile/dest/fileexist/" #File Existst already
        destpath = "./tests/data/test_Files/copyfile/dest/destpath/"
        destnotfound = "./tests/data/test_Files/copyfile/dest/test04/" #dest path not found
        try:
            os.mkdir(working_dest) #Working copy
            shutil.copytree(fileexist_src, fileexist_dest)
            os.mkdir(destpath)
        except:
            pass
        working_test = Files(working_src)
        fileexist_test = Files(fileexist_src)
        destpath_src = Files(destpath_src)
        self.assertEqual(working_test.copyfile(working_dest, working_test.filenames[0]), True) #Working copy
        self.assertEqual(fileexist_test.copyfile(fileexist_dest, fileexist_test.filenames[0]), False) #File Existst already
        self.assertEqual(destpath_src.copyfile(destpath, destpath_src.filenames), False) # Dest filename is path
        self.assertEqual(working_test.copyfile(destnotfound, working_test.filenames), False)
        shutil.rmtree(working_dest)
        shutil.rmtree(fileexist_dest)
        shutil.rmtree(destpath)

    def test_rename(self):
        og01 = "./tests/data/test_Files/rename/original/test01/"
        og02 = "./tests/data/test_Files/rename/original/test02/"
        og03 = "./tests/data/test_Files/rename/original/test03/"
        og04 = "./tests/data/test_Files/rename/original/test04/"
        src01 = "./tests/data/test_Files/rename/src/test01/"
        src02 = "./tests/data/test_Files/rename/src/test02/"
        src03 = "./tests/data/test_Files/rename/src/test03/"
        src04 = "./tests/data/test_Files/rename/src/test04/"
        dest01 = "./tests/data/test_Files/rename/dest/test01/"
        dest02 = "./tests/data/test_Files/rename/dest/test02/"
        dest03 = "./tests/data/test_Files/rename/dest/test03/"
        dest04 = "./tests/data/test_Files/rename/dest/test04/"
        shutil.copytree(og01, src01)
        shutil.copytree(og02, src02)
        shutil.copytree(og03, src03)
        shutil.copytree(og04, src04)
        os.mkdir(dest01)
        os.mkdir(dest03)
        shutil.copytree(og02, dest02)
        os.mkdir(dest04)
        test01 = Files(src01)
        test02 = Files(src02)
        test03 = Files(src03)
        test04 = Files(src04)
        dest01_filenames = ['Blue Box - CH001PG01 - Chinatsu Senpai.jpg', 'Blue Box - CH001PG02 - Chinatsu Senpai.jpg', 'Blue Box - CH001PG03 - Chinatsu Senpai.jpg', 'Blue Box - CH001PG04 - Chinatsu Senpai.jpg', 'Blue Box - CH001PG05 - Chinatsu Senpai.jpg', 'Blue Box - CH001PG06 - Chinatsu Senpai.jpg', 'Blue Box - CH001PG07 - Chinatsu Senpai.jpg', 'Blue Box - CH001PG08 - Chinatsu Senpai.jpg', 'Blue Box - CH001PG09 - Chinatsu Senpai.jpg', 'Blue Box - CH001PG10 - Chinatsu Senpai.jpg', 'Blue Box - CH001PG11 - Chinatsu Senpai.jpg', 'Blue Box - CH001PG12 - Chinatsu Senpai.jpg', 'Blue Box - CH001PG13 - Chinatsu Senpai.jpg', 'Blue Box - CH001PG14 - Chinatsu Senpai.jpg']
        for i in range(0,test01.num_files()):
            test01.rename(dest01, dest01_filenames[i], i)
        self.assertEqual(sorted(os.listdir(dest01)), dest01_filenames) #workds
        self.assertEqual(test02.rename(dest02, "01.jpg"), False) #dest already exists
        self.assertEqual(test03.rename(dest03, "01.jpg"), False) #no source
        self.assertEqual(test04.rename(dest04, "02.jpg"), True) #working rename
        #try to rename when it's already gone
        self.assertEqual(test04.rename(dest04, "02.jpg"), False) #try rename again
        
        shutil.rmtree(src01)
        shutil.rmtree(src02)
        shutil.rmtree(src03)
        shutil.rmtree(src04)
        shutil.rmtree(dest01)
        shutil.rmtree(dest02)
        shutil.rmtree(dest03)
        shutil.rmtree(dest04)

if __name__ == '__main__':
    unittest.main()
