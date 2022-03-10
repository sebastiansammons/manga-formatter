# manga_preview.py
import os

from . import manga_config as mc
from . import manga_sql as msql
from . import Files


def auto_chapter_preview(manga, chapter_title):
    chapter_pages = Files(mc.SOURCE_PATH)
    chapter_pages.pad_zero("Preview")
    new_chapter_number = msql.get_new_chapter_number(manga)
    # Directory path for the new chapter
    if(manga == "One Piece"):
        new_chapter_path = mc.MANGA_PATH + manga + mc.NEW_CHAPTERS_SUBPATH + str(new_chapter_number).zfill(4) + "/"
    else:
        new_chapter_path = mc.MANGA_PATH + manga + mc.NEW_CHAPTERS_SUBPATH + str(new_chapter_number).zfill(3) + "/"
    # Preview Rename
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
    new_volume_number, first_chapter_in_volume = msql.get_new_volume_number(manga)
    # Preview new volume directory
    if(manga == "One Piece"):
        new_volume_path = mc.MANGA_PATH + manga + mc.VOLUMES_SUBPATH + manga + " Volume " + str(new_volume_number).zfill(3) + " - " + volume_title + "/"
    else:
        new_volume_path = mc.MANGA_PATH + manga + mc.VOLUMES_SUBPATH + manga + " Volume " + str(new_volume_number).zfill(2) + " - " + volume_title + "/"
    # Preview Rename
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

def manual_single_chapter_preview(src_path, dest_path, manga, chapter_number, chapter_title):
    chapter_pages = Files(src_path)
    chapter_pages.pad_zero("Preview")
    chapter_path = dest_path + str(chapter_number).zfill(3) + "/"
    # Preview Rename
    preview_type = os.getenv("PREVIEW_TYPE", "SIMPLE")
    preview_changes = []
    for page in range(0, chapter_pages.count):
        if preview_type == "SIMPLE":
            preview_changes.append("Rename: " + chapter_pages.filenames[page] + " to " + manga + " - CH" + str(chapter_number).zfill(3) + "PG" + str(page + 1).zfill(2) + " - " + chapter_title + chapter_pages.ext(page))
        elif preview_type == "DETAILED":
            preview_changes.append("Rename: " + chapter_pages.path + chapter_pages.filenames[page] + " to " + chapter_path + manga + " - CH" + str(chapter_number).zfill(3) + "PG" + str(page + 1).zfill(2) + " - " + chapter_title + chapter_pages.ext(page))
    del chapter_pages
    return preview_changes

def manual_multiple_chapter_preview(src_path, dest_path, manga):
    # Chapter directory must be formatted like
    # /NUMBER - TITLE/ or /NUMBER/
    src_chapters = Files(src_path)
    # Preview Rename
    preview_type = os.getenv("PREVIEW_TYPE", "SIMPLE")
    preview_changes = []
    for chapter in range(0, src_chapters.count):
        if(src_chapters.isfile(chapter)):
            pass
        else:
            current_src_chapter = Files(src_chapters.path + src_chapters.filenames[chapter] + "/")
            current_src_chapter.pad_zero("Preview")
            number_title = src_chapters.filenames[chapter].split(" - ")
            current_chapter_number = number_title[0]
            chapter_path = dest_path + str(current_chapter_number).zfill(3) + "/"
            if(len(number_title) == 1):
                for page in range(0, current_src_chapter.count):
                    if preview_type == "SIMPLE":
                        preview_changes.append("Rename: " + current_src_chapter.filenames[page] + " to " + manga + " - CH" + str(current_chapter_number).zfill(3) + "PG" + str(page + 1).zfill(2) + current_src_chapter.ext(page))
                    elif preview_type == "DETAILED":
                        preview_changes.append("Rename: " + current_src_chapter.path + current_src_chapter.filenames[page] + " to " + chapter_path + manga + " - CH" + str(current_chapter_number).zfill(3) + "PG" + str(page + 1).zfill(2) + current_src_chapter.ext(page))
            else:
                current_chapter_title = number_title[1]
                for page in range(0, current_src_chapter.count):
                    if preview_type == "SIMPLE":
                        preview_changes.append("Rename: " + current_src_chapter.filenames[page] + " to " + manga + " - CH" + str(current_chapter_number).zfill(3) + "PG" + str(page + 1).zfill(2) + " - " + current_chapter_title + current_src_chapter.ext(page))
                    elif preview_type == "DETAILED":
                        preview_changes.append("Rename: " + current_src_chapter.path + current_src_chapter.filenames[page] + " to " + chapter_path + manga + " - CH" + str(current_chapter_number).zfill(3) + "PG" + str(page + 1).zfill(2) + " - " + current_chapter_title + current_src_chapter.ext(page))
    del src_chapters, current_src_chapter
    return preview_changes

def manual_volume_preview(src_path, dest_path, manga, volume_number, volume_title):
    src_chapters = Files(src_path)
    # Preview Rename
    preview_type = os.getenv("PREVIEW_TYPE", "SIMPLE")
    preview_changes = []
    if(volume_title == ""):
        volume_path = dest_path + manga + " Volume " + str(volume_number).zfill(2) + "/"
    else:
        volume_path = dest_path + manga + " Volume " + str(volume_number).zfill(2) + " - " + volume_title + "/"
    for chapter in range (0, src_chapters.count):
        if preview_type == "SIMPLE":
            if(volume_title == ""):
                preview_changes.append("Rename: /" + src_chapters.filenames[chapter] + " to " + manga + " Volume " + str(volume_number).zfill(2) + "/")
            else:
                preview_changes.append("Rename: /" + src_chapters.filenames[chapter] + " to " + manga + " Volume " + str(volume_number).zfill(2) + " - " + volume_title + "/")
        elif preview_type == "DETAILED":
            preview_changes.append("Rename: " + src_chapters.path + src_chapters.filenames[chapter] + "/ to " + volume_path)
    del src_chapters
    return preview_changes
