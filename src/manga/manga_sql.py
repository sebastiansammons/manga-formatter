# manga_sql.py
# import manga_config as mc
# import SQLite
from . import manga_config as mc
from . import SQLite

def get_active_manga():
    manga_db = SQLite(mc.DB_FILE_PATH)
    query_output = manga_db.execute("SELECT manga FROM manga_details WHERE ACTIVE = 1 ORDER BY manga ASC;")
    manga_db.close()
    if query_output == False:
        return "NOTHING"
    return query_output

def get_inactive_manga():
    manga_db = SQLite(mc.DB_FILE_PATH)
    query_output = manga_db.execute("SELECT manga FROM manga_details WHERE ACTIVE = 0 ORDER BY manga ASC;")
    manga_db.close()
    if query_output == False:
        return "NOTHING"
    return query_output

def get_chapter_status():
    manga_db = SQLite(mc.DB_FILE_PATH)
    query_output_manga = manga_db.execute("select manga_progress.manga from manga_progress LEFT JOIN manga_details ON  manga_progress.manga = manga_details.manga where ACTIVE = 1 ORDER BY manga_progress.manga ASC;")
    query_output_chapter = manga_db.execute("select current_chapter from manga_progress LEFT JOIN manga_details ON  manga_progress.manga = manga_details.manga where ACTIVE = 1 ORDER BY manga_progress.manga ASC;")
    manga_db.close()
    if query_output_manga == False or query_output_chapter == False:
        return "NOTHING"
    return query_output_manga, query_output_chapter

def get_volume_status():
    manga_db = SQLite(mc.DB_FILE_PATH)
    query_output_manga = manga_db.execute("select manga_progress.manga from manga_progress LEFT JOIN manga_details ON  manga_progress.manga = manga_details.manga where ACTIVE = 1 ORDER BY manga_progress.manga ASC;")
    query_output_volume = manga_db.execute("select current_volume from manga_progress LEFT JOIN manga_details ON  manga_progress.manga = manga_details.manga where ACTIVE = 1 ORDER BY manga_progress.manga ASC;")
    manga_db.close()
    if query_output_manga == False or query_output_volume == False:
        return "NOTHING"
    return query_output_manga, query_output_volume

def get_manga():
    manga_db = SQLite(mc.DB_FILE_PATH)
    query_output = manga_db.execute("SELECT manga FROM manga_details ORDER BY manga ASC;")
    manga_db.close()
    if query_output == False:
        return "NOTHING"
    return query_output

def get_manga_author(manga_title):
    manga_db = SQLite(mc.DB_FILE_PATH)
    query_output = manga_db.execute("SELECT writer FROM manga_details WHERE manga = ?", (manga_title, ))
    manga_db.close()
    if query_output == False:
        return "NOTHING"
    return query_output[0]

def get_volume_title(manga_title, volume):
    manga_db = SQLite(mc.DB_FILE_PATH)
    query_output = manga_db.execute("SELECT title FROM " + manga_title.replace(' ', '_') + "_volume WHERE volume = ?", (volume, ))
    manga_db.close()
    if query_output == False:
        return "NOTHING"
    return query_output[0]