# import sys
import manga_config
import manga_logging
import manga_utility


def full_manga(manga):
    manga_logging.log_debug("mangafull.full_manga(" + manga + ")")
    manga_path = manga_config.ROOT_MANGA_PATH + manga + manga_config.NEW_CHAPTERS_PATH
    if(check_full_manga(manga, manga_path) == False):
        return False
    if(full_manga_leading_zero(manga_path) == False):
        return False
    #Connect to SQLite and get appropriate data
    sql_name = manga_utility.sqlite_get_name(manga)
    connection = manga_utility.sqlite_get_connection(manga_config.DB_FILE_PATH)
    if(connection == False):
        return False
    cursor = manga_utility.sqlite_get_cursor(connection)
    if(cursor == False):
        return False
    if(manga == "Bleach"):
        chapter_number = manga_utility.sqlite_execute(cursor, "SELECT count FROM " + sql_name + "_chapter", "")
        if(chapter_number == False):
            return False
        chapter_style_number = manga_utility.sqlite_execute(cursor, "SELECT ch FROM " + sql_name + "_chapter", "")
        if(chapter_style_number == False):
            return False
    else:
        chapter_number = manga_utility.sqlite_execute(cursor, "SELECT ch FROM " + sql_name + "_chapter", "")
        if(chapter_number == False):
            return False
    chapter_title = manga_utility.sqlite_execute(cursor, "SELECT title FROM " + sql_name + "_chapter", "")
    if(chapter_title == False):
        return False
    volume_number = manga_utility.sqlite_execute(cursor, "SELECT volume FROM " + sql_name + "_volume", "")
    if(volume_number == False):
        return False
    volume_title = manga_utility.sqlite_execute(cursor, "SELECT title FROM " + sql_name + "_volume", "")
    if(volume_title == False):
        return False
    if(manga_utility.sqlite_close(connection) == False):
        return False
    #Get list of volume directory paths
    #NOTE Ongoing manga's will have a "ZZZ No Volume Chapters" Directory, these don't have a released volume yet
    volume_path = manga_utility.listdir(manga_path)
    if(volume_path == False):
        return False
    volume_count = len(volume_path)
    volume_path = sorted(volume_path)
    #Chapter Counter for entire mass format
    manga_count = 0
    #Every volume
    for volume in range(0, volume_count):
        #Get new volume directory path
        if(volume_path[volume] == "ZZZ No Volume Chapters"):
            #"ZZZ No Volume Chapters" directory
            current_volume_path = "New Chapters/"
        else:
            #"Volume ##" directory
            if(volume_title[volume] == ""):
                volume_title[volume] = "NULL"
            if(manga == "One Piece"):
                current_volume_path = manga + " Volume " + str(volume_number[volume]).zfill(3) + " - " + manga_utility.remove_windows_char(volume_title[volume]) + "/"
            else:
                current_volume_path = manga + " Volume " + str(volume_number[volume]).zfill(2) + " - " + manga_utility.remove_windows_char(volume_title[volume]) + "/"
        #Create new volume directory
        new_volume_path = manga_config.ROOT_MANGA_PATH + manga + manga_config.VOLUME_CHAPTERS_PATH + current_volume_path
        if(manga_utility.mkdir(new_volume_path) == False):
            return False
        #Get list of Chapter directory paths within the current Volume
        chapter_path = manga_utility.listdir(manga_path + volume_path[volume])
        if(chapter_path == False):
            return False
        chapter_count = len(chapter_path)
        chapter_path = sorted(chapter_path)
        #Every chapter in current volume
        for chapter in range(0, chapter_count):
            if(manga_utility.isfile(manga_path + volume_path[volume] + "/" + chapter_path[chapter]) == True):
                #Volume cover file
                if(manga == "One Piece"):
                    manga_utility.rename(manga_path + volume_path[volume] + "/" + chapter_path[chapter], new_volume_path + manga + " - " + str(volume_number[volume]).zfill(3) + " - " + manga_utility.remove_windows_char(volume_title[volume]) + manga_utility.get_extension(chapter_path[chapter]))
                else:
                    manga_utility.rename(manga_path + volume_path[volume] + "/" + chapter_path[chapter], new_volume_path + manga + " - " + str(volume_number[volume]).zfill(2) + " - " + manga_utility.remove_windows_char(volume_title[volume]) + manga_utility.get_extension(chapter_path[chapter]))
                continue
            else:
                #Chapter directory
                current_chapter_path = manga_path + volume_path[volume] + "/" + chapter_path[chapter] + "/"
                chapter_pages = manga_utility.listdir(current_chapter_path)
                if(chapter_pages == False):
                    return False
                page_count = len(chapter_pages)
                chapter_pages = sorted(chapter_pages)
                if(volume_path[volume] == "ZZZ No Volume Chapters"):
                    #"ZZZ No Volume Chapters" Directory. Make directories for each chapter
                    if(manga == "One Piece"):
                        new_chapter_path = new_volume_path + str(chapter_number[manga_count]).zfill(4) + "/"
                    else:
                        new_chapter_path = new_volume_path + str(chapter_number[manga_count]).zfill(3) + "/"
                    if(manga_utility.mkdir(new_chapter_path) == False):
                        return False
                page_src = [None] * page_count
                page_dest = [None] * page_count
                #Every page in chapter
                for page in range(0, page_count):
                    page_src[page] = current_chapter_path + chapter_pages[page]
                    if(manga == "Bleach"):
                        page_dest[page] = new_volume_path + manga + " - CH" + str(chapter_number[manga_count]).zfill(3) + "PG" + str(page + 1).zfill(2) + " - " + str(chapter_style_number[manga_count]) + " " + manga_utility.remove_windows_char(chapter_title[manga_count]) + manga_utility.get_extension(page_src[page])
                    elif(manga == "One Piece"):
                        if(page == 0):
                            #First page make a copy of the cover, put in Cover
                            op_cover_src = page_src[page]
                            op_cover_dest = manga_config.OP_COVER_PATH + "CH" + str(chapter_number[manga_count]).zfill(4) + " Cover" + manga_utility.get_extension(page_src[page])
                            manga_utility.copyfile(op_cover_src, op_cover_dest)
                        if(volume_path[volume] == "ZZZ No Volume Chapters"):
                            page_dest[page] = new_chapter_path + manga + " - CH" + str(chapter_number[manga_count]).zfill(4) + "PG" + str(page + 1).zfill(2) + " - " + manga_utility.remove_windows_char(chapter_title[manga_count]) + manga_utility.get_extension(page_src[page])
                        else:
                            page_dest[page] = new_volume_path + manga + " - CH" + str(chapter_number[manga_count]).zfill(4) + "PG" + str(page + 1).zfill(2) + " - " + manga_utility.remove_windows_char(chapter_title[manga_count]) + manga_utility.get_extension(page_src[page])
                    else:
                        if(volume_path[volume] == "ZZZ No Volume Chapters"):
                            page_dest[page] = new_chapter_path + manga + " - CH" + str(chapter_number[manga_count]).zfill(3) + "PG" + str(page + 1).zfill(2) + " - " + manga_utility.remove_windows_char(chapter_title[manga_count]) + manga_utility.get_extension(page_src[page])
                        else:
                            page_dest[page] = new_volume_path + manga + " - CH" + str(chapter_number[manga_count]).zfill(3) + "PG" + str(page + 1).zfill(2) + " - " + manga_utility.remove_windows_char(chapter_title[manga_count]) + manga_utility.get_extension(page_src[page])
                    #Rename
                    manga_utility.rename(page_src[page], page_dest[page])
                #Remove old chapter directory
                manga_utility.rmdir(current_chapter_path)
                #Increment manga index
                manga_count += 1
        #Remove old volume directory
        manga_utility.rmdir(manga_path + volume_path[volume])
    #
    #Remove old "New Chapters" directory
    #
    manga_utility.rmdir(manga_config.ROOT_MANGA_PATH + manga + manga_config.NEW_CHAPTERS_PATH)
    #
    #Move new "New Chapters" directory to original path
    #
    manga_utility.copydir(manga_config.ROOT_MANGA_PATH + manga + manga_config.VOLUME_CHAPTERS_PATH + "New Chapters/", manga_config.ROOT_MANGA_PATH + manga + manga_config.NEW_CHAPTERS_PATH)
    #Remove src
    manga_utility.rmdir(manga_config.ROOT_MANGA_PATH + manga + manga_config.VOLUME_CHAPTERS_PATH + "New Chapters/")

def full_manga_leading_zero(manga_path):
    manga_logging.log_debug("mangafull.full_manga_leading_zero(" + manga_path + ")")
    volume_path = manga_utility.listdir(manga_path)
    if(volume_path == False):
        return False
    volume_count = len(volume_path)
    volume_path = sorted(volume_path)
    #Every volume
    for volume in range(0, volume_count):
        chapter_path = manga_utility.listdir(manga_path + volume_path[volume])
        if(chapter_path == False):
            return False
        chapter_count = len(chapter_path)
        chapter_path = sorted(chapter_path)
        #Every chapter in current volume
        for chapter in range(0, chapter_count):
            if(manga_utility.isfile(manga_path + volume_path[volume] + "/" + chapter_path[chapter]) == True):
                #Volume cover file, skip
                continue
            else:
                #Chapter directory
                current_chapter_path = manga_path + volume_path[volume] + "/" + chapter_path[chapter]
                chapter_pages = manga_utility.listdir(current_chapter_path)
                if(chapter_pages == False):
                    return False
                page_count = len(chapter_pages)
                chapter_pages = sorted(chapter_pages)
                #Every Page
                for page in range(0, page_count):
                    page_src = current_chapter_path + "/" + chapter_pages[page]
                    if(manga_utility.leading_zero(page_src) == False):
                        return False

def check_full_manga(manga,manga_path):
    manga_logging.log_debug("mangafull.check_full_manga(" + manga + ", " + manga_path + ")")
    #Connect to SQLite and get appropriate data
    sql_name = manga_utility.sqlite_get_name(manga)
    connection = manga_utility.sqlite_get_connection(manga_config.DB_FILE_PATH)
    if(connection == False):
        return False
    cursor = manga_utility.sqlite_get_cursor(connection)
    if(cursor == False):
        return False
    if(manga == "Bleach"):
        chapter_number = manga_utility.sqlite_execute(cursor, "SELECT count FROM " + sql_name + "_chapter", "")
        if(chapter_number == False):
            return False
    else:
        chapter_number = manga_utility.sqlite_execute(cursor, "SELECT ch FROM " + sql_name + "_chapter", "")
        if(chapter_number == False):
            return False
    if(manga_utility.sqlite_close(connection) == False):
        return False
    #Get the number of chapters in the manga and make sure that the manga directory has the same number (no missing chapters)
    total_chapter_count = len(chapter_number)
    chapter_found = 0
    volume_path = manga_utility.listdir(manga_path)
    if(volume_path == False):
        return False
    volume_count = len(volume_path)
    volume_path = sorted(volume_path)
    #Every volume
    for volume in range(0, volume_count):
        chapter_path = manga_utility.listdir(manga_path + volume_path[volume])
        if(chapter_path == False):
            return False
        chapter_count = len(chapter_path)
        chapter_path = sorted(chapter_path)
        #Every chapter in current volume
        for chapter in range(0, chapter_count):
            if(manga_utility.isfile(manga_path + volume_path[volume] + "/" + chapter_path[chapter]) == True):
                #Volume cover file, skip
                continue
            else:
                #Chapter directory
                current_chapter_path = manga_path + volume_path[volume] + "/" + chapter_path[chapter]
                chapter_pages = manga_utility.listdir(current_chapter_path)
                if(chapter_pages == False):
                    return False
                page_count = len(chapter_pages)
                if(page_count == 0):
                    manga_logging.log_error("[" + current_chapter_path + "] IS EMPTY")
                    manga_logging.ERROR_MSG = "[" + current_chapter_path + "] IS EMPTY"
                    return False
                chapter_found += 1
    if(chapter_found != total_chapter_count):
        manga_logging.log_error("[" + manga_path + "] HAS A MISSING CHAPTER")
        manga_logging.ERROR_MSG = "[" + manga_path + "] HAS A MISSING CHAPTER"
        return False
        