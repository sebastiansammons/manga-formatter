# manga_status.py
# import logging
from . import manga_config as mc
from . import SQLite



def get_active_manga():
    manga_db = SQLite(mc.DB_FILE_PATH)
    query_output = manga_db.execute("SELECT manga FROM manga_details WHERE ACTIVE = 1 ORDER BY manga ASC;")
    if query_output == False:
        return "NOTHING"
    return query_output

def get_chapter_status():
    manga_db = SQLite(mc.DB_FILE_PATH)
    query_output_manga = manga_db.execute("select manga_progress.manga from manga_progress LEFT JOIN manga_details ON  manga_progress.manga = manga_details.manga where ACTIVE = 1 ORDER BY manga_progress.manga ASC;")
    query_output_chapter = manga_db.execute("select current_chapter from manga_progress LEFT JOIN manga_details ON  manga_progress.manga = manga_details.manga where ACTIVE = 1 ORDER BY manga_progress.manga ASC;")
    if query_output_manga == False or query_output_chapter == False:
        return "NOTHING"
    return query_output_manga, query_output_chapter

def get_volume_status():
    manga_db = SQLite(mc.DB_FILE_PATH)
    query_output_manga = manga_db.execute("select manga_progress.manga from manga_progress LEFT JOIN manga_details ON  manga_progress.manga = manga_details.manga where ACTIVE = 1 ORDER BY manga_progress.manga ASC;")
    query_output_volume = manga_db.execute("select current_volume from manga_progress LEFT JOIN manga_details ON  manga_progress.manga = manga_details.manga where ACTIVE = 1 ORDER BY manga_progress.manga ASC;")
    if query_output_manga == False or query_output_volume == False:
        return "NOTHING"
    return query_output_manga, query_output_volume