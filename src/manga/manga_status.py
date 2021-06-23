# manga_status.py
# import logging
from . import manga_config as mc
from . import SQLite



def get_active_manga():
    manga_db = SQLite(mc.DB_FILE_PATH)
    query_output = manga_db.execute("SELECT manga FROM manga_details WHERE ACTIVE = 1 ORDER BY manga ASC;")
    if query_output == False:
        return "NOTHING"
    manga_option = []
    for i in range(0, len(query_output)):
        manga_option.append("<option value=" + query_output[i] + ">" + query_output[i] + "</option>")
    return manga_option

def get_chapter_status():
    manga_db = SQLite(mc.DB_FILE_PATH)
    query_output = manga_db.execute("select manga_progress.manga, current_chapter from manga_progress LEFT JOIN manga_details ON  manga_progress.manga = manga_details.manga where ACTIVE = 1 ORDER BY manga_progress.manga ASC;")
    if query_output == False:
        return "NOTHING"
    chapter_status = []
    for i in range(0, len(query_output)):
        print(query_output[i])
        chapter_status.append("<td class = ""manga_title"">" + query_output[i][0] + "</td><td class = ""manga_number"">" + query_output[i][1] + "</td>")
        print("<td class = ""manga_title"">" + query_output[i][0] + "</td><td class = ""manga_number"">" + query_output[i][1] + "</td>")
    return chapter_status

def get_volume_status():
    manga_db = SQLite(mc.DB_FILE_PATH)
    query_output = manga_db.execute("select manga_progress.manga, current_volume from manga_progress LEFT JOIN manga_details ON  manga_progress.manga = manga_details.manga where ACTIVE = 1 ORDER BY manga_progress.manga ASC;")
    if query_output == False:
        return "NOTHING"
    volume_status = []
    for i in range(0, len(query_output)):
        print(query_output[i])
        volume_status.append("<td class = ""manga_title"">" + query_output[i][0] + "</td><td class = ""manga_number"">" + query_output[i][1] + "</td>")
        print("<td class = ""manga_title"">" + query_output[i][0] + "</td><td class = ""manga_number"">" + query_output[i][1] + "</td>")
    return volume_status