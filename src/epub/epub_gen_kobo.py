# epub_gen.py
import os
import shutil
import uuid
import datetime
from zipfile import ZipFile
from natsort import natsorted

import PIL.Image

from . import epub_config as ec
from . import template_kobo_css
from . import template_kobo_opf
from . import template_kobo_xhtml_page
from . import template_kobo_xhtml_toc
from . import template_kobo_toc_ncx
# from . import template_kobo_css
# from . import template_kobo_opf
# from . import template_kobo_xhtml_page
# from . import template_kobo_xhtml_toc


def generate_epub_kobo(src_path, dest_path, title, author, scans):
    temp_path = dest_path + "/temp/"
    temp_images = temp_path + ec.TEMP_IMAGES_SUBPATH
    copy_template(ec.EPUB_KOBO_TEMPLATE_PATH, temp_path)
    split_images(src_path, temp_images)
    # Scans or Digital Source
    if "Scans" in scans:
        check_spread(temp_images)
    max_height, max_width, page_id, opf_manifest_image, opf_manifest_xhtml, opf_spine, toc, ncx, xhtml_pages = build_template(temp_images, temp_path)
    build_xhtml_pages(page_id, xhtml_pages, max_height, max_width, temp_path)
    build_toc_xhtml(page_id, toc, temp_path)
    build_opf(opf_manifest_xhtml, opf_manifest_image, opf_spine, title, author, temp_path)
    build_css(max_height, max_width, temp_path)
    build_epub(dest_path, title, temp_path)
    remove_epub_temp(temp_path)

def copy_template(template_kobo_path, temp_path):
    try:
        # remove temp if it already exists
        if(os.path.isdir(temp_path)):
            shutil.rmtree(temp_path)
        shutil.copytree(template_kobo_path, temp_path)
        shutil.chown(temp_path, user = int(os.getenv("PUID")), group = int(os.getenv("PGID")))
    except PermissionError:
        pass

def split_images(src_path, dest_path):
    src_images = natsorted([f for f in os.listdir(src_path) if not f.startswith('.')])
    for page in src_images:
        tmp_image = PIL.Image.open(src_path + page)
        width, height = tmp_image.size
        if(width > height):
            # double spread found
            # crop images in half
            right_crop = (width / 2, 0, width, height)
            left_crop = (0, 0, width / 2, height)
            right_page = tmp_image.crop(right_crop)
            left_page = tmp_image.crop(left_crop)
            # save new pages/files to dest_path
            tmp_filename = page.split(" - ")
            if(len(tmp_filename) < 3):
                # CH##PG### will include the extension if there is no title, have to insert the _a/b before the extension
                right_page_filename = dest_path + tmp_filename[0] + " - " + tmp_filename[1][:9] + "_a" + tmp_filename[1][9:]
                left_page_filename = dest_path + tmp_filename[0] + " - " + tmp_filename[1][:9] + "_b" + tmp_filename[1][9:]
            else:
                right_page_filename = dest_path + tmp_filename[0] + " - " + tmp_filename[1] + "_a" + " - " + tmp_filename[2]
                left_page_filename = dest_path + tmp_filename[0] + " - " + tmp_filename[1] + "_b" + " - " + tmp_filename[2]
            right_page.save(right_page_filename)
            left_page.save(left_page_filename)
            try:
                shutil.chown(right_page_filename, user = int(os.getenv("PUID")), group = int(os.getenv("PGID")))
                shutil.chown(left_page_filename, user = int(os.getenv("PUID")), group = int(os.getenv("PGID")))
            except:
                pass
            right_page.close()
            left_page.close()
        else:
            try:
                shutil.copy(src_path + page, dest_path + page)
                shutil.chown(dest_path + page, user = int(os.getenv("PUID")), group = int(os.getenv("PGID")))
            except PermissionError:
                pass
        tmp_image.close()

def check_spread(src_path):
    src_images = natsorted([f for f in os.listdir(src_path) if not f.startswith('.')])
    image_count = len(src_images)
    # will always start on the left side in apple books (rtl reading)
    page_side = "left"
    # ignore the cover
    for page in range(1, image_count):
        if(page_side == "right"):
            if(src_images[page].rfind("PG01") != -1):
                # first page on right (bad most of the time)
                if(src_images[page].rfind("PG01_a") != -1):
                    # first page is double spread so it should start on the right
                    page_side = "left"
                    pass
                else:
                    # create blank page named to PG00 so it starts at the beginning
                    page_filename = src_images[page]
                    tmp_parse = page_filename.split(" - ")
                    if(len(tmp_parse) < 3):
                        # tmp_parse[1][:6] + "00" + tmp_parse[1][9:] replaces PG## with PG00 while keeping extension
                        blank_page_filename = tmp_parse[0] + " - " + tmp_parse[1][:6] + "00" + tmp_parse[1][9:]
                    else:
                        # tmp_parse[1][:-2] + "00" replaces PG## with PG00
                        blank_page_filename = tmp_parse[0] + " - " + tmp_parse[1][:-2] + "00" + " - " + tmp_parse[2]
                    # create blank page
                    # same dimensions as PG01
                    tmp_image = PIL.Image.open(src_path + page_filename)
                    width, height = tmp_image.size
                    tmp_image.close()
                    blank = PIL.Image.new(mode = "RGB", size = (width, height), color = (255, 255, 255))
                    blank.save(src_path + blank_page_filename)
                    blank.close()
            else:
                # regular right page, move to left
                page_side = "left"
        else:
            # regular left page, move to right
            page_side = "right"

def build_template(src_path, dest_path):
    src_images = natsorted([f for f in os.listdir(src_path) if not f.startswith('.')])
    image_count = len(src_images)
    page_id = []
    opf_manifest_image = []
    opf_manifest_xhtml = []
    opf_spine = []
    toc = []
    ncx = []
    xhtml_pages = []
    max_height = 0
    max_width = 0
    page_spread = ""
    prev_page_spread = ""
    chapter_title = ""
    nav_count = 1
    for page in range(0, image_count):
        tmp_parse = src_images[page].split(" - ")
        tmp_ext = src_images[page][src_images[page].rfind('.'):]
        # Append Array for page_id
        # CH###PG##
        if(len(tmp_parse) > 2):
            page_id.append(tmp_parse[1])
            # chapter_title (with extension)
            chapter_title = tmp_parse[2]
            # Some volume cover filenames don't have titles, need to make sure there
        else:
            page_id.append(tmp_parse[1][:tmp_parse[1].rfind('.')])
            chapter_title = ""
        # dest filename (also reduce filename length)
        dest_image = page_id[page] + tmp_ext
        # copy image/page
        try:
            shutil.copy(src_path + src_images[page], dest_path + "/OEBPS/images/" + dest_image)
            shutil.chown(dest_path + "/OEBPS/images/" + dest_image, user = int(os.getenv("PUID")), group = int(os.getenv("PGID")))
        except PermissionError:
            pass
        # Get width and height
        tmp_image = PIL.Image.open(src_path + src_images[page])
        width, height = tmp_image.size
        tmp_image.close()
        if(page == 0):
            # Cover
            max_height = height
            max_width = width
            page_spread = "right"
            prev_page_spread = "right"
            # Append Array for opf_manifest_image
            opf_manifest_image.append(generate_manifest_image(page_id[page], dest_image, get_mediatype(tmp_ext)))
            
            # Append Array for opf_manifest_xhtml
            opf_manifest_xhtml.append(generate_manifest_xhtml(page_id[page]))

            # Append Array for spine
            spine_cover = template_kobo_opf.spine_cover
            spine_cover = spine_cover.replace("[CH###PG##]", str(page_id))
            opf_spine.append(spine_cover)
        else:
            # check for max_height
            if(height > max_height):
                max_height = height
            # check for max_width
            if(width > max_width):
                max_width = width
            # next page spread
            page_spread = next_page_spread(prev_page_spread)
            prev_page_spread = page_spread

            # Append Array for opf_manifest_image
            opf_manifest_image.append(generate_manifest_image(page_id[page], dest_image, get_mediatype(tmp_ext)))

            # Append Array for opf_manifest_xhtml
            opf_manifest_xhtml.append(generate_manifest_xhtml(page_id[page]))

            # Append Array for spine
            opf_spine.append(generate_spine(page_id[page], page_spread))

            # Append Array for toc
            tmp_toc = generate_toc(page_id[page], chapter_title)
            if(tmp_toc != ""):
                toc.append(tmp_toc)

            # Append Array for ncx
            tmp_ncx, nav_count = generate_ncx(page_id[page], chapter_title, nav_count)
            if(tmp_ncx != ""):
                ncx.append(tmp_ncx)

        # Append Array for xhtml_pages
        xhtml_pages.append(generate_xhtml_pages(page_id[page], tmp_ext, page_spread))
    return max_height, max_width,  page_id, opf_manifest_image, opf_manifest_xhtml, opf_spine, toc, ncx, xhtml_pages

def generate_manifest_image(page_id, image, media_type):
    manifest_image = template_kobo_opf.manifest_image
    manifest_image = manifest_image.replace("[CH###PG##]", str(page_id))
    manifest_image = manifest_image.replace("[img_filename]", str(image))
    manifest_image = manifest_image.replace("[img_ext]", str(media_type))
    return manifest_image

def generate_manifest_xhtml(page_id):
    manifest_xhtml = template_kobo_opf.manifest_xhtml
    manifest_xhtml = manifest_xhtml.replace("[CH###PG##]", str(page_id))
    return manifest_xhtml

def generate_spine(page_id, page_spread):
    spine = template_kobo_opf.spine
    spine = spine.replace("[CH###PG##]", str(page_id))
    spine = spine.replace("[spread]", page_spread)
    return spine

def generate_toc(page_id, chapter_title):
    toc = template_kobo_xhtml_toc.toc
    # remove extension in title
    tmp_title = chapter_title[:chapter_title.rfind('.')]
    # toc for new chapters
    if "PG01" in page_id:
        # ignore rest of double spread if chapter starts with double spread
        if "PG01_b" in page_id:
            return ""
        else:
            toc = toc.replace("[CH###PG##]", str(page_id))
            # chapter number + remove leading 0s
            chapter_num = page_id[2:page_id.rfind("PG")]
            if(chapter_title == ""):
                toc = toc.replace("[chapter_title]", "Chapter " + str(chapter_num).lstrip("0"))
            else:
                toc = toc.replace("[chapter_title]", "Chapter " + str(chapter_num).lstrip("0") + ": " + tmp_title)
            return toc
    else:
        return ""

def generate_ncx(page_id, chapter_title, nav_count):
    nav = template_kobo_toc_ncx.nav_point
    # remove extension in title
    tmp_title = chapter_title[:chapter_title.rfind('.')]
    # toc for new chapters
    if "PG01" in page_id:
        # ignore rest of double spread if chapter starts with double spread
        if "PG01_b" in page_id:
            return ""
        else:
            nav = nav.replace("[CH###PG##]", str(page_id))
            nav = nav.replace("[COUNT]", str(nav_count))
            # chapter number + remove leading 0s
            chapter_num = page_id[2:page_id.rfind("PG")]
            if(chapter_title == ""):
                nav = nav.replace("[chapter_title]", "Chapter " + str(chapter_num).lstrip("0"))
            else:
                nav = nav.replace("[chapter_title]", "Chapter " + str(chapter_num).lstrip("0") + ": " + tmp_title)
            return nav, nav_count + 1
    else:
        return ""

def generate_xhtml_pages(page_id, ext, page_spread):
    xhtml_pages = template_kobo_xhtml_page.xhtml_pages
    xhtml_pages = xhtml_pages.replace("[CH###PG##]", str(page_id))
    xhtml_pages = xhtml_pages.replace("[ext]", ext)
    xhtml_pages = xhtml_pages.replace("[spread]", page_spread)
    return xhtml_pages

def build_xhtml_pages(page_id, xhtml_pages, max_height, max_width, dest_path):
    for page in range(0, len(page_id)):
        xhtml_page_string = ""
        xhtml_page_top = template_kobo_xhtml_page.top
        # viewport dimensions
        xhtml_page_top = xhtml_page_top.replace("[HEIGHT]", str(max_height))
        xhtml_page_top = xhtml_page_top.replace("[WIDTH]", str(max_width))
        xhtml_page_string = xhtml_page_top + xhtml_pages[page] + template_kobo_xhtml_page.bottom
        # xhtml title
        xhtml_page_string = xhtml_page_string.replace("[CH###PG##]", page_id[page])
        write_to_file(dest_path + "/OEBPS/xhtml/", page_id[page] + ".xhtml", xhtml_page_string)

def build_toc_xhtml(page_id, toc, dest_path):
    toc_xhtml = template_kobo_xhtml_toc.top
    toc_xhtml_bottom = template_kobo_xhtml_toc.bottom
    # toc
    for chapter in toc:
        toc_xhtml = toc_xhtml + template_kobo_xhtml_toc.nl + chapter
    # landmarks
    toc_xhtml_bottom = toc_xhtml_bottom.replace("[BODYMATTER]", page_id[1])
    toc_xhtml = toc_xhtml + toc_xhtml_bottom
    write_to_file(dest_path + "/OEBPS/", "toc.xhtml", toc_xhtml)

def build_toc_ncx(page_id, ncx, title, author, dest_path):
    toc_ncx = template_kobo_toc_ncx.top
    toc_ncx = toc_ncx.replace("[TITLE]", title)
    toc_ncx = toc_ncx.replace("[CREATOR]", author)
    toc_ncx_bottom = template_kobo_toc_ncx.bottom
    # nav
    for nav_point in ncx:
        toc_ncx = toc_ncx + template_kobo_toc_ncx.nl + nav_point
    toc_ncx = toc_ncx + toc_ncx_bottom
    write_to_file(dest_path + "/OEBPS/", "toc.ncx", toc_ncx)

def build_opf(opf_manifest_xhtml, opf_manifest_image, opf_spine, title, author, dest_path):
    opf = template_kobo_opf.top
    # uuid for unique ID
    gen_uuid = uuid.uuid4()
    # datetime for dcterms:modified
    time = datetime.datetime.now()
    time = time.strftime("%Y-%m-%dT%H:%M:%S")
    opf = opf.replace("[TITLE]", title)
    opf = opf.replace("[CREATOR]", author)
    opf = opf.replace("[UUID]", str(gen_uuid))
    opf = opf.replace("[DATETIME]", str(time))
    # manifest xhtml pages
    for page in range(0, len(opf_manifest_xhtml)):
        opf = opf + template_kobo_opf.nl + opf_manifest_xhtml[page]
    opf = opf + template_kobo_opf.mid_a
    # manifest image files
    for image in range(0, len(opf_manifest_image)):
        opf = opf + template_kobo_opf.nl + opf_manifest_image[image]
    opf = opf + template_kobo_opf.mid_b
    # spine
    for page in range(0, len(opf_spine)):
        opf = opf + template_kobo_opf.nl + opf_spine[page]
    opf = opf + template_kobo_opf.bottom
    write_to_file(dest_path + "/OEBPS/", "package.opf", opf)

def build_css(max_height, max_width, dest_path):
    css = template_kobo_css.stylesheet
    css = css.replace("[HEIGHT]", str(max_height))
    css = css.replace("[WIDTH]", str(max_width))
    write_to_file(dest_path + "/OEBPS/css/", "stylesheet.css", css)

def build_epub(dest_path, title, temp_path):
    epub_filename = dest_path + title + ".epub"
    try:
        zip = ZipFile(epub_filename, "x")
    except FileExistsError:
        # If one exists, override it
        os.remove(epub_filename)
        zip = ZipFile(epub_filename, "x")
    # zip mimetype
    zip.write(temp_path + "mimetype", "mimetype")
    # zip container.xml
    zip.write(temp_path + "META-INF/container.xml", "META-INF/container.xml")
    # zip com.kobobooks.display-options.xml
    zip.write(temp_path + "META-INF/com.kobobooks.display-options.xml", "META-INF/com.kobobooks.display-options.xml")
    # zip kobo.js
    zip.write(temp_path + "OEBPS/js/kobo.js", "OEBPS/js/kobo.js")
    # zip stylesheet.css
    zip.write(temp_path + "OEBPS/css/stylesheet.css", "OEBPS/css/stylesheet.css")
    # zip package.opf
    zip.write(temp_path + "OEBPS/package.opf", "OEBPS/package.opf")
    # zip toc.xhtml
    zip.write(temp_path + "OEBPS/toc.xhtml", "OEBPS/toc.xhtml")
    # zip toc.ncx
    zip.write(temp_path + "OEBPS/toc.ncx", "OEBPS/toc.ncx")
    # zip images
    image_src = natsorted([f for f in os.listdir(temp_path + "OEBPS/images/") if not f.startswith('.')])
    for i in range(0,len(image_src)):
        zip.write(temp_path + "OEBPS/images/" + image_src[i], "OEBPS/images/" + image_src[i])
    # zip xhtml
    xhtml_pages = natsorted([f for f in os.listdir(temp_path + "OEBPS/xhtml/") if not f.startswith('.')])
    for i in range(0,len(xhtml_pages)):
        zip.write(temp_path + "OEBPS/xhtml/" + xhtml_pages[i], "OEBPS/xhtml/" + xhtml_pages[i])
    # chown
    try:
        shutil.chown(epub_filename, user = int(os.getenv("PUID")), group = int(os.getenv("PGID")))
    except PermissionError:
        pass

def remove_epub_temp(temp_path):
    try:
        shutil.rmtree(temp_path)
    except PermissionError:
        pass

def write_to_file(dest_path, filename, contents):
    file = open(dest_path + filename, "w")
    file.write(contents)
    file.close()

def get_mediatype(ext):
    if ext == ".jpg" or ext == ".jpeg":
        return "jpeg"
    elif ext == ".png":
        return "png"
    else:
        return ext

def next_page_spread(prev_page_spread):
    if prev_page_spread == "left":
        return "right"
    else:
        return "left"
