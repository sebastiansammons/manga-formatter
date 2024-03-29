# manga_format.py
from . import manga_config as mc
from . import manga_sql as msql
from . import Directory
from . import Files


def auto_chapter_format(manga, chapter_title, src_path = mc.SOURCE_PATH):
    chapter_pages = Files(src_path)
    chapter_pages.pad_zero()
    # Connect to SQLite and get appropriate data
    new_chapter_number = msql.get_new_chapter_number(manga)
    # Make copy of the chapter cover for One Piece
    if "One Piece" in manga:
        op_cover_filename = "CH" + str(new_chapter_number).zfill(4) + " Cover" + chapter_pages.ext()
        if(new_chapter_number < 501):
            op_cover_path = mc.MANGA_PATH + manga + mc.OP_COVER_SUBPATH + "1-500/"
        elif(new_chapter_number < 1001):
            op_cover_path = mc.MANGA_PATH + manga + mc.OP_COVER_SUBPATH + "501-1000/"
        else:
            op_cover_path = mc.MANGA_PATH + manga + mc.OP_COVER_SUBPATH + "1001-End/"
        chapter_pages.copyfile(op_cover_path, op_cover_filename, 0)
    # Create directory path for the new chapter
    if "One Piece" in manga:
        new_chapter_path = mc.MANGA_PATH + manga + mc.NEW_CHAPTERS_SUBPATH + str(new_chapter_number).zfill(4) + "/"
    else:
        new_chapter_path = mc.MANGA_PATH + manga + mc.NEW_CHAPTERS_SUBPATH + str(new_chapter_number).zfill(3) + "/"
    # Make new directory
    dest_path = Directory(new_chapter_path)
    dest_path.mk_dir()
    # Rename
    for page in range(0, chapter_pages.count):
        if "One Piece" in manga:
            chapter_pages.rename(dest_path.path, manga + " - CH" + str(new_chapter_number).zfill(4) + "PG" + str(page + 1).zfill(2) + " - " + chapter_title + chapter_pages.ext(page), page)
        else:
            chapter_pages.rename(dest_path.path, manga + " - CH" + str(new_chapter_number).zfill(3) + "PG" + str(page + 1).zfill(2) + " - " + chapter_title + chapter_pages.ext(page), page)
    del chapter_pages, dest_path
    # Update appropriate tables
    msql.update_new_chapter(manga, new_chapter_number, chapter_title)

def auto_chapter_batch_format(manga):
    src_chapters = Files(mc.SOURCE_PATH)
    for chapter in range(0, src_chapters.count):
        if(src_chapters.isfile(chapter)):
            pass
        else:
            current_src_chapter = Files(src_chapters.path + src_chapters.filenames[chapter] + "/")
            current_src_chapter.pad_zero()
            number_title = src_chapters.filenames[chapter].split(" - ")
            current_chapter_title = number_title[1]
            auto_chapter_format(manga, current_chapter_title, current_src_chapter.path)
            current_src_chapter.rm_dir()
    del src_chapters, current_src_chapter

def auto_volume_format(manga, last_chapter_of_new_volume, volume_title):
    # Connect to SQLite and get appropriate data
    new_volume_number, first_chapter_in_volume = msql.get_new_volume_number(manga)
    # Create new volume directory
    if(volume_title == ""):
        if "One Piece" in manga:
            new_volume_path = mc.MANGA_PATH + manga + mc.VOLUMES_SUBPATH + manga + " Volume " + str(new_volume_number).zfill(3) + "/"
        else:
            new_volume_path = mc.MANGA_PATH + manga + mc.VOLUMES_SUBPATH + manga + " Volume " + str(new_volume_number).zfill(2) + "/"
    else:
        if "One Piece" in manga:
            new_volume_path = mc.MANGA_PATH + manga + mc.VOLUMES_SUBPATH + manga + " Volume " + str(new_volume_number).zfill(3) + " - " + volume_title + "/"
        else:
            new_volume_path = mc.MANGA_PATH + manga + mc.VOLUMES_SUBPATH + manga + " Volume " + str(new_volume_number).zfill(2) + " - " + volume_title + "/"
    dest_path = Directory(new_volume_path)
    dest_path.mk_dir()
    # Rename volume cover
    volume_cover_page = Files(mc.SOURCE_PATH)
    if(volume_title == ""):
        if "One Piece" in manga:
            volume_cover_page.rename(dest_path.path, manga + " - " + str(new_volume_number).zfill(3) + volume_cover_page.ext())
        else:
            volume_cover_page.rename(dest_path.path, manga + " - " + str(new_volume_number).zfill(2) + volume_cover_page.ext())
    else:
        if "One Piece" in manga:
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
    msql.update_new_volume(manga, new_volume_number, last_chapter_of_new_volume, volume_title)

def manual_single_chapter_format(src_path, dest_path, manga, chapter_number, chapter_title):
    chapter_pages = Files(src_path)
    chapter_pages.pad_zero()
    chapter_path = Directory(dest_path + str(chapter_number).zfill(3) + "/")
    chapter_path.mk_dir()
    for page in range(0, chapter_pages.count):
        if(chapter_title == ""):
            if "One Piece" in manga:
                chapter_pages.rename(chapter_path.path, manga + " - CH" + str(chapter_number).zfill(4) + "PG" + str(page + 1).zfill(2) + chapter_pages.ext(page), page)
            else:
                chapter_pages.rename(chapter_path.path, manga + " - CH" + str(chapter_number).zfill(3) + "PG" + str(page + 1).zfill(2) + chapter_pages.ext(page), page)
        else:
            if "One Piece" in manga:
                chapter_pages.rename(chapter_path.path, manga + " - CH" + str(chapter_number).zfill(4) + "PG" + str(page + 1).zfill(2) + " - " + chapter_title + chapter_pages.ext(page), page)
            else:
                chapter_pages.rename(chapter_path.path, manga + " - CH" + str(chapter_number).zfill(3) + "PG" + str(page + 1).zfill(2) + " - " + chapter_title + chapter_pages.ext(page), page)
    del chapter_pages, chapter_path

def manual_multiple_chapter_format(src_path, dest_path, manga):
    src_chapters = Files(src_path)
    for chapter in range(0, src_chapters.count):
        if(src_chapters.isfile(chapter)):
            pass
        else:
            current_src_chapter = Files(src_chapters.path + src_chapters.filenames[chapter] + "/")
            current_src_chapter.pad_zero()
            number_title = src_chapters.filenames[chapter].split(" - ")
            current_chapter_number = number_title[0]
            chapter_path = Directory(dest_path + str(current_chapter_number).zfill(3) + "/")
            chapter_path.mk_dir()
            if(len(number_title) == 1):
                for page in range(0, current_src_chapter.count):
                    if "One Piece" in manga:
                        current_src_chapter.rename(chapter_path.path, manga + " - CH" + str(current_chapter_number).zfill(4) + "PG" + str(page + 1).zfill(2) + current_src_chapter.ext(page), page)
                    else:
                        current_src_chapter.rename(chapter_path.path, manga + " - CH" + str(current_chapter_number).zfill(3) + "PG" + str(page + 1).zfill(2) + current_src_chapter.ext(page), page)
            else:
                current_chapter_title = number_title[1]
                for page in range(0, current_src_chapter.count):
                    if "One Piece" in manga:
                        current_src_chapter.rename(chapter_path.path, manga + " - CH" + str(current_chapter_number).zfill(4) + "PG" + str(page + 1).zfill(2) + " - " + current_chapter_title + current_src_chapter.ext(page), page)
                    else:
                        current_src_chapter.rename(chapter_path.path, manga + " - CH" + str(current_chapter_number).zfill(3) + "PG" + str(page + 1).zfill(2) + " - " + current_chapter_title + current_src_chapter.ext(page), page)
            current_src_chapter.rm_dir()
    del src_chapters, current_src_chapter, chapter_path, number_title

def manual_volume_format(src_path, dest_path, manga, volume_number, volume_title):
    manual_multiple_chapter_format(src_path, dest_path, manga)
    # Create volume directory
    if(volume_title == ""):
        if "One Piece" in manga:
            volume_path = Directory(dest_path + manga + " Volume " + str(volume_number).zfill(3) + "/")
        else:
            volume_path = Directory(dest_path + manga + " Volume " + str(volume_number).zfill(2) + "/")
    else:
        if "One Piece" in manga:
            volume_path = Directory(dest_path + manga + " Volume " + str(volume_number).zfill(3) + " - " + volume_title + "/")
        else:
            volume_path = Directory(dest_path + manga + " Volume " + str(volume_number).zfill(2) + " - " + volume_title + "/")
    volume_path.mk_dir()
    # move formatted chapters in volume directory
    volume_chapters = Files(dest_path)
    for chapter in range (0, volume_chapters.count):
        current_vol_chapter = Files(volume_chapters.path + volume_chapters.filenames[chapter] + "/")
        for page in range(0, current_vol_chapter.count):
            current_vol_chapter.rename(volume_path.path, current_vol_chapter.filenames[page], page)
        current_vol_chapter.rm_dir()
    # If there is a file in source, rename to cover page
    volume_cover = Files(src_path)
    if(volume_cover.count == 1):
        if(volume_title == ""):
            if "One Piece" in manga:
                volume_cover.rename(volume_path.path, manga + " - " + str(volume_number).zfill(3) + volume_cover.ext())
            else:
                volume_cover.rename(volume_path.path, manga + " - " + str(volume_number).zfill(2) + volume_cover.ext())
        else:
            if "One Piece" in manga:
                volume_cover.rename(volume_path.path, manga + " - " + str(volume_number).zfill(3) + " - " + volume_title + volume_cover.ext())
            else:
                volume_cover.rename(volume_path.path, manga + " - " + str(volume_number).zfill(2) + " - " + volume_title + volume_cover.ext())
    del volume_chapters, volume_path, current_vol_chapter, volume_cover
