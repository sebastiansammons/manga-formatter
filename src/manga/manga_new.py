# manga_new.py
from . import manga_config as mc
from . import manga_sql as msql
from . import manga_error as me
from . import manga_check
from . import manga_format
from . import Directory
from . import Files


def add_new_manga(manga, writer, illustrator, completed):
    new_manga_sql_entry(manga, writer, illustrator, completed)
    new_manga_directory = mc.MANGA_PATH + manga + "/"
    create_new_manga_directory(new_manga_directory)
    new_manga_volume_directory = new_manga_directory + mc.VOLUMES_SUBPATH
    manga_src = Files(mc.SOURCE_PATH)
    for volume in range(0, manga_src.count):
        volume_info = manga_src.filenames[volume].split(" - ")
        current_volume_number = int(volume_info[0])
        if(len(volume_info) == 2):
            current_volume_title = volume_info[1]
        else:
            current_volume_title = ""
        volume_src = Directory(mc.SOURCE_PATH + manga_src.filenames[volume] + "/")
        manga_format.manual_volume_format(volume_src.path, mc.DESTINATION_PATH, manga, current_volume_number, current_volume_title)
        move_temp_to_volume(mc.DESTINATION_PATH, new_manga_volume_directory)
        volume_src.rm_dir()
    if(completed == True):
        manga_chapters_pages = Directory(new_manga_directory + mc.NEW_CHAPTERS_SUBPATH)
        manga_chapters_pages.rm_dir()

def create_new_manga_directory(new_manga_directory):
    manga_directory = Directory(new_manga_directory)
    manga_directory.mk_dir()
    chapter_pages = Directory(new_manga_directory + "Chapter Pages/")
    chapter_pages.mk_dir()
    new_chapters = Directory(new_manga_directory + mc.NEW_CHAPTERS_SUBPATH)
    new_chapters.mk_dir()
    volume_pages_directory = Directory(new_manga_directory + mc.VOLUMES_SUBPATH)
    volume_pages_directory.mk_dir()
    volume_directory = Directory(new_manga_directory + mc.EPUB_VOLUMES_SUBPATH)
    volume_directory.mk_dir()
    del manga_directory, chapter_pages, new_chapters, volume_pages_directory, volume_directory

def new_manga_check(manga, writer, illustrator):
    if(manga == "" or writer == "" or illustrator == ""):
        me.error_write("BAD NEW MANGA ENTRY")
        return False
    manga_src = Files(mc.SOURCE_PATH)
    for volume in range(0, manga_src.count):
        volume_dir = mc.SOURCE_PATH + manga_src.filenames[volume] + "/"
        volume_info = manga_src.filenames[volume].split(" - ")
        current_volume_number = int(volume_info[0])
        result = manga_check.check_manual_volume(volume_dir, mc.DESTINATION_PATH, manga, current_volume_number)
        if(result == False):
            return False
    return True

def new_manga_sql_entry(manga, writer, illustrator, completed):
    msql.new_manga(manga, writer, illustrator, completed)
    current_chapter_number = 0
    current_chapter_title = ""
    current_volume_number = 0
    current_volume_title = ""
    last_chapter_of_volume = 1
    manga_src = Files(mc.SOURCE_PATH)
    for volume in range(0, manga_src.count):
        # Go through chapters, update each to sql
        volume_dir = mc.SOURCE_PATH +  manga_src.filenames[volume] + "/"
        current_volume = Files(volume_dir)
        for chapter in range(0, current_volume.count):
            if(current_volume.isfile(chapter)):
                pass
            else:
                chapter_info = current_volume.filenames[chapter].split(" - ")
                current_chapter_number = int(chapter_info[0])
                last_chapter_of_volume = current_chapter_number
                if(len(chapter_info) == 2):
                    current_chapter_title = chapter_info[1]
                else:
                    current_chapter_title = ""
                msql.update_new_chapter(manga, current_chapter_number, current_chapter_title)
        # All chapters in volume updated, update volume to sql
        volume_info = manga_src.filenames[volume].split(" - ")
        current_volume_number = int(volume_info[0])
        if(len(volume_info) == 2):
            current_volume_title = volume_info[1]
        else:
            current_volume_title = ""
        msql.update_new_volume(manga, current_volume_number, last_chapter_of_volume, current_volume_title)

def move_temp_to_volume(temp_dir, volume_dir):
    temp = Files(temp_dir)
    temp_volume = Files(temp.path + "/" + temp.filenames[0])
    volume_dest = Directory(volume_dir + "/" + temp.filenames[0])
    volume_dest.mk_dir()
    for page in range(0, temp_volume.count):
        temp_volume.rename(volume_dest.path, temp_volume.filenames[page], page)
    temp_volume.rm_dir()
