# manga_check.py
import os
import shutil
import logging
from . import manga_config as mc
from . import manga_error as me
from . import Files
from . import SQLite

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s|%(funcName)-30s|%(levelname)-7s|%(message)s')
file_handler = logging.FileHandler(mc.LOGS_PATH + "manga.log")
shutil.chown(mc.LOGS_PATH + "manga.log", user = int(os.getenv("PUID")), group = int(os.getenv("PGID")))
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.WARNING)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

def check_manga_config():
    if(os.path.isdir(mc.MANGA_PATH) == False):
        logger.error("[" + mc.MANGA_PATH + "] NOT FOUND")
        me.error_write("[" + mc.MANGA_PATH + "] NOT FOUND")
        return False
    if(os.path.isdir(mc.SOURCE_PATH) == False):
        logger.error("[" + mc.SOURCE_PATH + "] NOT FOUND")
        me.error_write("[" + mc.SOURCE_PATH + "] NOT FOUND")
        return False
    if(os.path.isdir(mc.DESTINATION_PATH) == False):
        logger.error("[" + mc.DESTINATION_PATH + "] NOT FOUND")
        me.error_write("[" + mc.DESTINATION_PATH + "] NOT FOUND")
        return False
    if(os.path.isfile(mc.DB_FILE_PATH) == False):
        logger.error("[" + mc.DB_FILE_PATH + "] NOT FOUND")
        me.error_write("[" + mc.DB_FILE_PATH + "] NOT FOUND")
        return False
    if(os.path.isdir(mc.LOGS_PATH) == False):
        logger.error("[" + mc.LOGS_PATH + "] NOT FOUND")
        me.error_write("[" + mc.LOGS_PATH + "] NOT FOUND")
        return False
    if(os.path.isdir(mc.MANGA_PATH + "One Piece" + mc.OP_COVER_SUBPATH) == False):
        logger.error("[" + mc.MANGA_PATH + "One Piece" + mc.OP_COVER_SUBPATH + "] NOT FOUND")
        me.error_write("[" + mc.MANGA_PATH + "One Piece" + mc.OP_COVER_SUBPATH + "] NOT FOUND")
        return False
    return True

def check_auto_chapter(manga, chapter_title):
    if(manga == "" or chapter_title == ""):
        logger.warning("BAD AUTO CHAPTER ENTRY")
        me.error_write("BAD AUTO CHAPTER ENTRY")
        return False
    #Check Source
    source = Files(mc.SOURCE_PATH)
    if(source.count == 0):
        logger.warning("INVALID SOURCE: SOURCE IS EMPTY")
        me.error_write("INVALID SOURCE: SOURCE IS EMPTY")
        return False
    for page in range(0, source.count):
        if not (source.isfile(page)):
            logger.warning("INVALID SOURCE: SOMETHING ISN'T A FILE")
            me.error_write("INVALID SOURCE: SOMETHING ISN'T A FILE")
            return False
        if(source.ext(page) == -1):
            logger.warning("INVALID SOURCE: FILE HAS NO EXTENSION")
            me.error_write("INVALID SOURCE: FILE HAS NO EXTENSION")
            return False
    #Check db
    manga_db = SQLite(mc.DB_FILE_PATH)
    query_input = (manga, )
    query_output = manga_db.execute("SELECT manga FROM manga_progress WHERE manga = ?", query_input)
    if(query_output == [] or query_output == False):
        logger.error("INVALID DB: " + manga + " ISN'T IN THE manga_progress TABLE")
        me.error_write("INVALID DB: " + manga + " ISN'T IN THE manga_progress TABLE")
        return False
    query_output = manga_db.execute("SELECT manga FROM " + manga.replace(' ', '_') + "_chapter;")
    if(query_output == [] or query_output == False):
        logger.error("INVALID DB: " + manga.replace(' ', '_') + "_chapter TABLE DOESN'T EXIST")
        me.error_write("INVALID DB: " + manga.replace(' ', '_') + "_chapter TABLE DOESN'T EXIST")
        return False
    return True

def check_auto_volume(manga, last_chapter_of_new_volume, volume_title):
    if(manga == "" or last_chapter_of_new_volume == "" or volume_title == ""):
        logger.warning("BAD AUTO VOLUME ENTRY")
        me.error_write("BAD AUTO VOLUME ENTRY")
        return False
    #Check Source
    source = Files(mc.SOURCE_PATH)
    if(source.count != 1):
        logger.warning("INVALID SOURCE: ONLY NEED 1 FILE")
        me.error_write("INVALID SOURCE: ONLY NEED 1 FILE")
        return False
    if not (source.isfile()):
        logger.warning("INVALID SOURCE: SOMETHING ISN'T A FILE")
        me.error_write("INVALID SOURCE: SOMETHING ISN'T A FILE")
        return False
    if(source.ext() == -1):
        logger.warning("INVALID SOURCE: FILE HAS NO EXTENSION")
        me.error_write("INVALID SOURCE: FILE HAS NO EXTENSION")
        return False
    #check db
    manga_db = SQLite(mc.DB_FILE_PATH)
    query_input = (manga, )
    query_output = manga_db.execute("SELECT manga FROM manga_progress WHERE manga = ?", query_input)
    if(query_output == [] or query_output == False):
        logger.error("INVALID DB: " + manga + " ISN'T IN THE manga_progress TABLE")
        me.error_write("INVALID DB: " + manga + " ISN'T IN THE manga_progress TABLE")
        return False
    query_output = manga_db.execute("SELECT manga FROM " + manga.replace(' ', '_') + "_volume;")
    if(query_output == [] or query_output == False):
        logger.error("INVALID DB: " + manga.replace(' ', '_') + "_volume TABLE DOESN'T EXIST")
        me.error_write("INVALID DB: " + manga.replace(' ', '_') + "_volume TABLE DOESN'T EXIST")
        return False
    query_output = manga_db.execute("SELECT first_chapter_of_new_volume FROM manga_progress WHERE manga = ?", query_input)
    if(query_output[0] >= int(last_chapter_of_new_volume)):
        logger.warning("INVALID DB: LAST CHAPTER OF NEW VOLUME IS NOT GREATER THAN NEXT CHAPTER IN NEW VOLUME")
        me.error_write("INVALID DB: LAST CHAPTER OF NEW VOLUME IS NOT GREATER THAN NEXT CHAPTER IN NEW VOLUME")
        return False
    return True

def check_manual_single_chapter(manga, chapter_numer, chapter_title):
    if(manga == "" or chapter_numer == "" or chapter_title == ""):
        logger.warning("BAD MANUAL SINGLE CHAPTER ENTRY")
        me.error_write("BAD MANUAL SINGLE CHAPTER ENTRY")
        return False
    #Check Source
    source = Files(mc.SOURCE_PATH)
    if(source.count == 0):
        logger.warning("INVALID SOURCE: SOURCE IS EMPTY")
        me.error_write("INVALID SOURCE: SOURCE IS EMPTY")
        return False
    for page in range(0, source.count):
        if not (source.isfile(page)):
            logger.warning("INVALID SOURCE: SOMETHING ISN'T A FILE")
            me.error_write("INVALID SOURCE: SOMETHING ISN'T A FILE")
            return False
        if(source.ext(page) == -1):
            logger.warning("INVALID SOURCE: FILE HAS NO EXTENSION")
            me.error_write("INVALID SOURCE: FILE HAS NO EXTENSION")
            return False
    #Check Destination
    dest_path = Files(mc.DESTINATION_PATH)
    if(dest_path.count != 0):
        logger.warning("INVALID DESTINATION: DESTINATION IS NOT EMPTY")
        me.error_write("INVALID DESTINATION: DESTINATION IS NOT EMPTY")
        return False
    return True

def check_manual_multiple_chapter(manga):
    if(manga == ""):
        logger.warning("BAD MANUAL MULTIPLE CHAPTER ENTRY")
        me.error_write("BAD MANUAL MULTIPLE CHAPTER ENTRY")
        return False
    #Check Source
    source = Files(mc.SOURCE_PATH)
    if(source.count == 0):
        logger.warning("INVALID SOURCE: SOURCE IS EMPTY")
        me.error_write("INVALID SOURCE: SOURCE IS EMPTY")
        return False
    for chapter in range(0, source.count):
        number_title = source.filenames[chapter].split(" - ")
        if(len(number_title) != 2):
            logger.warning("INVALID SOURCE: CHAPTER AND TITLE NOT PROVIDED CORRECTLY")
            me.error_write("INVALID SOURCE: CHAPTER AND TITLE NOT PROVIDED CORRECTLY")
            return False
        source_chapter = Files(source.path + source.filenames[chapter] + "/")
        #Check too make sure it's a directory
        if not (source_chapter.isdir()):
            logger.warning("INVALID SOURCE: SOURCE IS NOT ALL DIRECTORIES")
            me.error_write("INVALID SOURCE: SOURCE IS NOT ALL DIRECTORIES")
            return False
        #Make Sure it's not empty
        if(source_chapter.count == 0):
            logger.warning("INVALID SOURCE: ONE CHAPTER IS EMPTY")
            me.error_write("INVALID SOURCE: ONE CHAPTER IS EMPTY")
            return False
        #Check to make sure all files inside
        for page in range(0, source_chapter.count):
            if not (source_chapter.isfile(page)):
                logger.warning("INVALID SOURCE: ONE CHAPTER IS INVALID")
                me.error_write("INVALID SOURCE: ONE CHAPTER IS INVALID")
                return False
            if(source_chapter.ext(page) == -1):
                logger.warning("INVALID SOURCE: ONE CHAPTER IS MISSING AN EXTENSION")
                me.error_write("INVALID SOURCE: ONE CHAPTER IS MISSING AN EXTENSION")
                return False
    #Check Destination
    dest_path = Files(mc.DESTINATION_PATH)
    if(dest_path.count != 0):
        logger.warning("INVALID DESTINATION: DESTINATION IS NOT EMPTY")
        me.error_write("INVALID DESTINATION: DESTINATION IS NOT EMPTY")
        return False
    return True

def check_manual_volume(manga, volume_number, volume_title):
    if(volume_number == "" or volume_title == ""):
        logger.warning("BAD MANUAL VOLUME ENTRY")
        me.error_write("BAD MANUAL VOLUME ENTRY")
        return False
    if(check_manual_multiple_chapter(manga) == False):
        return False
    return True
