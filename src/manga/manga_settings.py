# manga_setting.py
from . import manga_config as mc
from . import SQLite

def active_to_inactive(manga):
    manga_db = SQLite(mc.DB_FILE_PATH)
    manga_db.execute("UPDATE manga_details SET ACTIVE = 0 WHERE manga = ?;", (manga, ))
    manga_db.commit()
    manga_db.close()
    del manga_db

def inactive_to_active(manga):
    manga_db = SQLite(mc.DB_FILE_PATH)
    manga_db.execute("UPDATE manga_details SET ACTIVE = 1 WHERE manga = ?;", (manga, ))
    manga_db.commit()
    manga_db.close()
    del manga_db
