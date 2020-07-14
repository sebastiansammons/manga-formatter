import os
from flask import Flask, render_template, request, redirect, session
import manga


#Get template path
template_path = os.path.abspath('../html')
app = Flask(__name__, template_folder = template_path)

app.secret_key = "heyalright"

#
#Initialize Logger
#
manga.log_config()

#
#Make sure path's in config are reachable
#
config_status = manga.check_manga_config()

@app.route('/', methods = ['GET', 'POST'])
def index():
    manga.log_debug("index()")
    if(manga.check_manga_config() == False):
        session["error"] = manga.ERROR_MSG
        return redirect('/error')
    if(request.method == 'GET'):
        session.pop("format", None)
        session.pop("manga", None)
        session.pop("number", None)
        session.pop("title", None)
        session.pop("preview", None)
        session.pop("error", None)
        manga.ERROR_MSG = ""
        return render_template('index.html')
    else:
        manga_title = request.form["manga"]
        if(manga_title == "auto"):
            return redirect('/auto')
        elif(manga_title == "manual"):
            return redirect('/manual')
        elif(manga_title == "full"):
            return redirect('/full')

@app.route('/auto', methods = ['GET', 'POST'])
def auto_format():
    manga.log_debug("auto_format()")
    if(request.method == 'GET'):
        return render_template('auto.html')
    else:
        format_type = request.form['format_type']
        manga_title = request.form['manga']
        number = request.form['last_chapter_in_volume']
        title = request.form['title']
        session["manga"] = manga_title
        session["number"] = number
        session["title"] = title
        if(format_type == "chapter"):
            session["format"] = "auto_chapter"
            preview = manga.auto_chapter_preview(manga.get_manga(manga_title), title)
            if(preview == False):
                session["error"] = manga.ERROR_MSG
                return redirect('/error')
        elif(format_type == "volume"):
            session["format"] = "auto_volume"
            preview = manga.auto_volume_preview(manga.get_manga(manga_title), number, title)
            if(preview == False):
                session["error"] = manga.ERROR_MSG
                return redirect('/error')
        else:
            return redirect('/')
        session["preview"] = preview
        return redirect('/preview')

@app.route('/manual', methods = ['GET', 'POST'])
def manual_format():
    manga.log_debug("manual_format()")
    if(request.method == 'GET'):
        return render_template('manual.html')
    else:
        format_type = request.form['format_type']
        manga_title = request.form['manga']
        number = request.form['number']
        title = request.form['title']
        chapter_type = request.form['chapter_type']
        session["manga"] = manga_title
        session["number"] = number
        session["title"] = title
        if(format_type == "chapter"):
            if(chapter_type == "single"):
                session["format"] = "manual_single_chapter"
                preview = manga.manual_single_chapter_preview(manga_title, number, title)
                if(preview == False):
                    session["error"] = manga.ERROR_MSG
                    return redirect('/error')
            elif(chapter_type == "multiple"):
                session["format"] = "manual_multiple_chapter"
                preview = manga.manual_multiple_chapter_preview(manga_title)
                if(preview == False):
                    session["error"] = manga.ERROR_MSG
                    return redirect('/error')
        elif(format_type == "volume"):
            session["format"] = "manual_volume"
            preview = manga.manual_volume_preview(manga_title, number, title)
            if(preview == False):
                session["error"] = manga.ERROR_MSG
                return redirect('/error')
        else:
            return redirect('/')
        session["preview"] = preview
        return redirect('/preview')

@app.route('/full', methods = ['GET', 'POST'])
def full_format():
    manga.log_debug("full_format()")
    if(request.method == 'GET'):
        return render_template('full_manga.html')
    else:
        manga_title = request.form['manga']
        if(manga_title == ""):
            manga.log_warning("EMPTY MANGA TITLE")
            session["error"] = "EMPTY MANGA TITLE"
            return redirect('/error')
        else:
            result = manga.full_manga(manga_title)
            if(result == False):
                session["error"] = manga.ERROR_MSG
                return redirect('/error')
            return redirect('/')

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
            session["error"] = manga.ERROR_MSG
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

if __name__ == "__main__":
    app.run(debug = True)