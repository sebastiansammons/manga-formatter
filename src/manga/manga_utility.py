#manga_utility.py
import os
import shutil
import sqlite3
from . import manga_config
from . import manga_logging


def check_extension(src):
    manga_logging.log_debug("mangautility.check_extension(" + src + ")")
    if(src.find('.') == -1):
        manga_logging.log_error("[" + src + "] HAS NO EXTENSION")
        manga_logging.message_write("[" + src + "] HAS NO EXTENSION")
        return False
    return True

def check_manga_config():
    manga_logging.log_debug("mangautility.check_manga_config()")
    if(isdir(manga_config.MANGA_PATH) == False):
        manga_logging.log_error("[" + manga_config.MANGA_PATH + "] NOT FOUND")
        manga_logging.message_write("[" + manga_config.MANGA_PATH + "] NOT FOUND")
        return False
    if(isdir(manga_config.SOURCE_PATH) == False):
        manga_logging.log_error("[" + manga_config.SOURCE_PATH + "] NOT FOUND")
        manga_logging.message_write("[" + manga_config.SOURCE_PATH + "] NOT FOUND")
        return False
    if(isdir(manga_config.DESTINATION_PATH) == False):
        manga_logging.log_error("[" + manga_config.DESTINATION_PATH + "] NOT FOUND")
        manga_logging.message_write("[" + manga_config.DESTINATION_PATH + "] NOT FOUND")
        return False
    if(isfile(manga_config.DB_FILE_PATH) == False):
        manga_logging.log_error("[" + manga_config.DB_FILE_PATH + "] NOT FOUND")
        manga_logging.message_write("[" + manga_config.DB_FILE_PATH + "] NOT FOUND")
        return False
    if(isdir(manga_config.LOGS_PATH) == False):
        manga_logging.log_error("[" + manga_config.LOGS_PATH + "] NOT FOUND")
        manga_logging.message_write("[" + manga_config.LOGS_PATH + "] NOT FOUND")
        return False
    return True

def check_source(format_type):
    manga_logging.log_debug("mangautility.check_source(" + format_type + ")")
    source_count = 0
    source_list = listdir(manga_config.SOURCE_PATH)
    if(source_list == False):
        return False
    source_count = len(source_list)
    source_list = sorted(source_list)
    if(source_count == 0):
        #Empty SOURCE
        manga_logging.log_warning("[SOURCE] IS EMPTY")
        manga_logging.message_write("SOURCE IS EMPTY")
        return False
    elif(source_count == 1):
        #Only auto_volume allows 1 item in SOURCE. Cover file only
        if(format_type == "auto_volume"):
            if(isfile(manga_config.SOURCE_PATH + source_list[0]) == True):
                return True
            else:
                manga_logging.log_warning("[" + source_list[0] + "] ISN'T A COVER FILE")
                manga_logging.message_write("[" + source_list[0] + "] ISN'T A COVER FILE")
                return False
        else:
            manga_logging.log_warning("[SOURCE] HAS ONLY 1 PAGE")
            manga_logging.message_write("SOURCE HAS ONLY 1 PAGE")
            return False
    else:
        #More than 1 item
        if(format_type == "auto_volume"):
            manga_logging.log_warning("[SOURCE] HAS MORE THAN 1 PAGE FOR AUTO VOLUME FORMAT")
            manga_logging.message_write("SOURCE HAS MORE THAN 1 PAGE FOR AUTO VOLUME FORMAT")
            return False
        elif(format_type == "manual_multi_chapter"):
            for chapter in range(0, source_count):
                #Make sure they're all directories
                if(isdir(manga_config.SOURCE_PATH + source_list[chapter]) == True):
                    current_path = listdir(manga_config.SOURCE_PATH + source_list[chapter])
                    if(current_path == False):
                        return False
                    if(len(current_path) == 0):
                        #Empty
                        manga_logging.log_warning("[" + manga_config.SOURCE_PATH + source_list[chapter] + "] IS EMPTY")
                        manga_logging.message_write("[" + source_list[chapter] + "] IS EMPTY")
                        return False
                    current_path = sorted(current_path)
                    #Check that each directory name is a number
                    try:
                        int(source_list[chapter].lstrip('0'))
                    #Directory name isn't a number
                    except ValueError:
                        manga_logging.log_warning("[" + source_list[chapter] + "] ISN'T A VALID DIRECTORY NAME FOR MULTI CHAPTER RENAME")
                        manga_logging.message_write("[" + source_list[chapter] + "] ISN'T A VALID DIRECTORY NAME FOR MULTI CHAPTER RENAME")
                        return False
                #Isn't a directory
                else:
                    manga_logging.log_warning("[" + source_list[chapter] + "] ISN'T A DIRECTORY")
                    manga_logging.message_write("[" + source_list[chapter] + "] ISN'T A DIRECTORY")
                    return False
            return True
        elif(format_type == "manual_volume"):
            #manual_volume runs manual_multiple_chapters so we only have to check if the chapters are in numerical order for a volume
            for chapter in range(0,source_count):
                #Remove leading zeroes and re-sort before comparing number values
                source_list[chapter] = source_list[chapter].lstrip('0')
            source_list = sorted(source_list)
            #try: isn't needed for int() here b/c it ran previously for manual_multiple_chapters
            chapter_number = int(source_list[0].lstrip('0'))
            for chapter in range(1, source_count):
                if(chapter_number + 1 == int(source_list[chapter].lstrip('0'))):
                    chapter_number += 1
                else:
                    manga_logging.log_warning("CHAPTERS IN SOURCE ARE NOT IN ORDER FOR A VOLUME FORMAT")
                    manga_logging.message_write("CHAPTERS IN SOURCE ARE NOT IN ORDER FOR A VOLUME FORMAT")
                    return False
            return True
        else:
            for page in range(0, source_count):
                #Make sure they're all files
                if(isfile(manga_config.SOURCE_PATH + source_list[page]) == False):
                    manga_logging.log_warning("[" + source_list[page] + "] ISN'T A FILE")
                    manga_logging.message_write("[" + source_list[page] + "] ISN'T A FILE")
                    return False
        return True

def chown(path, PUID, PGID):
    manga_logging.log_debug("mangautility.chown(" + path + ", " + str(PUID) + ", " + str(PGID) + ")")
    if(isfile(path) or isdir(path)):
        shutil.chown(path, user = PUID, group = PGID)

def copyfile(src, dest):
    manga_logging.log_debug("mangautility.copyfile(" + src + ", " + dest + ")")
    if(isfile(dest) == True):
        manga_logging.log_warning("[" + dest + "] ALREADY EXISTS")
        manga_logging.message_write("[" + dest + "] ALREADY EXISTS")
        return False
    try:
        shutil.copyfile(src, dest)
        manga_logging.log_debug("shutil.copyfile(" + src + ", " + dest + ")")
        chown(dest, int(os.getenv("PUID")), int(os.getenv("PGID")))
    except FileNotFoundError:
        if(isfile(src) == False):
            manga_logging.log_error("[" + src + "] NOT FOUND")
            manga_logging.message_write("[" + src + "] NOT FOUND")
        elif(isfile(dest) == False):
            manga_logging.log_error("[" + dest + "] NOT FOUND")
            manga_logging.message_write("[" + dest + "] NOT FOUND")
        return False
    except PermissionError:
        manga_logging.log_error("[" + src + ", " + dest + "] PERMISSION ERROR")
        manga_logging.message_write("[" + src + ", " + dest + "] PERMISSION ERROR")
        return False

def get_extension(src):
    manga_logging.log_debug("mangautility.get_extension(" + src + ")")
    return src[src.rfind('.'):]

def get_preview_type():
    manga_logging.log_debug("get_preview_type()")
    if(os.getenv("PREVIEW_TYPE", "SIMPLE") == "SIMPLE"):
        return "SIMPLE"
    else:
        return "DETAILED"

def isdir(path):
    manga_logging.log_debug("mangautility.isdir(" + path + ")")
    return os.path.isdir(path)

def isfile(path):
    manga_logging.log_debug("mangautility.isfile(" + path + ")")
    return os.path.isfile(path)

def pad_zero(src):
    manga_logging.log_debug("mangautility.pad_zero(" + src + ")")
    if(src == ""):
        #Empty string
        manga_logging.log_warning("EMPTY STRING")
        manga_logging.message_write("EMPTY STRING")
        return False
    src_filename = src[src.rfind('/') + 1:]
    src_path = src[:src.rfind('/') + 1 ]
    #Make sure src is a file
    if(isfile(src) == False):
        manga_logging.log_warning("[" + src + "] ISN'T A FILE")
        manga_logging.message_write("[" + src + "] ISN'T A FILE")
        return False
    for page in range(0, len(src_filename)):
        if(src_filename[page].isnumeric()):
            #Number found
            if(page == 0):
                #Beginning of the filename
                if(src_filename[page + 1].isnumeric()):
                    #Number at beginning and next character, ignore
                    continue
                else:
                    #No number after first char, add a leading zero
                    dest = src_path + src_filename[:page] + "0" + src_filename[page:]
                    rename(src, dest)
                    return True
            elif(page + 1 >= len(src_filename)):
                #End of the filename
                #Only number found is at the end, add a leading zero
                dest = src_path + src_filename[:page] + "0" + src_filename[page:]
                rename(src, dest)
                return True
            else:
                #Middle of filename
                if(src_filename[page] != '0'):
                    if(src_filename[page + 1].isnumeric()):
                        #First number isn't 0, the next is also a number, so probably a 10, 20, etc. Ignore
                        continue
                    if(src_filename[page - 1].isnumeric()):
                        #There's a number before current char, ignore
                        continue
                    else:
                        #Number that isn't a 0, there is no number before or after, so a solo non 0 number, adding zero
                        dest = src_path + src_filename[:page] + "0" + src_filename[page:]
                        rename(src, dest)
                        return True
                else:
                    if(src_filename[page + 1].isnumeric() and src_filename[page + 1] != '0'):
                        #First number is zero, and next is also a non-zero number, already has leading zero
                        return True
    return True

def pad_zero_dir(path):
    manga_logging.log_debug("mangautility.pad_zero_dir(" + path + ")")
    path_list = listdir(path)
    if(path_list == False):
        return False
    path_count = len(path_list)
    path_list = sorted(path_list)
    for page in range(0, path_count):
        src = path + path_list[page]
        if(pad_zero(src) == False):
            return False

def listdir(path):
    manga_logging.log_debug("mangautility.listdir(" + path + ")")
    try:
        #List of non-hidden files
        directory_list = [f for f in os.listdir(path) if not f.startswith('.')]
    except FileNotFoundError:
        manga_logging.log_error("[" + path + "] NOT FOUND")
        manga_logging.message_write("[" + path + "] NOT FOUND")
        return False
    except NotADirectoryError:
        manga_logging.log_error("[" + path + "] IS NOT A DIRECTORY")
        manga_logging.message_write("[" + path + "] IS NOT A DIRECTORY")
        return False
    return directory_list

def mkdir(path):
    manga_logging.log_debug("mangautility.mkdir(" + path + ")")
    try:
        os.mkdir(path)
        manga_logging.log_debug("os.mkdir(" + path + ")")
        chown(path, int(os.getenv("PUID")), int(os.getenv("PGID")))
        return True
    except FileNotFoundError:
        manga_logging.log_error("[" + path + "] NOT FOUND")
        manga_logging.message_write("[" + path + "] NOT FOUND")
        return False
    except FileExistsError:
        directory = listdir(path)
        if(directory == False):
            return False
        if(len(directory) > 0):
            manga_logging.log_error("[" + path + "] ALREADY EXISTS")
            manga_logging.message_write("[" + path + "] ALREADY EXISTS")
            return False
        #Directory exists but it's empty, should be good
        return True

def remove(path):
    manga_logging.log_debug("mangautility.remove(" + path + ")")
    try:
        os.remove(path)
        manga_logging.log_debug("os.remove(" + path + ")")
    except FileNotFoundError:
        manga_logging.log_error("[" + path + "] NOT FOUND")
        manga_logging.message_write("[" + path + "] NOT FOUND")
        return False
    except PermissionError:
        manga_logging.log_error("[" + path + "] PERMISSION ERROR")
        manga_logging.message_write("[" + path + "] PERMISSION ERROR")
        return False

def remove_windows_char(src):
    manga_logging.log_debug("mangautility.remove_windows_char(" + src + ")")
    windows_char_not_allowed = '*\:?"<>|/'
    for char in windows_char_not_allowed:
        src = src.replace(char, '')
    return src

def rename(src, dest):
    manga_logging.log_debug("mangautility.rename()")
    #Single page rename
    if(isinstance(src, str) & isinstance(dest, str)):
        if(isfile(dest) == True):
            manga_logging.log_warning("[" + dest + "] ALREADY EXISTS")
            manga_logging.message_write("[" + dest + "] ALREADY EXISTS")
            return False
        try:
            shutil.move(src, dest)
            manga_logging.log_debug("shutil.move(" + src + ", " + dest + ")")
            chown(dest, int(os.getenv("PUID")), int(os.getenv("PGID")))
        except FileNotFoundError:
            if(isfile(src) == False):
                manga_logging.log_error("[" + src + "] NOT FOUND")
                manga_logging.message_write("[" + src + "] NOT FOUND")
            elif(isfile(dest) == False):
                manga_logging.log_error("[" + dest + "] NOT FOUND")
                manga_logging.message_write("[" + dest + "] NOT FOUND")
            return False
        except PermissionError:
            manga_logging.log_error("[" + src + ", " + dest + "] PERMISSION ERROR")
            manga_logging.message_write("[" + src + ", " + dest + "] PERMISSION ERROR")
            return False
    else:
        #Multiple page rename
        if(len(src) != len(dest)):
            manga_logging.log_error("UNEVEN PAGES FOR RENAME")
            manga_logging.message_write("UNEVEN PAGES FOR RENAME")
            return False
        for page in range(0, len(src)):
            if(isfile(dest[page]) == True):
                manga_logging.log_warning("[" + dest[page] + "] ALREADY EXISTS")
                manga_logging.message_write("[" + dest[page] + "] ALREADY EXISTS")
                return False
            try:
                shutil.move(src[page], dest[page])
                manga_logging.log_debug("shutil.move(" + src[page] + ", " + dest[page] + ")")
                chown(dest[page], int(os.getenv("PUID")), int(os.getenv("PGID")))
            except FileNotFoundError:
                if(isfile(src[page]) == False):
                    manga_logging.log_error("[" + src[page] + "] NOT FOUND")
                    manga_logging.message_write("[" + src[page] + "] NOT FOUND")
                elif(isfile(dest[page]) == False):
                    manga_logging.log_error("[" + dest[page] + "] NOT FOUND")
                    manga_logging.message_write("[" + dest[page] + "] NOT FOUND")
                return False
            except PermissionError:
                manga_logging.log_error("[" + src[page] + ", " + dest[page] + "] PERMISSION ERROR")
                manga_logging.message_write("[" + src[page] + ", " + dest[page] + "] PERMISSION ERROR")
                return False
    return True

def rmdir(path):
    manga_logging.log_debug("mangautility.rmdir(" + path + ")")
    check_path = listdir(path)
    if(check_path == False):
        return
    if(len(check_path) == 0):
        #Don't need to use try/except. listdir() already catches any exceptions that might prevent rmtree() from working.
        #Maybe PermissionsError? keep it this way for now
        shutil.rmtree(path)
        manga_logging.log_debug("shutil.copytree(" + path + ")")
    else:
        manga_logging.log_warning("[" + path + "] ISN'T EMPTY.")
        manga_logging.log_warning("[" + path + "] COULD NOT BE REMOVED.")

def sqlite_close(connection):
    manga_logging.log_debug("mangautility.sqlite_close()")
    try:
        connection.close()
    except AttributeError:
        manga_logging.log_error("NO VALID SQLite CONNECTION GIVEN")
        manga_logging.message_write("NO VALID SQLite CONNECTION GIVEN")
        return False

def sqlite_commit(connection):
    manga_logging.log_debug("mangautility.sqlite_commit()")
    try:
        connection.commit()
    except AttributeError:
        manga_logging.log_error("NO VALID SQLite CONNECTION GIVEN")
        manga_logging.message_write("NO VALID SQLite CONNECTION GIVEN")
        return False

def sqlite_execute(cursor, query, query_input):
    manga_logging.log_debug("mangautility.sqlite_execute()")
    if(query_input == ""):
        try:
            query_output = [query_data[0] for query_data in cursor.execute(query)]
        except sqlite3.OperationalError:
            manga_logging.log_error("[" + query + "] IS NOT A VALID OPERATION")
            manga_logging.message_write("[" + query + "] IS NOT A VALID OPERATION")
            return False
    else:
        try:
            query_output = [query_data[0] for query_data in cursor.execute(query, query_input)]
        except sqlite3.OperationalError:
            manga_logging.log_error("[" + query + " with data: " + query_input + "] IS NOT A VALID OPERATION")
            manga_logging.message_write("[" + query + " with data: " + query_input + "] IS NOT A VALID OPERATION")
            return False
        except sqlite3.IntegrityError:
            manga_logging.log_error("[" + query_input + "] CANNOT BE USED TO INSERT/UPDATE")
            manga_logging.message_write("[" + query_input + "] CANNOT BE USED TO INSERT/UPDATE")
            return False
    return query_output

def sqlite_get_connection(path):
    manga_logging.log_debug("mangautility.sqlite_get_connetion(" + path + ")")
    if(isfile(path) == False):
        manga_logging.log_error("[" + path + "] IS NOT A .db FILE")
        manga_logging.message_write("[" + path + "] IS NOT A .db FILE")
        return False
    return sqlite3.connect(path)

def sqlite_get_cursor(connection):
    manga_logging.log_debug("mangautility.sqlite_get_cursor()")
    try:
        cursor = connection.cursor()
    except AttributeError:
        manga_logging.log_error("NO VALID SQLite CONNECTION GIVEN")
        manga_logging.message_write("NO VALID SQLite CONNECTION GIVEN")
        return False
    return cursor

#temp workaround
def sqlite_get_name(manga):
    manga_logging.log_debug("mangautility.sqlite_get_name(" + manga + ")")
    if(manga == "Dr. STONE"):
        return "Dr_STONE"
    else:
        result = manga.replace(' ', '_')
        return result
