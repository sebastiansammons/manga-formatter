# epub_config.py
import os


# Directory Paths:
MANGA_EPUB_PATH = os.getenv("MANGA_EPUB_PATH", "/manga/epub")
EPUB_TEMPLATE_PATH = os.getenv("EPUB_TEMPLATE_PATH", "/manga/staging/[epub_template]/")

# Sub Directory Paths:
TEMP_IMAGES_SUBPATH = os.getenv("TEMP_IMAGES_SUBPATH", "OEBPS/temp_images")
