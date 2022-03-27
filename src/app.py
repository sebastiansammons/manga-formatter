# app.py
from flask import Flask, render_template, request, redirect, session
import os

from . import manga
from . import epub


app = Flask(__name__)
app.secret_key = os.urandom(64)

@app.route('/', methods = ['GET', 'POST'])
def index():
    if(manga.check_manga_config() == False):
        session["error"] =  manga.error_read()
        return redirect('/error')
    if(request.method == 'GET'):
        session.pop("format", None)
        session.pop("manga", None)
        session.pop("number", None)
        session.pop("title", None)
        session.pop("author", None)
        session.pop("illustrator", None)
        session.pop("scans", None)
        session.pop("completed", None)
        session.pop("preview", None)
        session.pop("error", None)
        return render_template('index.html')
    else:
        submit = request.form["main_menu"]
        if(submit == "Main Menu"):
            return redirect('/')
        elif(submit == "Auto"):
            return redirect('/auto')
        elif(submit == "Manual"):
            return redirect('/manual')
        elif(submit == "EPUB"):
            return redirect('/epub')
        elif(submit == "New"):
            return redirect('/new')
        # TODO: Settings options
        elif(submit =="Settings"):
            return redirect('/settings')
        else:
            session["error"] = "MAIN MENU SELECTION ERROR"
            return redirect('/error')

@app.route('/settings', methods = ['GET', 'POST'])
def settings():
    if(request.method == 'GET'):
        active_manga = manga.get_active_manga()
        inactive_manga = manga.get_inactive_manga()
        return render_template('manga_settings.html', active_manga = active_manga, active_len = len(active_manga) inactive_manga = inactive_manga, inactive_len = len(inactive_manga))
    else:
        submit = request.form['settings']
        if(submit == "Main Menu"):
            return redirect('/')
        elif(submit == "INACTIVE"):
            manga_title = request.form['active_manga']
            manga.active_to_inactive(manga_title)
            return redirect('/')
        elif(submit == "ACTIVE"):
            manga_title = request.form['inactive_manga']
            manga.inactive_to_active(manga_title)
            return redirect('/')
        else:
            session["error"] = "AUTO FORMAT SELECTION ERROR"
@app.route('/auto', methods = ['GET', 'POST'])
def auto_format():
    if(request.method == 'GET'):
        manga_chapter_title, manga_chapter_status = manga.get_chapter_status()
        manga_volume_title, manga_volume_status = manga.get_volume_status()
        return render_template('auto_format.html', manga_chapter_title = manga_chapter_title, manga_chapter_status = manga_chapter_status, manga_volume_title = manga_volume_title, manga_volume_status = manga_volume_status, len = len(manga_chapter_status))
    else:
        submit = request.form['auto_format']
        if(submit == "Main Menu"):
            return redirect('/')
        elif(submit == "Chapter"):
            return redirect('/auto/chapter')
        elif(submit == "Volume"):
            return redirect('/auto/volume')
        else:
            session["error"] = "AUTO FORMAT SELECTION ERROR"
            return redirect('/error')

@app.route('/auto/chapter', methods = ['GET', 'POST'])
def auto_chapter():
    if(request.method == 'GET'):
        active_manga = manga.get_active_manga()
        return render_template('auto_chapter.html', active_manga = active_manga, len = len(active_manga))
    else:
        submit = request.form['auto_chapter']
        if(submit == "Main Menu"):
            return redirect('/')
        elif(submit == "Auto Chapter"):
            manga_title = request.form['manga']
            title = request.form['title']
            session["manga"] = manga_title
            session["title"] = title
            session["format"] = "auto_chapter"
            check = manga.check_auto_chapter(manga_title, title)
            if(check == False):
                session["error"] =  manga.error_read()
                return redirect('/error')
            session["preview"] = manga.auto_chapter_preview(manga_title, title)
            return redirect('/preview')
        else:
            session["error"] = "AUTO CHAPTER SELECTION ERROR"
            return redirect('/error')

@app.route('/auto/volume', methods = ['GET', 'POST'])
def auto_volume():
    if(request.method == 'GET'):
        active_manga = manga.get_active_manga()
        return render_template('auto_volume.html', active_manga = active_manga, len = len(active_manga))
    else:
        submit = request.form['auto_volume']
        if(submit == "Main Menu"):
            return redirect('/')
        elif(submit == "Auto Volume"):
            manga_title = request.form['manga']
            number = request.form['last_chapter_in_volume']
            title = request.form['title']
            session["manga"] = manga_title
            session["number"] = number
            session["title"] = title
            session["format"] = "auto_volume"
            check = manga.check_auto_volume(manga_title, number)
            if(check == False):
                session["error"] =  manga.error_read()
                return redirect('/error')
            session["preview"] = manga.auto_volume_preview(manga_title, number, title)
            return redirect('/preview')
        else:
            session["error"] = "AUTO VOLUME SELECTION ERROR"
            return redirect('/error')

@app.route('/manual', methods = ['GET', 'POST'])
def manual_format():
    if(request.method == 'GET'):
        return render_template('manual_format.html')
    else:
        submit = request.form['manual_format']
        if(submit == "Main Menu"):
            return redirect('/')
        elif(submit == "Single Chapter"):
            return redirect('/manual/single')
        elif(submit == "Multi Chapter"):
            return redirect('/manual/multi')
        elif(submit == "Volume"):
            return redirect('/manual/volume')
        else:
            session["error"] = "MANUAL FORMAT SELECTION ERROR"
            return redirect('/error')

@app.route('/manual/single', methods = ['GET', 'POST'])
def manual_single():
    if(request.method == 'GET'):
        return render_template('manual_single.html')
    else:
        submit = request.form['manual_single']
        if(submit == "Main Menu"):
            return redirect('/')
        elif(submit == "Single Chapter"):
            manga_title = request.form['manga']
            number = request.form['number']
            title = request.form['title']
            session["manga"] = manga_title
            session["number"] = number
            session["title"] = title
            session["format"] = "manual_single_chapter"
            check = manga.check_manual_single_chapter(manga.SOURCE_PATH, manga_title, number)
            if(check == False):
                session["error"] =  manga.error_read()
                return redirect('/error')
            session["preview"] = manga.manual_single_chapter_preview(manga.SOURCE_PATH, manga_title, number, title)
            return redirect('/preview')
        else:
            session["error"] = "MANUAL SINGLE CHAPTER SELECTION ERROR"
            return redirect('/error')

@app.route('/manual/multi', methods = ['GET', 'POST'])
def manual_multi():
    if(request.method == 'GET'):
        return render_template('manual_multi.html')
    else:
        submit = request.form['manual_multi']
        if(submit == "Main Menu"):
            return redirect('/')
        elif(submit == "Multi Chapter"):
            manga_title = request.form['manga']
            session["manga"] = manga_title
            session["format"] = "manual_multiple_chapter"
            check = manga.check_manual_multiple_chapter(manga.SOURCE_PATH, manga_title)
            if(check == False):
                session["error"] =  manga.error_read()
                return redirect('/error')
            session["preview"] = manga.manual_multiple_chapter_preview(manga.SOURCE_PATH, manga_title)
            return redirect('/preview')
        else:
            session["error"] = "MANUAL MULTI CHAPTER SELECTION ERROR"
            return redirect('/error')

@app.route('/manual/volume', methods = ['GET', 'POST'])
def manual_volume():
    if(request.method == 'GET'):
        return render_template('manual_volume.html')
    else:
        submit = request.form['manual_volume']
        if(submit == "Main Menu"):
            return redirect('/')
        elif(submit == "Manual Volume"):
            manga_title = request.form['manga']
            number = request.form['number']
            title = request.form['title']
            session["manga"] = manga_title
            session["number"] = number
            session["title"] = title
            session["format"] = "manual_volume"
            check = manga.check_manual_volume(manga.SOURCE_PATH, manga.DESTINATION_PATH, manga_title, number)
            if(check == False):
                session["error"] =  manga.error_read()
                return redirect('/error')
            session["preview"] = manga.manual_volume_preview(manga.SOURCE_PATH, manga_title, number, title)
            return redirect('/preview')
        else:
            session["error"] = "MANUAL VOLUME SELECTION ERROR"
            return redirect('/error')

@app.route('/epub', methods = ['GET', 'POST'])
def epub_build():
    if(request.method == 'GET'):
        # GET MANGA LIST
        manga_list = manga.get_manga()
        return render_template('epub.html', manga_list = manga_list, len = len(manga_list))
    else:
        submit = request.form['epub']
        if(submit == "Main Menu"):
            return redirect('/')
        elif(submit == "EPUB"):
            manga_title = request.form['manga']
            volume_number = request.form['volume_number']
            scans = request.form['scans']
            # volume title
            volume_title = manga.get_volume_title(manga_title, volume_number)
            if(volume_title == ""):
                epub_title = manga_title + " Volume " + str(volume_number).zfill(2)
            else:
                if "One Piece" in manga_title:
                    epub_title = manga_title + " Volume " + str(volume_number).zfill(3) + " - " + volume_title
                else:
                    epub_title = manga_title + " Volume " + str(volume_number).zfill(2) + " - " + volume_title
            # author
            author = manga.get_manga_author(manga_title)
            session["manga"] = manga_title
            session["title"] = epub_title
            session["author"] = author
            session["scans"] = scans
            session["format"] = "epub"
            preview = []
            preview.append("Manga: " + manga_title)
            preview.append("Title: " + volume_title)
            preview.append("Volume: " + volume_number)
            preview.append("Author: " + author)
            preview.append("Scans: " + scans)
            preview.append("EPUB: " + epub_title + ".epub")
            session["preview"] = preview
            return redirect('/preview')
        else:
            session["error"] = "EPUB SELECTION ERROR"
            return redirect('/error')

@app.route('/new', methods = ['GET', 'POST'])
def new_manga():
    if(request.method == 'GET'):
        return render_template('manga_new.html')
    else:
        submit = request.form['new_manga']
        if(submit == "Main Menu"):
            return redirect('/')
        elif(submit == "New Manga"):
            manga_title = request.form['manga']
            author = request.form['author']
            illustrator = request.form['illustrator']
            if "completed" in request.form:
                completed = True
            else:
                completed = False
            session["manga"] = manga_title
            session["author"] = author
            session["illustrator"] = illustrator
            session["completed"] = completed
            session["format"] = "new_manga"
            check = manga.new_manga_check(manga_title, author, illustrator)
            if(check == False):
                session["error"] =  manga.error_read()
                return redirect('/error')
            preview = []
            preview.append("Manga: " + manga_title)
            preview.append("Author: " + author)
            preview.append("Illustrator: " + illustrator)
            if(completed == True):
                preview.append("Completed Manga: YES")
            else:
                preview.append("Completed Manga: NO")
            session["preview"] = preview
            return redirect('/preview')
        else:
            session["error"] = "NEW MANGA SELECTION ERROR"
            return redirect('/error')

@app.route('/preview', methods = ['GET', 'POST'])
def preview():
    if(request.method == 'GET'):
        if "preview" in session:
            preview = session["preview"]
        else:
            preview = ["NO PREVIEW"]
        return render_template('preview.html', preview = preview, len = len(preview))
    else:
        manga_format = ""
        manga_title = ""
        number = ""
        title = ""
        author = ""
        illustrator = ""
        scans = ""
        completed = True
        if "format" in session:
            manga_format = session["format"]
        if "manga" in session:
            manga_title = session["manga"]
        if "number" in session:
            number = session["number"]
        if "title" in session:
            title = session["title"]
        if "author" in session:
            author = session["author"]
        if "illustrator" in session:
            illustrator = session["illustrator"]    
        if "scans" in session:
            scans = session["scans"]
        if "completed" in session:
            completed = session["completed"]    
        submit = request.form['commit']
        if(submit == "Main Menu"):
            return redirect('/')
        elif(submit == "Commit"):
            if(manga_format == "auto_chapter"):
                manga.auto_chapter_format(manga_title, title)
                return redirect('/auto')
            elif(manga_format == "auto_volume"):
                manga.auto_volume_format(manga_title, number, title)
                return redirect('/auto')
            elif(manga_format == "manual_single_chapter"):
                manga.manual_single_chapter_format(manga.SOURCE_PATH, manga.DESTINATION_PATH, manga_title, number, title)
                return redirect('/manual')
            elif(manga_format == "manual_multiple_chapter"):
                manga.manual_multiple_chapter_format(manga.SOURCE_PATH, manga.DESTINATION_PATH, manga_title)
                return redirect('/manual')
            elif(manga_format == "manual_volume"):
                manga.manual_volume_format(manga.SOURCE_PATH, manga.DESTINATION_PATH, manga_title, number, title)
                return redirect('/manual')
            elif(manga_format == "epub"):
                epub_src = manga.MANGA_PATH + manga_title + manga.VOLUMES_SUBPATH + title + "/"
                epub_dest = manga.MANGA_PATH + manga_title + manga.EPUB_VOLUMES_SUBPATH
                epub.generate_epub(epub_src, epub_dest, title, author, scans)
                return redirect('/epub')
            elif(manga_format == "new_manga"):
                manga.add_new_manga(manga_title, author, illustrator, completed)
                return redirect('/')
            else:
                session["error"] = "NOTHING TO COMMIT"
                return redirect('/error')
        else:
            session["error"] = "PREVIEW SELECTION ERROR"
            return redirect('/error')

@app.route('/error', methods = ['GET', 'POST'])
def error():
    if(request.method == 'GET'):
        if "error" in session:
            error = session["error"]
        else:
            error = "NO KNOWN ERROR"
        return render_template('error.html', error = error)
    else:
        submit = request.form['error_action']
        if(submit == "Main Menu"):
            return redirect('/')
        elif(submit == "Try Again"):
            if "format" in session:
                manga_format = session["format"]
            else:
                manga_format = ""
            if "manga" in session:
                manga_title = session["manga"]
            else:
                manga_title = ""
            if "number" in session:
                number = session["number"]
            else:
                number = ""
            if "title" in session:
                title = session["title"]
            else:
                title = ""
            if "author" in session:
                author = session["author"]
            else:
                author = ""
            if "illustrator" in session:
                illustrator = session["illustrator"]
            else:
                illustrator = ""
            if "completed" in session:
                completed = session["completed"]
            else:
                completed = ""    
            if(manga_format == "auto_chapter"):
                check = manga.check_auto_chapter(manga_title, title)
                if(check == False):
                    error =  manga.error_read()
                    return render_template('error.html', error = error)
                session.modified = True
                session["preview"] = manga.auto_chapter_preview(manga_title, title)
                return redirect('/preview')
            elif(manga_format == "auto_volume"):
                check = manga.check_auto_volume(manga_title, number)
                if(check == False):
                    error =  manga.error_read()
                    return render_template('error.html', error = error)
                session.modified = True
                session["preview"] = manga.auto_volume_preview(manga_title, number, title)
                return redirect('/preview')
            elif(manga_format == "manual_single_chapter"):
                check = manga.check_manual_single_chapter(manga.SOURCE_PATH, manga_title, number)
                if(check == False):
                    error =  manga.error_read()
                    return render_template('error.html', error = error)
                session.modified = True
                session["preview"] = manga.manual_single_chapter_preview(manga.SOURCE_PATH, manga_title, number, title)
                return redirect('/preview')
            elif(manga_format == "manual_multiple_chapter"):
                check = manga.check_manual_multiple_chapter(manga.SOURCE_PATH, manga_title)
                if(check == False):
                    error =  manga.error_read()
                    return render_template('error.html', error = error)
                session.modified = True
                session["preview"] = manga.manual_multiple_chapter_preview(manga.SOURCE_PATH, manga_title)
                return redirect('/preview')
            elif(manga_format == "manual_volume"):
                check = manga.check_manual_volume(manga.SOURCE_PATH, manga.DESTINATION_PATH, manga_title, number)
                if(check == False):
                    error =  manga.error_read()
                    return render_template('error.html', error = error)
                session.modified = True
                session["preview"] = manga.manual_volume_preview(manga.SOURCE_PATH, manga_title, number, title)
                return redirect('/preview')
            elif(manga_format == "new_manga"):
                check = manga.new_manga_check(manga_title, author, illustrator)
                if(check == False):
                    error =  manga.error_read()
                    return render_template('error.html', error = error)
                session.modified = True
                preview = []
                preview.append("Manga: " + manga_title)
                preview.append("Author: " + author)
                preview.append("Illustrator: " + illustrator)
                if(completed == True):
                    preview.append("Completed Manga: YES")
                else:
                    preview.append("Completed Manga: NO")
                session["preview"] = preview
                return redirect('/preview')
            else:
                session["error"] = "TRY AGAIN FAILED"
                return redirect('/error')
        else:
            session["error"] = "ERROR SELECTION ERROR"
            return redirect('/error')
