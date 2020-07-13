import os
from flask import Flask, render_template, request, redirect, session
import manga_logging
import manga_utility
import manga_format
import manga_preview
import manga_full


#Get template path
template_path = os.path.abspath('../html')
app = Flask(__name__, template_folder = template_path)

app.secret_key = "heyalright"

#
#Initialize Logger
#
manga_logging.config()

#
#Make sure path's in config are reachable
#
config_status = manga_utility.check_config()

@app.route('/', methods = ['GET', 'POST'])
def index():
    if(manga_utility.check_config() == False):
        session["error"] = manga_logging.ERROR_MSG
        return redirect('/error')
    manga_logging.log_debug("index()")
    if(request.method == 'GET'):
        session.pop("format", None)
        session.pop("manga", None)
        session.pop("number", None)
        session.pop("title", None)
        session.pop("preview", None)
        session.pop("error", None)
        manga_logging.ERROR_MSG = ""
        return render_template('index.html')
    else:
        manga_format = request.form["manga_format"]
        if(manga_format == "auto"):
            return redirect('/auto')
        elif(manga_format == "manual"):
            return redirect('/manual')
        elif(manga_format == "full"):
            return redirect('/full')

@app.route('/auto', methods = ['GET', 'POST'])
def auto_format():
    manga_logging.log_debug("auto_format()")
    if(request.method == 'GET'):
        return render_template('auto.html')
    else:
        format_type = request.form['format_type']
        manga = request.form['manga']
        number = request.form['last_chapter_in_volume']
        title = request.form['title']
        session["manga"] = manga
        session["number"] = number
        session["title"] = title
        if(format_type == "chapter"):
            session["format"] = "auto_chapter"
            preview = manga_preview.auto_chapter(manga_utility.get_manga(manga), title)
            if(preview == False):
                session["error"] = manga_logging.ERROR_MSG
                return redirect('/error')
        elif(format_type == "volume"):
            session["format"] = "auto_volume"
            preview = manga_preview.auto_volume(manga_utility.get_manga(manga), number, title)
            if(preview == False):
                session["error"] = manga_logging.ERROR_MSG
                return redirect('/error')
        else:
            return redirect('/')
        session["preview"] = preview
        return redirect('/preview')

@app.route('/manual', methods = ['GET', 'POST'])
def manual_format():
    manga_logging.log_debug("manual_format()")
    if(request.method == 'GET'):
        return render_template('manual.html')
    else:
        format_type = request.form['format_type']
        manga = request.form['manga']
        number = request.form['number']
        title = request.form['title']
        chapter_type = request.form['chapter_type']
        session["manga"] = manga
        session["number"] = number
        session["title"] = title
        if(format_type == "chapter"):
            if(chapter_type == "single"):
                session["format"] = "manual_single_chapter"
                preview = manga_preview.manual_single_chapter(manga, number, title)
                if(preview == False):
                    session["error"] = manga_logging.ERROR_MSG
                    return redirect('/error')
            elif(chapter_type == "multiple"):
                session["format"] = "manual_multiple_chapter"
                preview = manga_preview.manual_multiple_chapter(manga)
                if(preview == False):
                    session["error"] = manga_logging.ERROR_MSG
                    return redirect('/error')
        elif(format_type == "volume"):
            session["format"] = "manual_volume"
            preview = manga_preview.manual_volume(manga, number, title)
            if(preview == False):
                session["error"] = manga_logging.ERROR_MSG
                return redirect('/error')
        else:
            return redirect('/')
        session["preview"] = preview
        return redirect('/preview')

@app.route('/full', methods = ['GET', 'POST'])
def full_format():
    manga_logging.log_debug("full_format()")
    if(request.method == 'GET'):
        return render_template('full_manga.html')
    else:
        manga = request.form['manga']
        if(manga == ""):
            manga_logging.log_warning("EMPTY MANGA TITLE")
            session["error"] = "EMPTY MANGA TITLE"
            return redirect('/error')
        else:
            result = manga_full.full_manga(manga)
            if(result == False):
                session["error"] = manga_logging.ERROR_MSG
                return redirect('/error')
            return redirect('/')

@app.route('/preview', methods = ['GET', 'POST'])
def preview():
    manga_logging.log_debug("preview()")
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
            manga = session["manga"]
        else:
            manga = ""
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
            manga_logging.log_debug("Commit to format")
            if(format == "auto_chapter"):
                result = manga_format.auto_chapter(manga_utility.get_manga(manga), title)
            elif(format == "auto_volume"):
                result = manga_format.auto_volume(manga_utility.get_manga(manga), number, title)
            elif(format == "manual_single_chapter"):
                result = manga_format.manual_single_chapter(manga, number, title)
            elif(format == "manual_multiple_chapter"):
                result = manga_format.manual_multiple_chapter(manga)
            elif(format == "manual_volume"):
                result = manga_format.manual_volume(manga, number, title)
            else:
                manga_logging.log_critical("MAJOR ERROR")
                session["error"] = "MAJOR ERROR"
        elif(commit =="Abort"):
            return redirect('/')
        if(result == False):
            session["error"] = manga_logging.ERROR_MSG
            return redirect('/error')
        return redirect('/')

@app.route('/error', methods = ['GET', 'POST'])
def error():
    manga_logging.log_debug("error()")
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