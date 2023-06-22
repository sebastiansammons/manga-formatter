# epub_config.py
import os


# Directory Paths:
EPUB_TEMPLATE_PATH = os.getenv("EPUB_TEMPLATE_PATH", "/manga/other/[epub_template]/")

EPUB_KOBO_TEMPLATE_PATH = os.getenv("EPUB_KOBO_TEMPLATE_PATH", "/manga/other/[epub_kobo_template]/")

# Sub Directory Paths:
TEMP_IMAGES_SUBPATH = os.getenv("TEMP_IMAGES_SUBPATH", "/OEBPS/temp_images/")
