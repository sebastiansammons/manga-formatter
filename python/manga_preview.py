# import sys
import manga_config
import manga_logging
import manga_utility


def auto_chapter(manga, chapter_title):
    manga_logging.log_debug("mangapreview.auto_chapter(" + manga + ", " + chapter_title + ")")
    if(chapter_title == ""):
        manga_logging.log_error("NO CHAPTER TITLE GIVEN")
        manga_logging.ERROR_MSG = "NO CHAPTER TITLE GIVEN"
        return False
    if(manga_utility.check_queue("auto_chapter") == False):
        return False
    #Most checks look good, add leading zero, even if it's not needed. The leading zero stays even if you abort the format
    if(manga_utility.leading_zero_dir(manga_config.QUEUE_PATH) == False):
        return False
    chapter_pages = manga_utility.listdir(manga_config.QUEUE_PATH)
    if(chapter_pages == False):
        return False
    page_count = len(chapter_pages)
    chapter_pages = sorted(chapter_pages)
    #Connect to SQLite and get appropriate data
    connection = manga_utility.sqlite_get_connection(manga_config.DB_FILE_PATH)
    if(connection == False):
        return False
    cursor = manga_utility.sqlite_get_cursor(connection)
    if(cursor == False):
        return False
    query_input = (manga, )
    #Get current chapter number from SQLite and increment
    query_output = manga_utility.sqlite_execute(cursor, "SELECT current_chapter FROM manga_progress WHERE manga = ?", query_input)
    if(query_output == False):
        return False
    new_chapter_number = query_output[0] + 1
    if(manga_utility.sqlite_close(connection) == False):
        return False
    #Directory path for the new chapter
    if(manga == "One Piece"):
        new_chapter_directory = manga_config.ROOT_MANGA_PATH + manga + manga_config.NEW_CHAPTERS_PATH + str(new_chapter_number).zfill(4) + "/"
    else:
        new_chapter_directory = manga_config.ROOT_MANGA_PATH + manga + manga_config.NEW_CHAPTERS_PATH + str(new_chapter_number).zfill(3) + "/"
    #Get source and destination file path
    page_src = [None] * page_count
    page_dest = [None] * page_count
    preview = [None] * page_count
    for i in range(0, page_count):
        page_src[i] = manga_config.QUEUE_PATH + str(chapter_pages[i])
        if(manga_utility.check_extension(page_src[i]) == False):
            return False
        if(manga == "One Piece"):
            page_dest[i] = new_chapter_directory + manga + " - CH" + str(new_chapter_number).zfill(4) + "PG" + str(i + 1).zfill(2) + " - " + chapter_title + manga_utility.get_extension(page_src[i])
        else:
            page_dest[i] = new_chapter_directory + manga + " - CH" + str(new_chapter_number).zfill(3) + "PG" + str(i + 1).zfill(2) + " - " + chapter_title + manga_utility.get_extension(page_src[i])
        if(manga_config.LOG_TYPE == "SIMPLE"):
            preview[i] = "Rename: " + page_src[i][page_src[i].rfind("/"):] + " to " + page_dest[i][page_dest[i].rfind("/"):]
        elif(manga_config.LOG_TYPE == "DETAILED"):
            preview[i] = "Rename: " + page_src[i] + " to " + page_dest[i]
    return preview

def auto_volume(manga, last_chapter_of_new_volume, volume_title):
    manga_logging.log_debug("mangapreview.auto_volume(" + manga + ", " + volume_title + ", " + last_chapter_of_new_volume + ")")
    if(volume_title == ""):
        manga_logging.log_error("NO VOLUME TITLE GIVEN")
        manga_logging.ERROR_MSG = "NO VOLUME TITLE GIVEN"
        return False
    if(last_chapter_of_new_volume == ""):
        manga_logging.log_error("NO VOLUME ENDING CHAPTER NUMBER GIVEN")
        manga_logging.ERROR_MSG = "NO VOLUME ENDING CHAPTER NUMBER GIVEN"
        return False
    if(manga_utility.check_queue("auto_volume") == False):
        return False
    #Connect to SQLite and get appropriate data
    connection = manga_utility.sqlite_get_connection(manga_config.DB_FILE_PATH)
    if(connection == False):
        return False
    cursor = manga_utility.sqlite_get_cursor(connection)
    if(cursor == False):
        return False
    query_input = (manga, )
    #Get current volume number from SQLite and increment
    query_output = manga_utility.sqlite_execute(cursor, "SELECT current_volume FROM manga_progress WHERE manga = ?", query_input)
    if(query_output == False):
        return False
    new_volume_number = query_output[0] + 1
    #Get the first chapter in the new volume
    query_output = manga_utility.sqlite_execute(cursor, "SELECT first_chapter_of_new_volume FROM manga_progress WHERE manga = ?", query_input)
    if(query_output == False):
        return False
    first_chapter_in_volume = query_output[0]
    if(manga_utility.sqlite_close(connection) == False):
        return False
    #Make sure first_chapter_in_volume is valid
    if(int(last_chapter_of_new_volume) <= first_chapter_in_volume):
        manga_logging.log_error("[" + last_chapter_of_new_volume + "] <= [" + str(first_chapter_in_volume) + "] FIRST CHAPTER IN VOLUME ISN'T VALID")
        manga_logging.ERROR_MSG = last_chapter_of_new_volume + " <= " + str(first_chapter_in_volume) + "] FIRST CHAPTER IN VOLUME ISN'T VALID"
        return False
    #New volume directory path
    if(manga == "One Piece"):
        new_volume_path = manga_config.ROOT_MANGA_PATH + manga + manga_config.VOLUME_CHAPTERS_PATH + manga + " Volume " + str(new_volume_number).zfill(3) + " - " + volume_title + "/"
    else:
        new_volume_path = manga_config.ROOT_MANGA_PATH + manga + manga_config.VOLUME_CHAPTERS_PATH + manga + " Volume " + str(new_volume_number).zfill(2) + " - " + volume_title + "/"
    chapter_count = int(last_chapter_of_new_volume) - first_chapter_in_volume + 1
    #List of chapter directory paths
    chapter_path = [None] * chapter_count
    #List of each chapter page filename (2D List)
    chapter_filename = [None] * chapter_count
    for chapter_number in range(first_chapter_in_volume, int(last_chapter_of_new_volume) + 1):
        if(manga == "One Piece"):
            chapter_path[chapter_number - first_chapter_in_volume] = manga_config.ROOT_MANGA_PATH + manga + manga_config.NEW_CHAPTERS_PATH + str(chapter_number).zfill(4) + "/"
        else:
            chapter_path[chapter_number - first_chapter_in_volume] = manga_config.ROOT_MANGA_PATH + manga + manga_config.NEW_CHAPTERS_PATH + str(chapter_number).zfill(3) + "/"
        chapter_filename[chapter_number - first_chapter_in_volume] = manga_utility.listdir(chapter_path[chapter_number - first_chapter_in_volume])
        if(chapter_filename[chapter_number - first_chapter_in_volume] == False):
            return False
        chapter_filename[chapter_number - first_chapter_in_volume] = sorted(chapter_filename[chapter_number - first_chapter_in_volume])
    if(manga_config.LOG_TYPE == "SIMPLE"):
        preview = [None] * chapter_count
        for i in range(0, chapter_count):
            preview[i] = "Rename: " + chapter_path[i][chapter_path[i].rfind("/", 0, chapter_path[i].rfind("/")):] + " to " + new_volume_path[new_volume_path.rfind("/", 0, new_volume_path.rfind("/")):]
    elif(manga_config.LOG_TYPE == "DETAILED"):
        #Get number of volume pages
        volume_pages = 0
        for i in range(0, chapter_count):
            volume_pages += len(chapter_filename[i])
        #Get source and destination filename path
        page_src = [None] * volume_pages
        page_dest = [None] * volume_pages
        preview = [None] * volume_pages
        page_count = 0
        for i in range(0, chapter_count):
            for j in range(0, len(chapter_filename[i])):
                page_src[page_count] = chapter_path[i] + chapter_filename[i][j]
                page_dest[page_count] = new_volume_path + chapter_filename[i][j]
                preview[page_count] = "Rename: " + page_src[page_count] + " to " + page_dest[page_count]
                page_count += 1
    return preview

def manual_single_chapter(manga, chapter_number, chapter_title):
    manga_logging.log_debug("mangapreview.manual_single_chapter(" + manga + ", " + chapter_title + ", " + chapter_number + ")")
    if(chapter_number == ""):
        manga_logging.log_error("NO CHAPTER NUMBER GIVEN")
        manga_logging.ERROR_MSG = "NO CHAPTER NUMBER GIVEN"
        return False
    if(manga_utility.check_queue("manual_single_chapter") == False):
        return False
    #Most checks look good, add leading zero, even if it's not needed. The leading zero stays even if you abort the format
    if(manga_utility.leading_zero_dir(manga_config.QUEUE_PATH) == False):
        return False
    chapter_pages = manga_utility.listdir(manga_config.QUEUE_PATH)
    if(chapter_pages == False):
        return False
    page_count = len(chapter_pages)
    chapter_pages = sorted(chapter_pages)
    #Directory path for the new chapter
    new_chapter_directory = manga_config.MANUAL_DEST_PATH + chapter_number.zfill(3) + "/"
    #Get source and destination file path
    page_src = [None] * page_count
    page_dest = [None] * page_count
    preview = [None] * page_count
    for i in range(0, page_count):
        page_src[i] = manga_config.QUEUE_PATH + str(chapter_pages[i])
        if(manga_utility.check_extension(page_src[i]) == False):
            return False
        if(chapter_title == ""):
            page_dest[i] = new_chapter_directory + manga + " - CH" + str(chapter_number).zfill(3) + "PG" + str(i + 1).zfill(2) + manga_utility.get_extension(page_src[i])
        else:
            page_dest[i] = new_chapter_directory + manga + " - CH" + str(chapter_number).zfill(3) + "PG" + str(i + 1).zfill(2) + " - " + chapter_title + manga_utility.get_extension(page_src[i])
        if(manga_config.LOG_TYPE == "SIMPLE"):
            preview[i] = "Rename: " + page_src[i][page_src[i].rfind("/"):] + " to " + page_dest[i][page_dest[i].rfind("/"):]
        elif(manga_config.LOG_TYPE == "DETAILED"):
            preview[i] = "Rename: " + page_src[i] + " to " + page_dest[i]
    return preview

def manual_multiple_chapter(manga):
    manga_logging.log_debug("mangapreview.manual_multiple_chapter" + manga + ")")
    if(manga_utility.check_queue("manual_multi_chapter") == False):
        return False
    chapter_path = manga_utility.listdir(manga_config.QUEUE_PATH)
    if(chapter_path == False):
        return False
    chapter_count = len(chapter_path)
    chapter_path = sorted(chapter_path)
    #List of source directory paths
    src_path = [None] * chapter_count
    #List of destination directory paths
    dest_path = [None] * chapter_count
    #List of each chapter page source filename (2D List)
    src_filename = [None] * chapter_count
    #List of each chapter page destination filename (2D List)
    dest_filename = [None] * chapter_count
    for i in range(0, chapter_count):
        #Get chapter source directory path
        src_path[i] = manga_config.QUEUE_PATH + chapter_path[i] + "/"
        #Most checks look good, add leading zero, even if it's not needed. The leading zero stays even if you abort the format
        if(manga_utility.leading_zero_dir(src_path[i]) == False):
            return False
        current_chapter_path = manga_utility.listdir(src_path[i])
        if(current_chapter_path == False):
            return False
        current_chapter_count = len(current_chapter_path)
        current_chapter_path = sorted(current_chapter_path)
        #Get each source and destination filename
        src_filename[i] = [None] * current_chapter_count
        dest_filename[i] = [None] * current_chapter_count
        for j in range(0, current_chapter_count):
            src_filename[i][j] = current_chapter_path[j]
            if(manga_utility.check_extension(current_chapter_path[j]) == False):
                return False
            dest_filename[i][j] = manga + " - CH" + (chapter_path[i].lstrip('0')).zfill(3) + "PG" + str(j + 1).zfill(2) + manga_utility.get_extension(current_chapter_path[j])
        #Chapter destination directory path
        dest_path[i] = manga_config.MANUAL_DEST_PATH + (chapter_path[i].lstrip('0')).zfill(3) + "/"
    #Make sure all destination directory paths are available
    for i in range(0, chapter_count):
        if(manga_utility.isdir(dest_path[i]) == True and len(manga_utility.listdir(dest_path[i])) > 0):
            manga_logging.log_error("[" + dest_path[i] + "] ALREADY EXISTS")
            manga_logging.ERROR_MSG = "[" + dest_path[i] + "] ALREADY EXISTS"
            return False
    #Make sure all destination directory paths are different
    #Since manual_multiple will remove leading zeroes, theres a chance that dest_path[i] can have duplicates
    #i.e. src has 058, 58, and 000058, all three of these will have the same destination directory of /058
    for i in range(0, chapter_count):
        for j in range(0, chapter_count):
            if(i != j):
                if(dest_path[i] == dest_path[j]):
                    manga_logging.log_error("[" + src_path[i] + "] AND [ " + src_path[j] + "] WILL HAVE THE SAME PATH [" + dest_path[i] + "]")
                    manga_logging.ERROR_MSG = "[" + src_path[i] + "] AND [ " + src_path[j] + "] WILL HAVE THE SAME DEST PATH [" + dest_path[i] + "]"
                    return False
    multi_chapter_pages = 0
    for i in range(0, chapter_count):
        multi_chapter_pages += len(src_filename[i])
    #Get source and destination filename path
    page_src = [None] * multi_chapter_pages
    page_dest = [None] * multi_chapter_pages
    preview = [None] * multi_chapter_pages
    page_count = 0
    for i in range(0, chapter_count):
        for j in range(0, len(src_filename[i])):
            page_src[page_count] = src_path[i] + src_filename[i][j]
            page_dest[page_count] = dest_path[i] + dest_filename[i][j]
            if(manga_config.LOG_TYPE == "SIMPLE"):
                preview[page_count] = "Rename: " + page_src[page_count][page_src[page_count].rfind(manga_config.QUEUE_PATH) + len(manga_config.QUEUE_PATH):] + " to " + page_dest[page_count][page_dest[page_count].rfind(manga_config.MANUAL_DEST_PATH) + len(manga_config.MANUAL_DEST_PATH):]
            elif(manga_config.LOG_TYPE == "DETAILED"):
                preview[page_count] = "Rename: " + page_src[page_count] + " to " + page_dest[page_count]
            page_count += 1
    return preview

def manual_volume(manga, volume_number, volume_title):
    manga_logging.log_debug("mangapreview.manual_volume(" + manga + ", " + volume_title + ", " + volume_number + ")")
    if(volume_number == ""):
        manga_logging.log_error("NO VOLUME NUMBER GIVEN")
        manga_logging.ERROR_MSG = "NO VOLUME NUMBER GIVEN"
        return False
    if(len(manga_utility.listdir(manga_config.MANUAL_DEST_PATH)) > 0):
        manga_logging.log_error("[DESTINATION] IS NOT EMPTY")
        manga_logging.ERROR_MSG = "[DESTINATION] IS NOT EMPTY"
        return False
    multi_chapter_preview = manual_multiple_chapter(manga)
    if(multi_chapter_preview == False):
        return False
    if(manga_utility.check_queue("manual_volume") == False):
        return False
    page_count = len(multi_chapter_preview)
    preview = [None] * page_count
    for i in range(0, page_count):
        if(volume_title == ""):
            if(manga_config.LOG_TYPE == "SIMPLE"):
                preview[i] = multi_chapter_preview[i][:multi_chapter_preview[i].rfind(" to ")] + " to /" + manga + " Volume " + str(volume_number).zfill(2) + multi_chapter_preview[i][multi_chapter_preview[i].rfind("/"):]
            elif(manga_config.LOG_TYPE == "DETAILED"):
                preview[i] = multi_chapter_preview[i][:multi_chapter_preview[i].rfind(" to ")] + " to " + manga_config.MANUAL_DEST_PATH + manga + " Volume " + str(volume_number).zfill(2) + multi_chapter_preview[i][multi_chapter_preview[i].rfind("/"):]
        else:
            if(manga_config.LOG_TYPE == "SIMPLE"):
                preview[i] = multi_chapter_preview[i][:multi_chapter_preview[i].rfind(" to ")] + " to /" + manga + " Volume " + str(volume_number).zfill(2) + " - " + volume_title + multi_chapter_preview[i][multi_chapter_preview[i].rfind("/"):]
            elif(manga_config.LOG_TYPE == "DETAILED"):
                preview[i] = multi_chapter_preview[i][:multi_chapter_preview[i].rfind(" to ")] + " to " + manga_config.MANUAL_DEST_PATH + manga + " Volume " + str(volume_number).zfill(2) + " - " + volume_title + multi_chapter_preview[i][multi_chapter_preview[i].rfind("/"):]
    return preview
    