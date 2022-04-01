Manga Filename Formatting tool (README.md updated as of 04/01/2022)

Intro
This tool renames a manga chapter(a list of images) from a source directory and puts the chapter into a specific naming convention and file structure. The tool can also create a volume (list of chapters) and gather them into a singe directory to easily make volumes(in epub format). "Auto" formats are meant to update ongoing manga as well as record the chapter/volume title and chapter number. "Auto" formats are the main purpose for this tool so I could automate a weekly task. "Manual" Formats are meant for one off chapters, batch of chapters, or a volume. Usually for when I mess up an "Auto" format.

The naming conventions are:
    (title is optional)
    A page(image file):                     [manga] - CH[###]PG[##] - [title]
    A Volume(book) cover(image file):       [manga] Volume [##] - [title]

I use this naming convention to create directoriess filled with chapter pages(image files) that are sorted to mirror a book. Then use "EPUB" to create a epub document for the volume in the correct right-to-left direction. "New" will format a pre-sorted directory to format a whole manga at once. If the manga is still ongoing it will be added to the sql manga_progress table. 
"New" Format Needed:

SOURCE_PATH
         -> Volume 01 Directory
            Naming convention:
            [Vol##] - [title (optional)]/
                                       -> Chapter 01 DIR
                                          Naming convention:
                                          [CH##] - [title (optional)]/
                                                                    -> [pages in correct order]
                                                     *
                                                     *
                                          [CH##] - [title (optional)]/
                        *
                        *
            [Vol##] - [title (optional)]/
                  



The tool is written in python, uses SQlite for it's database and uses the flask framework to create the webUI. This was designed to run in a docker container on my debian home server. I have no plans of creating a GUI or command line version right now.

Installing

Docker-Compose Set-Up (docker-compose.yml):
Example from my debian server docker-compose file
version: '3'
services:
  manga_format:
    image: imthefridge/manga-format
    container_name: manga-format
    ports:
      - "5000:5000"
    restart: always
    volumes:
      - /etc/localtime:/etc/localtime:ro
      - <path to /manga>:/manga
      - <path to /appdata>:/appdata
    environment:
      - PUID=<PUID>
      - PGID=<PGID>
      # Optional Environment Variables. (I recommend the default's in _config.py)
      
      # DirectoryPaths
      # manga_config.py
      - MANGA_PATH=<path to MANGA_PATH>
      - SOURCE_PATH=<path to SOURCE_PATH>
      - DESTINATION_PATH=<path to DESTINATION_PATH>
      - ERROR_PATH=<path to ERROR_PATH>
      - DB_FILE_PATH=<path to DB_FILE_PATH>
      # epub_config.py
      - EPUB_TEMPLATE_PATH=<path to EPUB_TEMPLATE_PATH> (look in tests/data/container/[epub_template])
      
      # SubDirectoryPaths
      # Note: These are the subdirectories for the title's directory. 
      #       I recommend using the default in _config.py
      # manga_config.py
      - NEW_CHAPTERS_SUBPATH = <path to NEW_CHAPTERS_SUBPATH>
      - VOLUMES_SUBPATH = <path to VOLUMES_SUBPATH>
      - EPUB_VOLUMES_SUBPATH=<path to EPUB_VOLUMES_SUBPATH>
      - OP_COVER_SUBPATH = <path to OP_COVER_SUBPATH>
      # epub_config.py
      - TEMP_IMAGES_SUBPATH=<path to TEMP_IMAGES_SUBPATH>
