# manga_format.py
from . import manga_config as mc
from . import Directory
from . import Files
from . import SQLite


def auto_chapter_format(manga, chapter_title):
    chapter_pages = Files(mc.SOURCE_PATH)
    chapter_pages.pad_zero()
    # Connect to SQLite and get appropriate data
    manga_db = SQLite(mc.DB_FILE_PATH)
    query_input = (manga, )
    query_output = manga_db.execute("SELECT current_chapter FROM manga_progress WHERE manga = ?", query_input)
    new_chapter_number = query_output[0] + 1
    # Make copy of the chapter cover for One Piece
    if(manga == "One Piece"):
        op_cover_filename = "CH" + str(new_chapter_number).zfill(4) + " Cover" + chapter_pages.ext()
        if(new_chapter_number < 501):
            op_cover_path = mc.MANGA_PATH + manga + mc.OP_COVER_SUBPATH + "1-500/"
        elif(new_chapter_number < 1001):
            op_cover_path = mc.MANGA_PATH + manga + mc.OP_COVER_SUBPATH + "501-1000/"
        else:
            op_cover_path = mc.MANGA_PATH + manga + mc.OP_COVER_SUBPATH + "1001-End/"
        chapter_pages.copyfile(op_cover_path, op_cover_filename, 0)
    # Create directory path for the new chapter
    if(manga == "One Piece"):
        new_chapter_path = mc.MANGA_PATH + manga + mc.NEW_CHAPTERS_SUBPATH + str(new_chapter_number).zfill(4) + "/"
    else:
        new_chapter_path = mc.MANGA_PATH + manga + mc.NEW_CHAPTERS_SUBPATH + str(new_chapter_number).zfill(3) + "/"
    # Make new directory
    dest_path = Directory(new_chapter_path)
    dest_path.mk_dir()
    # Rename
    for page in range(0, chapter_pages.count):
        if(manga == "One Piece"):
            chapter_pages.rename(dest_path.path, manga + " - CH" + str(new_chapter_number).zfill(4) + "PG" + str(page + 1).zfill(2) + " - " + chapter_title + chapter_pages.ext(page), page)
        else:
            chapter_pages.rename(dest_path.path, manga + " - CH" + str(new_chapter_number).zfill(3) + "PG" + str(page + 1).zfill(2) + " - " + chapter_title + chapter_pages.ext(page), page)
    del chapter_pages, dest_path
    # Update appropriate tables
    manga_db.execute("UPDATE manga_progress SET current_chapter = ? WHERE manga = ?", (new_chapter_number, manga))
    manga_db.execute("INSERT INTO " + manga.replace(' ', '_') + "_chapter (manga, ch, title) VALUES(?, ?, ?)", (manga, new_chapter_number, chapter_title))
    manga_db.commit()
    manga_db.close()
    del manga_db

def auto_volume_format(manga, last_chapter_of_new_volume, volume_title):
    # Connect to SQLite and get appropriate data
    manga_db = SQLite(mc.DB_FILE_PATH)
    query_input = (manga, )
    # Get current volume number from SQLite and increment
    query_output = manga_db.execute("SELECT current_volume FROM manga_progress WHERE manga = ?", query_input)
    new_volume_number = query_output[0] + 1
    # Get the first chapter in the new volume
    query_output = manga_db.execute("SELECT first_chapter_of_new_volume FROM manga_progress WHERE manga = ?", query_input)
    first_chapter_in_volume = query_output[0]
    # Create new volume directory
    if(manga == "One Piece"):
        new_volume_path = mc.MANGA_PATH + manga + mc.VOLUMES_SUBPATH + manga + " Volume " + str(new_volume_number).zfill(3) + " - " + volume_title + "/"
    else:
        new_volume_path = mc.MANGA_PATH + manga + mc.VOLUMES_SUBPATH + manga + " Volume " + str(new_volume_number).zfill(2) + " - " + volume_title + "/"
    dest_path = Directory(new_volume_path)
    dest_path.mk_dir()
    # Rename volume cover
    volume_cover_page = Files(mc.SOURCE_PATH)
    if(manga == "One Piece"):
        volume_cover_page.rename(dest_path.path, manga + " - " + str(new_volume_number).zfill(3) + " - " + volume_title + volume_cover_page.ext())
    else:
        volume_cover_page.rename(dest_path.path, manga + " - " + str(new_volume_number).zfill(2) + " - " + volume_title + volume_cover_page.ext())
    del volume_cover_page
    # Move chapters
    chapter_count = int(last_chapter_of_new_volume) - first_chapter_in_volume + 1
    released_chapters = Files(mc.MANGA_PATH + manga + mc.NEW_CHAPTERS_SUBPATH)
    for volume_chapter in range(0, chapter_count):
        current_chapter_pages = Files(released_chapters.path + released_chapters.filenames[volume_chapter] + "/")
        for page in range(0, current_chapter_pages.count):
            current_chapter_pages.rename(dest_path.path, current_chapter_pages.filenames[page], page)
        current_chapter_pages.rm_dir()
    del dest_path, released_chapters, current_chapter_pages
    # Update appropriate tables
    manga_db.execute("UPDATE manga_progress SET current_volume = ?, first_chapter_of_new_volume = ? WHERE manga = ?", (new_volume_number, int(last_chapter_of_new_volume) + 1, manga))
    manga_db.execute("INSERT INTO " + manga.replace(' ', '_') + "_volume (manga, volume, title) VALUES(?, ?, ?)", (manga, new_volume_number, volume_title))
    manga_db.commit()
    manga_db.close()
    del manga_db

def manual_single_chapter_format(manga, chapter_number, chapter_title):
    chapter_pages = Files(mc.SOURCE_PATH)
    chapter_pages.pad_zero()
    dest_path = Directory(mc.DESTINATION_PATH + str(chapter_number).zfill(3) + "/")
    dest_path.mk_dir()
    for page in range(0, chapter_pages.count):
        chapter_pages.rename(dest_path.path, manga + " - CH" + str(chapter_number).zfill(3) + "PG" + str(page + 1).zfill(2) + " - " + chapter_title + chapter_pages.ext(page), page)
    del chapter_pages, dest_path

def manual_multiple_chapter_format(manga):
    src_chapters = Files(mc.SOURCE_PATH)
    for chapter in range(0, src_chapters.count):
        current_src_chapter = Files(src_chapters.path + src_chapters.filenames[chapter] + "/")
        current_src_chapter.pad_zero()
        number_title = src_chapters.filenames[chapter].split(" - ")
        current_chapter_number = number_title[0]
        current_chapter_title = number_title[1]
        dest_path = Directory(mc.DESTINATION_PATH + str(current_chapter_number).zfill(3) + "/")
        dest_path.mk_dir()
        for page in range(0, current_src_chapter.count):
            current_src_chapter.rename(dest_path.path, manga + " - CH" + str(current_chapter_number).zfill(3) + "PG" + str(page + 1).zfill(2) + " - " + current_chapter_title + current_src_chapter.ext(page), page)
        current_src_chapter.rm_dir()
    del src_chapters, current_src_chapter, dest_path

def manual_volume_format(manga, volume_number, volume_title):
    manual_multiple_chapter_format(manga)
    vol_chapters = Files(mc.DESTINATION_PATH)
    dest_dir = Directory(mc.DESTINATION_PATH + manga + " Volume " + str(volume_number).zfill(2) + " - " + volume_title + "/")
    dest_dir.mk_dir()
    for chapter in range (0, vol_chapters.count):
        current_vol_chapter = Files(vol_chapters.path + vol_chapters.filenames[chapter] + "/")
        for page in range(0, current_vol_chapter.count):
            current_vol_chapter.rename(dest_dir.path, current_vol_chapter.filenames[page], page)
        current_vol_chapter.rm_dir()
    del vol_chapters, dest_dir, current_vol_chapter
