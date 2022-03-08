# manga_check.py
import os

from . import manga_config as mc
from . import manga_error as me
from . import manga_sql as msql
from . import Files


def check_manga_config():
    if(os.path.isdir(mc.MANGA_PATH) == False):
        me.error_write("[" + mc.MANGA_PATH + "] NOT FOUND")
        return False
    if(os.path.isdir(mc.SOURCE_PATH) == False):
        me.error_write("[" + mc.SOURCE_PATH + "] NOT FOUND")
        return False
    if(os.path.isdir(mc.DESTINATION_PATH) == False):
        me.error_write("[" + mc.DESTINATION_PATH + "] NOT FOUND")
        return False
    if(os.path.isfile(mc.DB_FILE_PATH) == False):
        me.error_write("[" + mc.DB_FILE_PATH + "] NOT FOUND")
        return False
    if(os.path.isdir(mc.ERROR_PATH) == False):
        me.error_write("[" + mc.ERROR_PATH + "] NOT FOUND")
        return False
    if(os.path.isdir(mc.MANGA_PATH + "One Piece" + mc.OP_COVER_SUBPATH) == False):
        me.error_write("[" + mc.MANGA_PATH + "One Piece" + mc.OP_COVER_SUBPATH + "] NOT FOUND")
        return False
    return True

def check_auto_chapter(manga, chapter_title):
    if(manga == "" or chapter_title == ""):
        me.error_write("BAD AUTO CHAPTER ENTRY")
        return False
    # Check Source
    source = Files(mc.SOURCE_PATH)
    if(source.count == 0):
        me.error_write("INVALID SOURCE: SOURCE IS EMPTY")
        return False
    for page in range(0, source.count):
        if not (source.isfile(page)):
            me.error_write("INVALID SOURCE: SOMETHING ISN'T A FILE")
            return False
        if(source.ext(page) == -1):
            me.error_write("INVALID SOURCE: FILE HAS NO EXTENSION")
            return False
    # Check db
    if(msql.check_auto_chapter_sql(manga) == False):
        return False
    return True

def check_auto_volume(manga, last_chapter_of_new_volume, volume_title):
    if(manga == "" or last_chapter_of_new_volume == "" or volume_title == ""):
        me.error_write("BAD AUTO VOLUME ENTRY")
        return False
    # Check Source
    source = Files(mc.SOURCE_PATH)
    if(source.count != 1):
        me.error_write("INVALID SOURCE: ONLY NEED 1 FILE")
        return False
    if not (source.isfile()):
        me.error_write("INVALID SOURCE: SOMETHING ISN'T A FILE")
        return False
    if(source.ext() == -1):
        me.error_write("INVALID SOURCE: FILE HAS NO EXTENSION")
        return False
    # Check db
    if(msql.check_auto_volume_sql(manga, last_chapter_of_new_volume) == False):
        return False
    return True

def check_manual_single_chapter(manga, chapter_numer, chapter_title):
    if(manga == "" or chapter_numer == "" or chapter_title == ""):
        me.error_write("BAD MANUAL SINGLE CHAPTER ENTRY")
        return False
    # Check Source
    source = Files(mc.SOURCE_PATH)
    if(source.count == 0):
        me.error_write("INVALID SOURCE: SOURCE IS EMPTY")
        return False
    for page in range(0, source.count):
        if not (source.isfile(page)):
            me.error_write("INVALID SOURCE: SOMETHING ISN'T A FILE")
            return False
        if(source.ext(page) == -1):
            me.error_write("INVALID SOURCE: FILE HAS NO EXTENSION")
            return False
    # Check Destination
    dest_path = Files(mc.DESTINATION_PATH)
    if(dest_path.count != 0):
        me.error_write("INVALID DESTINATION: DESTINATION IS NOT EMPTY")
        return False
    return True

def check_manual_multiple_chapter(manga):
    if(manga == ""):
        me.error_write("BAD MANUAL MULTIPLE CHAPTER ENTRY")
        return False
    # Check Source
    source = Files(mc.SOURCE_PATH)
    if(source.count == 0):
        me.error_write("INVALID SOURCE: SOURCE IS EMPTY")
        return False
    for chapter in range(0, source.count):
        number_title = source.filenames[chapter].split(" - ")
        if(len(number_title) != 2):
            me.error_write("INVALID SOURCE: CHAPTER AND TITLE NOT PROVIDED CORRECTLY")
            return False
        source_chapter = Files(source.path + source.filenames[chapter] + "/")
        # Check too make sure it's a directory
        if not (source_chapter.isdir()):
            me.error_write("INVALID SOURCE: SOURCE IS NOT ALL DIRECTORIES")
            return False
        # Make Sure it's not empty
        if(source_chapter.count == 0):
            me.error_write("INVALID SOURCE: ONE CHAPTER IS EMPTY")
            return False
        # Check to make sure all files inside
        for page in range(0, source_chapter.count):
            if not (source_chapter.isfile(page)):
                me.error_write("INVALID SOURCE: ONE CHAPTER IS INVALID")
                return False
            if(source_chapter.ext(page) == -1):
                me.error_write("INVALID SOURCE: ONE CHAPTER IS MISSING AN EXTENSION")
                return False
    # Check Destination
    dest_path = Files(mc.DESTINATION_PATH)
    if(dest_path.count != 0):
        me.error_write("INVALID DESTINATION: DESTINATION IS NOT EMPTY")
        return False
    return True

def check_manual_volume(manga, volume_number, volume_title):
    if(volume_number == "" or volume_title == ""):
        me.error_write("BAD MANUAL VOLUME ENTRY")
        return False
    if(check_manual_multiple_chapter(manga) == False):
        return False
    return True
