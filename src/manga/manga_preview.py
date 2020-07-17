#manga_preview.py
from . import manga_config
from . import manga_logging
from . import manga_utility


def auto_chapter_preview(manga, chapter_title):
    manga_logging.log_debug("mangapreview.auto_chapter_preview(" + manga + ", " + chapter_title + ")")
    if(chapter_title == ""):
        manga_logging.log_error("NO CHAPTER TITLE GIVEN")
        manga_logging.message_write("NO CHAPTER TITLE GIVEN")
        return False
    if(manga_utility.check_source("auto_chapter") == False):
        return False
    #Most checks look good, add leading zero, even if it's not needed. The leading zero stays even if you abort the format
    if(manga_utility.pad_zero_dir(manga_config.SOURCE_PATH) == False):
        return False
    chapter_pages = manga_utility.listdir(manga_config.SOURCE_PATH)
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
        new_chapter_directory = manga_config.MANGA_PATH + manga + manga_config.NEW_CHAPTERS_SUBPATH + str(new_chapter_number).zfill(4) + "/"
    else:
        new_chapter_directory = manga_config.MANGA_PATH + manga + manga_config.NEW_CHAPTERS_SUBPATH + str(new_chapter_number).zfill(3) + "/"
    #Get source and destination file path
    page_src = [None] * page_count
    page_dest = [None] * page_count
    preview = [None] * page_count
    preview_type = manga_utility.get_preview_type()
    for page in range(0, page_count):
        page_src[page] = manga_config.SOURCE_PATH + str(chapter_pages[page])
        if(manga_utility.check_extension(page_src[page]) == False):
            return False
        if(manga == "One Piece"):
            page_dest[page] = new_chapter_directory + manga + " - CH" + str(new_chapter_number).zfill(4) + "PG" + str(page + 1).zfill(2) + " - " + chapter_title + manga_utility.get_extension(page_src[page])
        else:
            page_dest[page] = new_chapter_directory + manga + " - CH" + str(new_chapter_number).zfill(3) + "PG" + str(page + 1).zfill(2) + " - " + chapter_title + manga_utility.get_extension(page_src[page])
        if(preview_type == "SIMPLE"):
            preview[page] = "Rename: " + page_src[page][page_src[page].rfind("/"):] + " to " + page_dest[page][page_dest[page].rfind("/"):]
        elif(preview_type == "DETAILED"):
            preview[page] = "Rename: " + page_src[page] + " to " + page_dest[page]
    return preview

def auto_volume_preview(manga, last_chapter_of_new_volume, volume_title):
    manga_logging.log_debug("mangapreview.auto_volume_preview(" + manga + ", " + volume_title + ", " + last_chapter_of_new_volume + ")")
    if(volume_title == ""):
        manga_logging.log_error("NO VOLUME TITLE GIVEN")
        manga_logging.message_write("NO VOLUME TITLE GIVEN")
        return False
    if(last_chapter_of_new_volume == ""):
        manga_logging.log_error("NO VOLUME ENDING CHAPTER NUMBER GIVEN")
        manga_logging.message_write("NO VOLUME ENDING CHAPTER NUMBER GIVEN")
        return False
    if(manga_utility.check_source("auto_volume") == False):
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
        manga_logging.message_write(last_chapter_of_new_volume + " <= " + str(first_chapter_in_volume) + "] FIRST CHAPTER IN VOLUME ISN'T VALID")
        return False
    #New volume directory path
    if(manga == "One Piece"):
        new_volume_path = manga_config.MANGA_PATH + manga + manga_config.VOLUMES_SUBPATH + manga + " Volume " + str(new_volume_number).zfill(3) + " - " + volume_title + "/"
    else:
        new_volume_path = manga_config.MANGA_PATH + manga + manga_config.VOLUMES_SUBPATH + manga + " Volume " + str(new_volume_number).zfill(2) + " - " + volume_title + "/"
    chapter_count = int(last_chapter_of_new_volume) - first_chapter_in_volume + 1
    #List of chapter directory paths
    chapter_path = [None] * chapter_count
    #List of each chapter page filename (2D List)
    chapter_filename = [None] * chapter_count
    for chapter_number in range(first_chapter_in_volume, int(last_chapter_of_new_volume) + 1):
        if(manga == "One Piece"):
            chapter_path[chapter_number - first_chapter_in_volume] = manga_config.MANGA_PATH + manga + manga_config.NEW_CHAPTERS_SUBPATH + str(chapter_number).zfill(4) + "/"
        else:
            chapter_path[chapter_number - first_chapter_in_volume] = manga_config.MANGA_PATH + manga + manga_config.NEW_CHAPTERS_SUBPATH + str(chapter_number).zfill(3) + "/"
        chapter_filename[chapter_number - first_chapter_in_volume] = manga_utility.listdir(chapter_path[chapter_number - first_chapter_in_volume])
        if(chapter_filename[chapter_number - first_chapter_in_volume] == False):
            return False
        chapter_filename[chapter_number - first_chapter_in_volume] = sorted(chapter_filename[chapter_number - first_chapter_in_volume])
    preview_type = manga_utility.get_preview_type()
    if(preview_type == "SIMPLE"):
        preview = [None] * chapter_count
        for chapter in range(0, chapter_count):
            preview[chapter] = "Rename: " + chapter_path[chapter][chapter_path[chapter].rfind("/", 0, chapter_path[chapter].rfind("/")):] + " to " + new_volume_path[new_volume_path.rfind("/", 0, new_volume_path.rfind("/")):]
    elif(preview_type == "DETAILED"):
        #Get number of volume pages
        volume_pages = 0
        for chapter in range(0, chapter_count):
            volume_pages += len(chapter_filename[chapter])
        #Get source and destination filename path
        page_src = [None] * volume_pages
        page_dest = [None] * volume_pages
        preview = [None] * volume_pages
        page_count = 0
        for chapter in range(0, chapter_count):
            for page in range(0, len(chapter_filename[chapter])):
                page_src[page_count] = chapter_path[chapter] + chapter_filename[chapter][page]
                page_dest[page_count] = new_volume_path + chapter_filename[chapter][page]
                preview[page_count] = "Rename: " + page_src[page_count] + " to " + page_dest[page_count]
                page_count += 1
    return preview

def manual_single_chapter_preview(manga, chapter_number, chapter_title):
    manga_logging.log_debug("mangapreview.manual_single_chapter_preview(" + manga + ", " + chapter_title + ", " + chapter_number + ")")
    if(chapter_number == ""):
        manga_logging.log_error("NO CHAPTER NUMBER GIVEN")
        manga_logging.message_write("NO CHAPTER NUMBER GIVEN")
        return False
    if(manga_utility.check_source("manual_single_chapter") == False):
        return False
    #Most checks look good, add leading zero, even if it's not needed. The leading zero stays even if you abort the format
    if(manga_utility.pad_zero_dir(manga_config.SOURCE_PATH) == False):
        return False
    chapter_pages = manga_utility.listdir(manga_config.SOURCE_PATH)
    if(chapter_pages == False):
        return False
    page_count = len(chapter_pages)
    chapter_pages = sorted(chapter_pages)
    #Directory path for the new chapter
    new_chapter_directory = manga_config.DESTINATION_PATH + chapter_number.zfill(3) + "/"
    #Get source and destination file path
    page_src = [None] * page_count
    page_dest = [None] * page_count
    preview = [None] * page_count
    preview_type = manga_utility.get_preview_type()
    for page in range(0, page_count):
        page_src[page] = manga_config.SOURCE_PATH + str(chapter_pages[page])
        if(manga_utility.check_extension(page_src[page]) == False):
            return False
        if(chapter_title == ""):
            page_dest[page] = new_chapter_directory + manga + " - CH" + str(chapter_number).zfill(3) + "PG" + str(page + 1).zfill(2) + manga_utility.get_extension(page_src[page])
        else:
            page_dest[page] = new_chapter_directory + manga + " - CH" + str(chapter_number).zfill(3) + "PG" + str(page + 1).zfill(2) + " - " + chapter_title + manga_utility.get_extension(page_src[page])
        if(preview_type == "SIMPLE"):
            preview[page] = "Rename: " + page_src[page][page_src[page].rfind("/"):] + " to " + page_dest[page][page_dest[page].rfind("/"):]
        elif(preview_type == "DETAILED"):
            preview[page] = "Rename: " + page_src[page] + " to " + page_dest[page]
    return preview

def manual_multiple_chapter_preview(manga):
    manga_logging.log_debug("mangapreview.manual_multiple_chapter" + manga + ")")
    if(manga_utility.check_source("manual_multi_chapter") == False):
        return False
    chapter_path = manga_utility.listdir(manga_config.SOURCE_PATH)
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
    for chapter in range(0, chapter_count):
        #Get chapter source directory path
        src_path[chapter] = manga_config.SOURCE_PATH + chapter_path[chapter] + "/"
        #Most checks look good, add leading zero, even if it's not needed. The leading zero stays even if you abort the format
        if(manga_utility.pad_zero_dir(src_path[chapter]) == False):
            return False
        current_chapter_path = manga_utility.listdir(src_path[chapter])
        if(current_chapter_path == False):
            return False
        current_chapter_count = len(current_chapter_path)
        current_chapter_path = sorted(current_chapter_path)
        #Get each source and destination filename
        src_filename[chapter] = [None] * current_chapter_count
        dest_filename[chapter] = [None] * current_chapter_count
        for page in range(0, current_chapter_count):
            src_filename[chapter][page] = current_chapter_path[page]
            if(manga_utility.check_extension(current_chapter_path[page]) == False):
                return False
            dest_filename[chapter][page] = manga + " - CH" + (chapter_path[chapter].lstrip('0')).zfill(3) + "PG" + str(page + 1).zfill(2) + manga_utility.get_extension(current_chapter_path[page])
        #Chapter destination directory path
        dest_path[chapter] = manga_config.DESTINATION_PATH + (chapter_path[chapter].lstrip('0')).zfill(3) + "/"
    #Make sure all destination directory paths are available
    for chapter in range(0, chapter_count):
        if(manga_utility.isdir(dest_path[chapter]) == True and len(manga_utility.listdir(dest_path[chapter])) > 0):
            manga_logging.log_error("[" + dest_path[chapter] + "] ALREADY EXISTS")
            manga_logging.message_write("[" + dest_path[chapter] + "] ALREADY EXISTS")
            return False
    #Make sure all destination directory paths are different
    #Since manual_multiple will remove leading zeroes, theres a chance that dest_path[chapter] can have duplicates
    #i.e. src has 058, 58, and 000058, all three of these will have the same destination directory of /058
    #Compare all destination directories. This is an n^2 comparison but I don't expect to multi_chapter format
    #for more than 10 chapters
    for i in range(0, chapter_count):
        for j in range(0, chapter_count):
            if(i != j):
                if(dest_path[i] == dest_path[j]):
                    manga_logging.log_error("[" + src_path[i] + "] AND [ " + src_path[j] + "] WILL HAVE THE SAME PATH [" + dest_path[i] + "]")
                    manga_logging.message_write("[" + src_path[i] + "] AND [ " + src_path[j] + "] WILL HAVE THE SAME DEST PATH [" + dest_path[i] + "]")
                    return False
    multi_chapter_pages = 0
    for chapter in range(0, chapter_count):
        multi_chapter_pages += len(src_filename[chapter])
    #Get source and destination filename path
    page_src = [None] * multi_chapter_pages
    page_dest = [None] * multi_chapter_pages
    preview = [None] * multi_chapter_pages
    page_count = 0
    preview_type = manga_utility.get_preview_type()
    for chapter in range(0, chapter_count):
        for page in range(0, len(src_filename[chapter])):
            page_src[page_count] = src_path[chapter] + src_filename[chapter][page]
            page_dest[page_count] = dest_path[chapter] + dest_filename[chapter][page]
            if(preview_type == "SIMPLE"):
                preview[page_count] = "Rename: " + page_src[page_count][page_src[page_count].rfind(manga_config.SOURCE_PATH) + len(manga_config.SOURCE_PATH):] + " to " + page_dest[page_count][page_dest[page_count].rfind(manga_config.DESTINATION_PATH) + len(manga_config.DESTINATION_PATH):]
            elif(preview_type == "DETAILED"):
                preview[page_count] = "Rename: " + page_src[page_count] + " to " + page_dest[page_count]
            page_count += 1
    return preview

def manual_volume_preview(manga, volume_number, volume_title):
    manga_logging.log_debug("mangapreview.manual_volume_preview(" + manga + ", " + volume_title + ", " + volume_number + ")")
    if(volume_number == ""):
        manga_logging.log_error("NO VOLUME NUMBER GIVEN")
        manga_logging.message_write("NO VOLUME NUMBER GIVEN")
        return False
    if(len(manga_utility.listdir(manga_config.DESTINATION_PATH)) > 0):
        manga_logging.log_error("[DESTINATION] IS NOT EMPTY")
        manga_logging.message_write("[DESTINATION] IS NOT EMPTY")
        return False
    multi_chapter_preview = manual_multiple_chapter_preview(manga)
    if(multi_chapter_preview == False):
        return False
    if(manga_utility.check_source("manual_volume") == False):
        return False
    page_count = len(multi_chapter_preview)
    preview = [None] * page_count
    preview_type = manga_utility.get_preview_type()
    for page in range(0, page_count):
        if(volume_title == ""):
            if(preview_type == "SIMPLE"):
                preview[page] = multi_chapter_preview[page][:multi_chapter_preview[page].rfind(" to ")] + " to /" + manga + " Volume " + str(volume_number).zfill(2) + multi_chapter_preview[page][multi_chapter_preview[page].rfind("/"):]
            elif(preview_type == "DETAILED"):
                preview[page] = multi_chapter_preview[page][:multi_chapter_preview[page].rfind(" to ")] + " to " + manga_config.DESTINATION_PATH + manga + " Volume " + str(volume_number).zfill(2) + multi_chapter_preview[page][multi_chapter_preview[page].rfind("/"):]
        else:
            if(preview_type == "SIMPLE"):
                preview[page] = multi_chapter_preview[page][:multi_chapter_preview[page].rfind(" to ")] + " to /" + manga + " Volume " + str(volume_number).zfill(2) + " - " + volume_title + multi_chapter_preview[page][multi_chapter_preview[page].rfind("/"):]
            elif(preview_type == "DETAILED"):
                preview[page] = multi_chapter_preview[page][:multi_chapter_preview[page].rfind(" to ")] + " to " + manga_config.DESTINATION_PATH + manga + " Volume " + str(volume_number).zfill(2) + " - " + volume_title + multi_chapter_preview[page][multi_chapter_preview[page].rfind("/"):]
    return preview
