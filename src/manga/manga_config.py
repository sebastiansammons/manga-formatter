# manga_config.py
import os


# Directory Paths:
MANGA_PATH = os.getenv("MANGA_PATH", "/manga/")
SOURCE_PATH = os.getenv("SOURCE_PATH", "/manga/other/[source]/")
DESTINATION_PATH = os.getenv("DESTINATION_PATH", "/manga/other/[destination]/")
NEW_MANGA_PATH = os.getenv("NEW_MANGA_PATH", "/manga/other/[new_manga]/")
ERROR_PATH = os.getenv("LOGS_PATH", "/appdata/error_msg/")
DB_FILE_PATH = os.getenv("DB_FILE_PATH", "/appdata/sqlite/fridge_manga.db")

# SubDirectory Paths:
NEW_CHAPTERS_SUBPATH = os.getenv("NEW_CHAPTERS_SUBPATH", "/Chapter Pages/Newly Released/")
VOLUMES_SUBPATH = os.getenv("VOLUMES_SUBPATH", "/Chapter Pages/Volumes/")
OP_COVER_SUBPATH = os.getenv("OP_COVER_SUBPATH", "/Cover Pages/")
