#manga_config.py
import os
#FolderPaths:
MANGA_PATH = os.getenv("MANGA_PATH", "/manga/")
SOURCE_PATH = os.getenv("SOURCE_PATH", "/manga/other/source/")
DESTINATION_PATH = os.getenv("DESTINATION_PATH", "/manga/other/destination/")
LOGS_PATH = os.getenv("LOGS_PATH", "/appdata/logs/")
DB_FILE_PATH = os.getenv("DB_FILE_PATH", "/appdata/sqlite/fridge_manga.db")

#SubFolderPaths:
NEW_CHAPTERS_SUBPATH = os.getenv("NEW_CHAPTERS_SUBPATH", "/Chapter Pages/Newly Released/")
VOLUMES_SUBPATH = os.getenv("VOLUMES_SUBPATH", "/Chapter Pages/Volumes/")
OP_COVER_SUBPATH = os.getenv("OP_COVER_SUBPATH", "/Cover Pages/")   