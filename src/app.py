# app.py
from msilib.schema import Directory
from turtle import title
from flask import Flask, render_template, request, redirect, session
import os

# import manga
# import epub
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
        session.pop("scans", None)
        session.pop("build_toc", None)
        session.pop("preview", None)
        session.pop("error", None)
        return render_template('index.html')
    else:
        main_menu = request.form["main_menu"]
        if(main_menu == "Auto"):
            return redirect('/auto')
        elif(main_menu == "Manual"):
            return redirect('/manual')
        elif(main_menu == "EPUB"):
            return redirect('/epub')
        elif(main_menu == "New"):
            # TODO: New Manga Feature
            return redirect('/')
        elif(main_menu =="Main Menu"):
            return redirect('/')
            # TODO: Settings options
        elif(main_menu =="Settings"):
            return redirect('/')
        else:
            return redirect('/')

@app.route('/auto', methods = ['GET', 'POST'])
def auto_format():
    if(request.method == 'GET'):
        manga_chapter_title, manga_chapter_status = manga.get_chapter_status()
        manga_volume_title, manga_volume_status = manga.get_volume_status()
        return render_template('auto_format.html', manga_chapter_title = manga_chapter_title, manga_chapter_status = manga_chapter_status, manga_volume_title = manga_volume_title, manga_volume_status = manga_volume_status, len = len(manga_chapter_status))
    else:
        format_type = request.form['auto_format']
        if(format_type == "Chapter"):
            return redirect('/auto/chapter')
        elif(format_type == "Volume"):
            return redirect('/auto/volume')
        elif(format_type == "Main Menu"):
            return redirect('/')    
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
            session["error"] = "CHAPTER SELECTION ERROR"
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
            check = manga.check_auto_volume(manga_title, number, title)
            if(check == False):
                session["error"] =  manga.error_read()
                return redirect('/error')
            session["preview"] = manga.auto_volume_preview(manga_title, number, title)
            return redirect('/preview')
        else:
            session["error"] = "VOLUME SELECTION ERROR"
            return redirect('/error')    

@app.route('/manual', methods = ['GET', 'POST'])
def manual_format():
    if(request.method == 'GET'):
        return render_template('manual_format.html')
    else:
        format_type = request.form['manual_format']
        if(format_type == "Single Chapter"):
            return redirect('/manual/single')
        if(format_type == "Multi Chapter"):
            return redirect('/manual/multi') 
        elif(format_type == "Volume"):
            return redirect('/manual/volume')
        elif(format_type == "Main Menu"):
            return redirect('/')
        else:
            session["error"] = "AUTO FORMAT SELECTION ERROR"
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
            check = manga.check_manual_single_chapter(manga_title, number, title)
            if(check == False):
                session["error"] =  manga.error_read()
                return redirect('/error')
            session["preview"] = manga.manual_single_chapter_preview(manga_title, number, title)
            return redirect('/preview')
        else:
            session["error"] = "MANUAL CHAPTER SELECTION ERROR"
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
            check = manga.check_manual_multiple_chapter(manga_title)
            if(check == False):
                session["error"] =  manga.error_read()
                return redirect('/error')
            session["preview"] = manga.manual_multiple_chapter_preview(manga_title)
            return redirect('/preview')
        else:
            session["error"] = "MANUAL CHAPTER SELECTION ERROR"
            return redirect('/error')

@app.route('/manual/volume', methods = ['GET', 'POST'])
def manual_volume():
    if(request.method == 'GET'):
        return render_template('manual_volume.html')
    else:
        submit = request.form['manual_volume']
        if(submit == "Main Menu"):
            return redirect('/')
        elif(submit == "Volume"):
            manga_title = request.form['manga']
            number = request.form['number']
            title = request.form['title']
            session["manga"] = manga_title
            session["number"] = number
            session["title"] = title
            session["format"] = "manual_volume"
            check = manga.check_manual_volume(manga_title, number, title)
            if(check == False):
                session["error"] =  manga.error_read()
                return redirect('/error')
            session["preview"] = manga.manual_volume_preview(manga_title, number, title)
            return redirect('/preview')
        else:
            session["error"] = "MANUAL VOLUME SELECTION ERROR"
            return redirect('/error')

@app.route('/epub', methods = ['GET', 'POST'])
def epub_option():
    if(request.method == 'GET'):
        return render_template('epub_option.html')
    else:
        submit = request.form['epub']
        if(submit == "Main Menu"):
            return redirect('/')
        elif(submit == "Auto"):
            return redirect('/epub/auto')
        elif(submit == "Manual"):
            return redirect('/epub/manual')
        else:
            return redirect('/')
        
@app.route('/epub/auto', methods = ['GET', 'POST'])
def epub_auto():
    if(request.method == 'GET'):
        # GET MANGA LIST
        manga_list = manga.get_manga()
        return render_template('epub_auto.html', manga_list = manga_list, len = len(manga_list))
    else:
        submit = request.form['epub_auto']
        if(submit == "Main Menu"):
            return redirect('/')
        elif(submit == "EPUB Auto"):
            manga_title = request.form['manga']
            volume_number = request.form['volume_number']
            scans = request.form['scans']
            # volume title
            volume_title = manga.get_manga_volume(manga_title, volume_number)
            if(manga_title == "One Piece"):
                epub_title = manga_title + " Volume " + str(volume_number).zfill(3) + " - " + volume_title
            else:
                epub_title = manga_title + " Volume " + str(volume_number).zfill(2) + " - " + volume_title
            # author
            author = manga.get_manga_author(manga_title)
            session["manga"] = manga_title
            session["title"] = epub_title
            session["author"] = author
            session["scans"] = scans
            session["format"] = "epub_auto"
            preview = []
            preview.append("Manga: " + manga_title)
            preview.append("Author: " + author)
            preview.append("Volume: " + volume_number)
            preview.append("Title: " + manga_title)
            preview.append("EPUB: " + epub_title + ".epub")
            return redirect('/preview')
        else:
            session["error"] = "CHAPTER SELECTION ERROR"
            return redirect('/error')

@app.route('/epub/manual', methods = ['GET', 'POST'])
def epub_manual():
    if(request.method == 'GET'):
        return render_template('epub_manual.html')
    else:
        submit = request.form['epub_manual']
        if(submit == "Main Menu"):
            return redirect('/')
        elif(submit == "EPUB Manual"):
            manga_title = request.form['manga']
            title = request.form['title']
            number = request.form['number']
            author = request.form['author']
            scans = request.form['scans']
            if(request.form['build_toc'] == "Build"):
                build_toc = True
            else:
                build_toc = False
            epub_title = manga_title + " Volume " + str(number).zfill(2) + " - " + title
            session["title"] = epub_title
            session["author"] = author
            session["scans"] = scans
            session["buid_toc"] = build_toc
            session["format"] = "epub_manual"
            preview = []
            preview.append("Manga: " + manga_title)
            preview.append("Author: " + author)
            preview.append("Volume: " + number)
            preview.append("Title: " + title)
            preview.append("EPUB: " + epub_title + ".epub")
            return redirect('/preview')

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
        scans = ""
        build_toc = ""
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
        if "scans" in session:
            scans = session["scans"]
        if "buid_toc" in session:
            build_toc = session["build_toc"]
        commit = request.form['choice']
        if(commit == "Commit"):
            if(manga_format == "auto_chapter"):
                manga.auto_chapter_format(manga_title, title)
            elif(manga_format == "auto_volume"):
                manga.auto_volume_format(manga_title, number, title)
            elif(manga_format == "manual_single_chapter"):
                manga.manual_single_chapter_format(manga_title, number, title)
            elif(manga_format == "manual_multiple_chapter"):
                manga.manual_multiple_chapter_format(manga_title)
            elif(manga_format == "manual_volume"):
                manga.manual_volume_format(manga_title, number, title)
            elif(manga_format == "epub_auto"):
                epub_auto_src = manga.MANGA_PATH + manga_title + manga.VOLUMES_SUBPATH + title + "/"
                epub_auto_dest = manga.MANGA_PATH + manga_title + epub.EPUB_VOLUMES_SUBPATH
                epub.generate_epub(epub_auto_src, epub_auto_dest, title, author, scans)
            elif(manga_format == "epub_manual"):
                epub.generate_epub(manga.SOURCE_PATH, manga.DESTINATION_PATH, title, author, scans, build_toc)
            else:
                session["error"] = "MAJOR ERROR"
        elif(commit =="Abort"):
            return redirect('/')
        return redirect('/')

@app.route('/error', methods = ['GET', 'POST'])
def error():
    if(request.method == 'GET'):
        if "error" in session:
            error = session["error"]
        else:
            error = "UNKNOWN"
        return render_template('error.html', error = error)
    else:
        submit = request.form['error_action']
        if(submit == "Try Again"):
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
            if(manga_format == "auto_chapter"):
                check = manga.check_auto_chapter(manga_title, title)
                if(check == False):
                    error =  manga.error_read()
                    return render_template('error.html', error = error)
                session.modified = True
                session["preview"] = manga.auto_chapter_preview(manga_title, title)
                return redirect('/preview')
            elif(manga_format == "auto_volume"):
                check = manga.check_auto_volume(manga_title, number, title)
                if(check == False):
                    error =  manga.error_read()
                    return render_template('error.html', error = error)
                session.modified = True
                session["preview"] = manga.auto_volume_preview(manga_title, number, title)
                return redirect('/preview')
            elif(manga_format == "manual_single_chapter"):
                check = manga.check_manual_single_chapter(manga_title, number, title)
                if(check == False):
                    error =  manga.error_read()
                    return render_template('error.html', error = error)
                session.modified = True
                session["preview"] = manga.manual_single_chapter_preview(manga_title, number, title)
                return redirect('/preview')
            elif(manga_format == "manual_multiple_chapter"):
                check = manga.check_manual_multiple_chapter(manga_title)
                if(check == False):
                    error =  manga.error_read()
                    return render_template('error.html', error = error)
                session.modified = True
                session["preview"] = manga.manual_multiple_chapter_preview(manga_title)
                return redirect('/preview')
            elif(manga_format == "manual_volume"):
                check = manga.check_manual_volume(manga_title, number, title)
                if(check == False):
                    error =  manga.error_read()
                    return render_template('error.html', error = error)
                session.modified = True
                session["preview"] = manga.manual_volume_preview(manga_title, number, title)
                return redirect('/preview')
        else:
            return redirect('/')
