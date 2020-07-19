#app.py
from flask import Flask, render_template, request, redirect, session
import manga
import os


#
#Initialize Logger
#
manga.log_config()

manga.log_debug("app = Flask(__name__)")
app = Flask(__name__)

app.secret_key = os.urandom(64)

@app.route('/', methods = ['GET', 'POST'])
def index():
    manga.log_debug("index()")
    if(manga.check_manga_config() == False):
        session["error"] = manga.message_read()
        return redirect('/error')
    if(request.method == 'GET'):
        session.pop("format", None)
        session.pop("manga", None)
        session.pop("number", None)
        session.pop("title", None)
        session.pop("preview", None)
        session.pop("error", None)
        return render_template('index.html')
    else:
        manga_format = request.form["manga_format"]
        if(manga_format == "Auto"):
            return redirect('/auto')
        elif(manga_format == "Manual"):
            return redirect('/manual')
        elif(manga_format == "Full Manga"):
            return redirect('/full')

@app.route('/auto', methods = ['GET', 'POST'])
def auto_format():
    manga.log_debug("auto_format()")
    if(request.method == 'GET'):
        return render_template('auto_format.html')
    else:
        format_type = request.form['auto_format']
        if(format_type == "Chapter"):
            return redirect('/auto/chapter')
        elif(format_type == "Volume"):
            return redirect('/auto/volume')
        elif(format_type == "Main Menu"):
            return redirect('/')    
        else:
            manga.log_error("AUTO FORMAT SELECTION ERROR")
            session["error"] = "AUTO FORMAT SELECTION ERROR"
            return redirect('/error')

@app.route('/auto/chapter', methods = ['GET', 'POST'])
def auto_chapter():
    manga.log_debug("auto_chapter()")
    if(request.method == 'GET'):
        return render_template('auto_chapter.html')
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
            preview = manga.auto_chapter_preview(manga.get_manga(manga_title), title)
            if(preview == False):
                session["error"] = manga.message_read()
                return redirect('/error')
            session["preview"] = preview
            return redirect('/preview')
        else:
            manga.log_error("CHAPTER SELECTION ERROR")
            session["error"] = "CHAPTER SELECTION ERROR"
            return redirect('/error')

@app.route('/auto/volume', methods = ['GET', 'POST'])
def auto_volume():
    manga.log_debug("auto_volume()")
    if(request.method == 'GET'):
        return render_template('auto_volume.html')
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
            preview = manga.auto_volume_preview(manga.get_manga(manga_title), number, title)
            if(preview == False):
                session["error"] = manga.message_read()
                return redirect('/error')
            session["preview"] = preview
            return redirect('/preview')
        else:
            manga.log_error("VOLUME SELECTION ERROR")
            session["error"] = "VOLUME SELECTION ERROR"
            return redirect('/error')    

@app.route('/manual', methods = ['GET', 'POST'])
def manual_format():
    manga.log_debug("manual_format()")
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
            manga.log_error("AUTO FORMAT SELECTION ERROR")
            session["error"] = "AUTO FORMAT SELECTION ERROR"
            return redirect('/error')

@app.route('/manual/single', methods = ['GET', 'POST'])
def manual_single():
    manga.log_debug("manual_single()")
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
            preview = manga.manual_single_chapter_preview(manga_title, number, title)
            if(preview == False):
                session["error"] = manga.message_read()
                return redirect('/error')
            session["preview"] = preview
            return redirect('/preview')
        else:
            manga.log_error("MANUAL CHAPTER SELECTION ERROR")
            session["error"] = "MANUAL CHAPTER SELECTION ERROR"
            return redirect('/error')  

@app.route('/manual/multi', methods = ['GET', 'POST'])
def manual_multi():
    manga.log_debug("manual_multi()")
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
            preview = manga.manual_multiple_chapter_preview(manga_title)
            if(preview == False):
                session["error"] = manga.message_read()
                return redirect('/error')
            session["preview"] = preview
            return redirect('/preview')
        else:
            manga.log_error("MANUAL CHAPTER SELECTION ERROR")
            session["error"] = "MANUAL CHAPTER SELECTION ERROR"
            return redirect('/error')

@app.route('/manual/volume', methods = ['GET', 'POST'])
def manual_volume():
    manga.log_debug("manual_volume()")
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
            preview = manga.manual_volume_preview(manga_title, number, title)
            if(preview == False):
                session["error"] = manga.message_read()
                return redirect('/error')
            session["preview"] = preview
            return redirect('/preview')
        else:
            manga.log_error("MANUAL VOLUME SELECTION ERROR")
            session["error"] = "MANUAL VOLUME SELECTION ERROR"
            return redirect('/error')

@app.route('/full', methods = ['GET', 'POST'])
def full_format():
    manga.log_debug("full_format()")
    if(request.method == 'GET'):
        return render_template('full_manga.html')
    else:
        submit = request.form['full_format']
        if(submit == "Main Menu"):
            return redirect('/')
        elif(submit == "Full Manga Format"):
            manga_title = request.form['manga']
            if(manga_title == ""):
                manga.log_warning("EMPTY MANGA TITLE")
                session["error"] = "EMPTY MANGA TITLE"
                return redirect('/error')
            else:
                result = manga.full_manga(manga_title)
                if(result == False):
                    session["error"] = manga.message_read()
                    return redirect('/error')
                return redirect('/')
        else:
            manga.log_error("FULL MANGA SELECTION ERROR")
            session["error"] = "FULL MANGA SELECTION ERROR"
            return redirect('/error')

@app.route('/preview', methods = ['GET', 'POST'])
def preview():
    manga.log_debug("preview()")
    if(request.method == 'GET'):
        if "preview" in session:
            preview = session["preview"]
        else:
            preview = "NO PREVIEW"
        return render_template('preview.html', preview = preview, len = len(preview))
    else:
        if "format" in session:
            format = session["format"]
        else:
            format = ""
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
        commit = request.form['commit']
        if(commit == "Commit"):
            manga.log_debug("Commit to format")
            if(format == "auto_chapter"):
                result = manga.auto_chapter_format(manga.get_manga(manga_title), title)
            elif(format == "auto_volume"):
                result = manga.auto_volume_format(manga.get_manga(manga_title), number, title)
            elif(format == "manual_single_chapter"):
                result = manga.manual_single_chapter_format(manga_title, number, title)
            elif(format == "manual_multiple_chapter"):
                result = manga.manual_multiple_chapter_format(manga_title)
            elif(format == "manual_volume"):
                result = manga.manual_volume_format(manga_title, number, title)
            else:
                manga.log_critical("MAJOR ERROR")
                session["error"] = "MAJOR ERROR"
        elif(commit =="Abort"):
            return redirect('/')
        if(result == False):
            session["error"] = manga.message_read()
            return redirect('/error')
        return redirect('/')

@app.route('/error', methods = ['GET', 'POST'])
def error():
    manga.log_debug("error()")
    if(request.method == 'GET'):
        if "error" in session:
            error = session["error"]
        else:
            error = "UNKNOWN"
        return render_template('error.html', error = error)
    else:
        return redirect('/')
