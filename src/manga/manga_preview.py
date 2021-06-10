#manga_preview.py
import os
from . import manga_config as mc
from . import Files
from . import SQLite

def auto_chapter_preview(manga, chapter_title):
    chapter_pages = Files(mc.SOURCE_PATH)
    chapter_pages.pad_zero("Preview")
    #Connect to SQLite and get appropriate data
    manga_db = SQLite(mc.DB_FILE_PATH)
    query_input = (manga, )
    query_output = manga_db.execute("SELECT current_chapter FROM manga_progress WHERE manga = ?", query_input)
    new_chapter_number = query_output[0] + 1
    manga_db.close()
    del manga_db
    #Directory path for the new chapter
    if(manga == "One Piece"):
        new_chapter_path = mc.MANGA_PATH + manga + mc.NEW_CHAPTERS_SUBPATH + str(new_chapter_number).zfill(4) + "/"
    else:
        new_chapter_path = mc.MANGA_PATH + manga + mc.NEW_CHAPTERS_SUBPATH + str(new_chapter_number).zfill(3) + "/"
    #Preview Rename
    preview_type = os.getenv("PREVIEW_TYPE", "SIMPLE")
    preview_changes = []
    if(preview_type == "SIMPLE"):
        for page in range(0, chapter_pages.count):
            if(manga == "One Piece"):
                preview_changes.append("Rename: " + chapter_pages.filenames[page] + " to " + manga + " - CH" + str(new_chapter_number).zfill(4) + "PG" + str(page + 1).zfill(2) + " - " + chapter_title + chapter_pages.ext(page))
            else:
                preview_changes.append("Rename: " + chapter_pages.filenames[page] + " to " + manga + " - CH" + str(new_chapter_number).zfill(3) + "PG" + str(page + 1).zfill(2) + " - " + chapter_title + chapter_pages.ext(page))
    elif(preview_type == "DETAIlED"):
        for page in range(0, chapter_pages.count):
            if(manga == "One Piece"):
                preview_changes.append("Rename: " + chapter_pages.path + chapter_pages.filenames[page] + " to " + new_chapter_path + manga + " - CH" + str(new_chapter_number).zfill(4) + "PG" + str(page + 1).zfill(2) + " - " + chapter_title + chapter_pages.ext(page))
            else:
                preview_changes.append("Rename: " + chapter_pages.path + chapter_pages.filenames[page] + " to " + new_chapter_path + manga + " - CH" + str(new_chapter_number).zfill(3) + "PG" + str(page + 1).zfill(2) + " - " + chapter_title + chapter_pages.ext(page))
    del chapter_pages
    return preview_changes

def auto_volume_preview(manga, last_chapter_of_new_volume, volume_title):
    manga_db = SQLite(mc.DB_FILE_PATH)
    query_input = (manga, )
    #Get current volume number from SQLite and increment
    query_output = manga_db.execute("SELECT current_volume FROM manga_progress WHERE manga = ?", query_input)
    new_volume_number = query_output[0] + 1
    #Get the first chapter in the new volume
    query_output = manga_db.execute("SELECT first_chapter_of_new_volume FROM manga_progress WHERE manga = ?", query_input)
    first_chapter_in_volume = query_output[0]
    manga_db.close()
    del manga_db
    #Preview new volume directory
    if(manga == "One Piece"):
        new_volume_path = mc.MANGA_PATH + manga + mc.VOLUMES_SUBPATH + manga + " Volume " + str(new_volume_number).zfill(3) + " - " + volume_title + "/"
    else:
        new_volume_path = mc.MANGA_PATH + manga + mc.VOLUMES_SUBPATH + manga + " Volume " + str(new_volume_number).zfill(2) + " - " + volume_title + "/"
    #Preview Rename
    preview_type = os.getenv("PREVIEW_TYPE", "SIMPLE")
    chapter_count = int(last_chapter_of_new_volume) - first_chapter_in_volume + 1
    released_chapters = Files(mc.MANGA_PATH + manga + mc.NEW_CHAPTERS_SUBPATH)
    preview_changes = []
    for volume_chapter in range(0, chapter_count):
        if preview_type == "SIMPLE":
            preview_changes.append("Rename: " + released_chapters.filenames[volume_chapter] + "/ to " + manga + " Volume " + str(new_volume_number).zfill(3) + " - " + volume_title + "/")
        elif preview_type == "DETAILED":
            preview_changes.append("Rename: " + released_chapters.path + released_chapters.filenames[volume_chapter] + "/ to " + new_volume_path)
    del released_chapters
    return preview_changes

def manual_single_chapter_preview(manga, chapter_number, chapter_title):
    chapter_pages = Files(mc.SOURCE_PATH)
    chapter_pages.pad_zero("Preview")
    dest_path = mc.DESTINATION_PATH + str(chapter_number).zfill(3) + "/"
    #Preview Rename
    preview_type = os.getenv("PREVIEW_TYPE", "SIMPLE")
    preview_changes = []
    for page in range(0, chapter_pages.count):
        if preview_type == "SIMPLE":
            preview_changes.append("Rename: " + chapter_pages.filenames[page] + " to " + manga + " - CH" + str(chapter_number).zfill(3) + "PG" + str(page + 1).zfill(2) + " - " + chapter_title + chapter_pages.ext(page))
        elif preview_type == "DETAILED":
            preview_changes.append("Rename: " + chapter_pages.path + chapter_pages.filenames[page] + " to " + dest_path + manga + " - CH" + str(chapter_number).zfill(3) + "PG" + str(page + 1).zfill(2) + " - " + chapter_title + chapter_pages.ext(page))
    del chapter_pages
    return preview_changes

def manual_multiple_chapter_preview(manga):
    #Chapter directory must be formatted like
    #/NUMBER - TITLE/
    src_chapters = Files(mc.SOURCE_PATH)
    #Preview Rename
    preview_type = os.getenv("PREVIEW_TYPE", "SIMPLE")
    preview_changes = []
    for chapter in range(0, src_chapters.count):
        current_src_chapter = Files(src_chapters.path + src_chapters.filenames[chapter] + "/")
        current_src_chapter.pad_zero("Preview")
        number_title = src_chapters.filenames[chapter].split(" - ")
        current_chapter_number = number_title[0]
        current_chapter_title = number_title[1]
        dest_path = mc.DESTINATION_PATH + str(current_chapter_number).zfill(3) + "/"
        for page in range(0, current_src_chapter.count):
            if preview_type == "SIMPLE":
                preview_changes.append("Rename: " + current_src_chapter.filenames[page] + " to " + manga + " - CH" + str(current_chapter_number).zfill(3) + "PG" + str(page + 1).zfill(2) + " - " + current_chapter_title + current_src_chapter.ext(page))
            elif preview_type == "DETAILED":
                preview_changes.append("Rename: " + current_src_chapter.path + current_src_chapter.filenames[page] + " to " + dest_path + manga + " - CH" + str(current_chapter_number).zfill(3) + "PG" + str(page + 1).zfill(2) + " - " + current_chapter_title + current_src_chapter.ext(page))
    del src_chapters, current_src_chapter
    return preview_changes

def manual_volume_preview(manga, volume_number, volume_title):
    src_chapters = Files(mc.SOURCE_PATH)
    dest_dir = mc.DESTINATION_PATH + manga + " Volume " + str(volume_number).zfill(2) + " - " + volume_title + "/"
    #Preview Rename
    preview_type = os.getenv("PREVIEW_TYPE", "SIMPLE")
    preview_changes = []
    for chapter in range (0, src_chapters.count):
        if preview_type == "SIMPLE":
            preview_changes.append("Rename: " + src_chapters.filenames[chapter] + "/ to " + manga + " Volume " + str(volume_number).zfill(2) + " - " + volume_title + "/")
        elif preview_type == "DETAILED":
            preview_changes.append("Rename: " + src_chapters.path + src_chapters.filenames[chapter] + "/ to " + dest_dir)
    del src_chapters    
    return preview_changes
