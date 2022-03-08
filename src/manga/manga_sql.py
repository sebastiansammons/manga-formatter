# manga_sql.py
from . import manga_config as mc
from . import manga_error as me
from . import SQLite


def get_manga():
    manga_db = SQLite(mc.DB_FILE_PATH)
    query_output = manga_db.execute("SELECT manga FROM manga_details ORDER BY manga ASC;")
    manga_db.close()
    if query_output == False:
        return "NOTHING"
    return query_output

def get_active_manga():
    manga_db = SQLite(mc.DB_FILE_PATH)
    query_output = manga_db.execute("SELECT manga FROM manga_details WHERE ACTIVE = 1 ORDER BY manga ASC;")
    manga_db.close()
    del manga_db
    if query_output == False:
        return "NOTHING"
    return query_output

def get_inactive_manga():
    manga_db = SQLite(mc.DB_FILE_PATH)
    query_output = manga_db.execute("SELECT manga FROM manga_details WHERE ACTIVE = 0 ORDER BY manga ASC;")
    manga_db.close()
    del manga_db
    if query_output == False:
        return "NOTHING"
    return query_output

def get_chapter_status():
    manga_db = SQLite(mc.DB_FILE_PATH)
    query_output_manga = manga_db.execute("select manga_progress.manga from manga_progress LEFT JOIN manga_details ON  manga_progress.manga = manga_details.manga where ACTIVE = 1 ORDER BY manga_progress.manga ASC;")
    query_output_chapter = manga_db.execute("select current_chapter from manga_progress LEFT JOIN manga_details ON  manga_progress.manga = manga_details.manga where ACTIVE = 1 ORDER BY manga_progress.manga ASC;")
    manga_db.close()
    del manga_db
    if query_output_manga == False or query_output_chapter == False:
        return "NOTHING"
    return query_output_manga, query_output_chapter

def get_volume_status():
    manga_db = SQLite(mc.DB_FILE_PATH)
    query_output_manga = manga_db.execute("select manga_progress.manga from manga_progress LEFT JOIN manga_details ON  manga_progress.manga = manga_details.manga where ACTIVE = 1 ORDER BY manga_progress.manga ASC;")
    query_output_volume = manga_db.execute("select current_volume from manga_progress LEFT JOIN manga_details ON  manga_progress.manga = manga_details.manga where ACTIVE = 1 ORDER BY manga_progress.manga ASC;")
    manga_db.close()
    del manga_db
    if query_output_manga == False or query_output_volume == False:
        return "NOTHING"
    return query_output_manga, query_output_volume

def get_new_chapter_number(manga):
    manga_db = SQLite(mc.DB_FILE_PATH)
    query_input = (manga, )
    # Get current chapter number from SQLite and increment
    query_output = manga_db.execute("SELECT current_chapter FROM manga_progress WHERE manga = ?", query_input)
    new_chapter_number = query_output[0] + 1
    manga_db.close()
    del manga_db
    return new_chapter_number

def update_new_chapter(manga, new_chapter_number, chapter_title):
    manga_db = SQLite(mc.DB_FILE_PATH)
    manga_db.execute("UPDATE manga_progress SET current_chapter = ? WHERE manga = ?", (new_chapter_number, manga))
    manga_db.execute("INSERT INTO " + manga.replace(' ', '_') + "_chapter (manga, ch, title) VALUES(?, ?, ?)", (manga, new_chapter_number, chapter_title))
    manga_db.commit()
    manga_db.close()
    del manga_db

def get_new_volume_number(manga):
    manga_db = SQLite(mc.DB_FILE_PATH)
    query_input = (manga, )
    # Get current volume number from SQLite and increment
    query_output = manga_db.execute("SELECT current_volume FROM manga_progress WHERE manga = ?", query_input)
    new_volume_number = query_output[0] + 1
    # Get the first chapter in the new volume
    query_output = manga_db.execute("SELECT first_chapter_of_new_volume FROM manga_progress WHERE manga = ?", query_input)
    first_chapter_in_volume = query_output[0]
    manga_db.close()
    del manga_db
    return new_volume_number, first_chapter_in_volume

def update_new_volume(manga, new_volume_number, last_chapter_of_new_volume, volume_title):
    manga_db = SQLite(mc.DB_FILE_PATH)
    manga_db.execute("UPDATE manga_progress SET current_volume = ?, first_chapter_of_new_volume = ? WHERE manga = ?", (new_volume_number, int(last_chapter_of_new_volume) + 1, manga))
    manga_db.execute("INSERT INTO " + manga.replace(' ', '_') + "_volume (manga, volume, title) VALUES(?, ?, ?)", (manga, new_volume_number, volume_title))
    manga_db.commit()
    manga_db.close()
    del manga_db

def check_auto_chapter_sql(manga):
    manga_db = SQLite(mc.DB_FILE_PATH)
    query_input = (manga, )
    query_output = manga_db.execute("SELECT manga FROM manga_progress WHERE manga = ?", query_input)
    if(query_output == False):
        me.error_write("INVALID DB: " + manga + " ISN'T IN THE manga_progress TABLE")
        manga_db.close()
        del manga_db
        return False
    query_output = manga_db.execute("SELECT manga FROM " + manga.replace(' ', '_') + "_chapter;")
    if(query_output == False):
        me.error_write("INVALID DB: " + manga.replace(' ', '_') + "_chapter TABLE DOESN'T EXIST")
        manga_db.close()
        del manga_db
        return False
    return True

def check_auto_volume_sql(manga, last_chapter_of_new_volume):
    manga_db = SQLite(mc.DB_FILE_PATH)
    query_input = (manga, )
    query_output = manga_db.execute("SELECT manga FROM manga_progress WHERE manga = ?", query_input)
    if(query_output == False):
        me.error_write("INVALID DB: " + manga + " ISN'T IN THE manga_progress TABLE")
        manga_db.close()
        del manga_db
        return False
    query_output = manga_db.execute("SELECT manga FROM " + manga.replace(' ', '_') + "_volume;")
    if(query_output == False):
        me.error_write("INVALID DB: " + manga.replace(' ', '_') + "_volume TABLE DOESN'T EXIST")
        manga_db.close()
        del manga_db
        return False
    query_output = manga_db.execute("SELECT first_chapter_of_new_volume FROM manga_progress WHERE manga = ?", query_input)
    if(query_output[0] >= int(last_chapter_of_new_volume)):
        me.error_write("INVALID DB: LAST CHAPTER OF NEW VOLUME IS NOT GREATER THAN NEXT CHAPTER IN NEW VOLUME")
        manga_db.close()
        del manga_db
        return False
    return True
