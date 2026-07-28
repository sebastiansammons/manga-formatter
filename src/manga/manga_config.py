# manga_config.py
import os


# directory paths:
MANGA_PAGE_PATH = os.getenv("MANGA_PAGE_PATH", "/manga/pages")
SOURCE_PATH = os.getenv("SOURCE_PATH", "/manga/staging/source")
DESTINATION_PATH = os.getenv("DESTINATION_PATH", "/manga/staging/destination")
ERROR_PATH = os.getenv("ERROR_PATH", "/appdata/error_msg")
DB_FILE_PATH = os.getenv("DB_FILE_PATH", "/appdata/sqlite/fridge_manga.db")

# sub-diractory paths:
CHAPTER_SUBPATH = os.getenv("CHAPTER_SUBPATH", "chapter")
VOLUME_SUBPATH = os.getenv("VOLUME_SUBPATH", "volume")
OP_COVER_SUBPATH = os.getenv("OP_COVER_SUBPATH", "cover")
