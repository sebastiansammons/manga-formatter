#manga_format.py
from . import manga_config
from . import manga_logging
from . import manga_utility


def auto_chapter_format(manga, chapter_title):
    manga_logging.log_debug("mangaformatlib.auto_chapter_format(" + manga + ", " + chapter_title + ")")
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
    #Create directory path for the new chapter
    if(manga == "One Piece"):
        new_chapter_path = manga_config.MANGA_PATH + manga + manga_config.NEW_CHAPTERS_SUBPATH + str(new_chapter_number).zfill(4) + "/"
    else:
        new_chapter_path = manga_config.MANGA_PATH + manga + manga_config.NEW_CHAPTERS_SUBPATH + str(new_chapter_number).zfill(3) + "/"
    #Make new directory
    if(manga_utility.mkdir(new_chapter_path) == False):
        return False
    #Get source and destination file path
    page_src = [None] * page_count
    page_dest = [None] * page_count
    for page in range(0, page_count):
        page_src[page] = manga_config.SOURCE_PATH + str(chapter_pages[page])
        if(manga == "One Piece"):
            page_dest[page] = new_chapter_path + manga + " - CH" + str(new_chapter_number).zfill(4) + "PG" + str(page + 1).zfill(2) + " - " + chapter_title + manga_utility.get_extension(page_src[page])
        else:
            page_dest[page] = new_chapter_path + manga + " - CH" + str(new_chapter_number).zfill(3) + "PG" + str(page + 1).zfill(2) + " - " + chapter_title + manga_utility.get_extension(page_src[page])
    #Rename
    if(manga_utility.rename(page_src, page_dest) == False):
        return False
    #Update appropriate tables
    result = manga_utility.sqlite_execute(cursor, "UPDATE manga_progress SET current_chapter = ? WHERE manga = ?", (new_chapter_number, manga))
    if(result == False):
        return False
    result = manga_utility.sqlite_execute(cursor, "INSERT INTO " + manga_utility.sqlite_get_name(manga) + "_chapter (manga, ch, title) VALUES(?, ?, ?)", (manga, new_chapter_number, chapter_title))
    if(result == False):
        return False
    #commit and close SQLite connection
    if(manga_utility.sqlite_commit(connection) == False):
        return False
    if(manga_utility.sqlite_close(connection) == False):
        return False
    #Make copy of the chapter cover for One Piece
    if(manga == "One Piece"):
        op_cover_src = page_dest[0]
        if(new_chapter_number < 501):
            op_cover_dest = manga_config.MANGA_PATH + manga + manga_config.OP_COVER_SUBPATH + "1-500/CH" + str(new_chapter_number).zfill(4) + " Cover" + manga_utility.get_extension(page_src[0])
        elif(new_chapter_number < 1001):
            op_cover_dest = manga_config.MANGA_PATH + manga + manga_config.OP_COVER_SUBPATH + "501-1000/CH" + str(new_chapter_number).zfill(4) + " Cover" + manga_utility.get_extension(page_src[0])
        else:
            op_cover_dest = manga_config.MANGA_PATH + manga + manga_config.OP_COVER_SUBPATH + "1001-End/CH" + str(new_chapter_number).zfill(4) + " Cover" + manga_utility.get_extension(page_src[0])
        manga_utility.copyfile(op_cover_src, op_cover_dest)
    return True

def auto_volume_format(manga, last_chapter_of_new_volume, volume_title):
    manga_logging.log_debug("mangaformatlib.auto_volume_preview(" + manga + ", " + volume_title + ", " + last_chapter_of_new_volume + ")")
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
    #New volume directory path
    if(manga == "One Piece"):
        new_volume_path = manga_config.MANGA_PATH + manga + manga_config.VOLUMES_SUBPATH + manga + " Volume " + str(new_volume_number).zfill(3) + " - " + volume_title + "/"
    else:
        new_volume_path = manga_config.MANGA_PATH + manga + manga_config.VOLUMES_SUBPATH + manga + " Volume " + str(new_volume_number).zfill(2) + " - " + volume_title + "/"
    #Create new volume directory
    if(manga_utility.mkdir(new_volume_path) == False):
        return False
    #Rename volume cover
    volume_cover_filename = manga_utility.listdir(manga_config.SOURCE_PATH)
    if(volume_cover_filename == False):
        return False
    volume_cover_src = manga_config.SOURCE_PATH + volume_cover_filename[0]
    if(manga == "One Piece"):
        volume_cover_dest = new_volume_path + manga + " - " + str(new_volume_number).zfill(3) + " - " + volume_title + manga_utility.get_extension(volume_cover_src)
    else:
        volume_cover_dest = new_volume_path + manga + " - " + str(new_volume_number).zfill(2) + " - " + volume_title + manga_utility.get_extension(volume_cover_src)
    if(manga_utility.rename(volume_cover_src, volume_cover_dest) == False):
        return False
    #Finally move chapters
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
    #Get number of volume pages
    volume_pages = 0
    for chapter in range(0, chapter_count):
        volume_pages += len(chapter_filename[chapter])
    #Get source and destination filename path
    page_src = [None] * volume_pages
    page_dest = [None] * volume_pages
    page_count = 0
    for chapter in range(0, chapter_count):
        for page in range(0, len(chapter_filename[chapter])):
            page_src[page_count] = chapter_path[chapter] + chapter_filename[chapter][page]
            page_dest[page_count] = new_volume_path + chapter_filename[chapter][page]
            page_count += 1
    #Rename
    if(manga_utility.rename(page_src, page_dest) == False):
        return False
    #Remove old directories
    for chapter in range(0, chapter_count):
        manga_utility.rmdir(chapter_path[chapter])
    #Update appropriate tables
    result = manga_utility.sqlite_execute(cursor, "UPDATE manga_progress SET current_volume = ?, first_chapter_of_new_volume = ? WHERE manga = ?", (new_volume_number, int(last_chapter_of_new_volume) + 1, manga))
    if(result == False):
        return False
    result = manga_utility.sqlite_execute(cursor, "INSERT INTO " + manga_utility.sqlite_get_name(manga) + "_volume (manga, volume, title) VALUES(?, ?, ?)", (manga, new_volume_number, volume_title))
    if(result == False):
        return False
    #commit and close SQLite connection
    if(manga_utility.sqlite_commit(connection) == False):
        return False
    if(manga_utility.sqlite_close(connection) == False):
        return False
    return True

def manual_single_chapter_format(manga, chapter_number, chapter_title):
    manga_logging.log_debug("mangaformatlib.manual_single_chapter_format(" + manga + ", " + chapter_title + ", " + chapter_number + ")")
    chapter_pages = manga_utility.listdir(manga_config.SOURCE_PATH)
    if(chapter_pages == False):
        return False
    page_count = len(chapter_pages)
    chapter_pages = sorted(chapter_pages)
    #Create directory path for the new chapter
    new_chapter_path = manga_config.DESTINATION_PATH + chapter_number.zfill(3) + "/"
    if(manga_utility.mkdir(new_chapter_path) == False):
        return False
    #Get source and destination file path
    page_src = [None] * page_count
    page_dest = [None] * page_count
    for page in range(0, page_count):
        page_src[page] = manga_config.SOURCE_PATH + str(chapter_pages[page])
        if(chapter_title == ""):
            page_dest[page] = new_chapter_path + manga + " CH" + str(chapter_number).zfill(3) + "PG" + str(page + 1).zfill(2) + manga_utility.get_extension(page_src[page])
        else:
            page_dest[page] = new_chapter_path + manga + " CH" + str(chapter_number).zfill(3) + "PG" + str(page + 1).zfill(2) + " - " + chapter_title + manga_utility.get_extension(page_src[page])
    #Rename
    if(manga_utility.rename(page_src, page_dest) == False):
        return False
    return True

def manual_multiple_chapter_format(manga):
    manga_logging.log_debug("mangaformatlib.manual_multiple_chapter_format(" + manga + ")")
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
        #Get pages for each chapter
        current_chapter_path = manga_utility.listdir(src_path[chapter])
        if(current_chapter_path == False):
            return False
        current_chapter_count = len(current_chapter_path)
        current_chapter_path = sorted(current_chapter_path)
        #Chapter destination directory path
        dest_path[chapter] = manga_config.DESTINATION_PATH + (chapter_path[chapter].lstrip('0')).zfill(3) + "/"
        if(manga_utility.mkdir(dest_path[chapter]) == False):
            return False
        #Get each source and destination filename
        src_filename[chapter] = [None] * current_chapter_count
        dest_filename[chapter] = [None] * current_chapter_count
        for page in range(0, current_chapter_count):
            src_filename[chapter][page] = current_chapter_path[page]
            dest_filename[chapter][page] = manga + " - CH" + (chapter_path[chapter].lstrip('0')).zfill(3) + "PG" + str(page + 1).zfill(2) + manga_utility.get_extension(current_chapter_path[page])
    multi_chapter_pages = 0
    for chapter in range(0, chapter_count):
        multi_chapter_pages += len(src_filename[chapter])
    #Get source and destination filename path
    page_src = [None] * multi_chapter_pages
    page_dest = [None] * multi_chapter_pages
    page_count = 0
    for chapter in range(0, chapter_count):
        for page in range(0, len(src_filename[chapter])):
            page_src[page_count] = src_path[chapter] + src_filename[chapter][page]
            page_dest[page_count] = dest_path[chapter] + dest_filename[chapter][page]
            page_count += 1
    #Rename
    if(manga_utility.rename(page_src, page_dest) == False):
        return False
    #Remove old directories
    for chapter in range(0, chapter_count):
        manga_utility.rmdir(src_path[chapter])
    return True

def manual_volume_format(manga, volume_number, volume_title):
    manga_logging.log_debug("mangaformatlib.manual_volume_preview(" + manga + ", " + volume_title + ", " + volume_number + ")")
    if(manual_multiple_chapter_format(manga) == False):
        return False
    chapter_path = manga_utility.listdir(manga_config.DESTINATION_PATH)
    if(chapter_path == False):
        return False
    chapter_count = len(chapter_path)
    chapter_path = sorted(chapter_path)
    chapter_filename = [None] * chapter_count
    #Get new volume directory path
    if(volume_title == ""):
        new_volume_path = manga_config.DESTINATION_PATH + manga + " Volume " + str(volume_number).zfill(2) + "/"
    else:
        new_volume_path = manga_config.DESTINATION_PATH + manga + " Volume " + str(volume_number).zfill(2) + " - " + volume_title + "/"
    #Create new volume directory
    if(manga_utility.mkdir(new_volume_path) == False):
        return False
    #Get list of each chapter's filename
    for chapter in range(0, chapter_count):
        chapter_filename[chapter] = manga_utility.listdir(manga_config.DESTINATION_PATH + chapter_path[chapter])
        if(chapter_filename[chapter] == False):
            return False
        chapter_filename[chapter] = sorted(chapter_filename[chapter])
    #Get number of volume pages
    volume_pages = 0
    for chapter in range(0, chapter_count):
        volume_pages += len(chapter_filename[chapter])
    #Get source and destination filename path
    page_src = [None] * volume_pages
    page_dest = [None] * volume_pages
    page_count = 0
    for chapter in range(0, chapter_count):
        for page in range(0, len(chapter_filename[chapter])):
            page_src[page_count] = manga_config.DESTINATION_PATH + chapter_path[chapter] + "/" +chapter_filename[chapter][page]
            page_dest[page_count] = new_volume_path + chapter_filename[chapter][page]
            page_count += 1
    #Rename
    if(manga_utility.rename(page_src, page_dest) == False):
        return False
    #Remove old directories
    for chapter in range(0, chapter_count):
        manga_utility.rmdir(manga_config.DESTINATION_PATH + chapter_path[chapter])
    return True
