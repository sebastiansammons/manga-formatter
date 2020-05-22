import os
from flask import Flask, render_template, request, redirect, session
import mangaconfig
import mangaformatlib
import mangalogging
import mangapreview

#Get template path
template_path = os.path.abspath('../html')
app = Flask(__name__, template_folder=template_path)


app.secret_key = "heyalright"

#
#Make sure mangaconfig.py is reachable
#

#
#Initialize Logger
#
mangalogging.config()

#Default version when template is local folder
#app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    mangalogging.log_debug("index()")
    if(request.method == 'GET'):
        session.pop("format", None)
        session.pop("manga", None)
        session.pop("number", None)
        session.pop("preview", None)
        session.pop("error", None)
        mangalogging.ERROR_MSG = ""
        return render_template('index.html')
    else:
        manga_format = request.form["format"]
        if(manga_format=="auto"):
            return redirect('/auto')
        elif(manga_format=="manual"):
            return redirect('/manual')


@app.route('/auto', methods=['GET', 'POST'])
def auto_format():
    mangalogging.log_debug("auto_format()")
    if(request.method == 'GET'):
        return render_template('autoformat.html')
    else:
        fmat = request.form['fmat']
        manga = request.form['manga']
        number = request.form['volendat']
        session["manga"] = manga
        session["number"] = number
        if(fmat=="chapter"):
            session["format"] = "autochapter"
            preview = mangapreview.sql_format_chapter(mangaformatlib.get_manga(manga))
            if(preview==False):
                session["error"] = mangalogging.ERROR_MSG
                return redirect('/error')
        elif(fmat=="volume"):
            session["format"] = "autovolume"
            preview = mangapreview.sql_format_volume(mangaformatlib.get_manga(manga),number)
            if(preview==False):
                session["error"] = mangalogging.ERROR_MSG
                return redirect('/error')
        session["preview"] = preview
        return redirect('/preview')


@app.route('/manual', methods=['GET','POST'])
def manual_format():
    mangalogging.log_debug("manual_format()")
    if(request.method == 'GET'):
        return render_template('manualformat.html')
    else:
        fmat = request.form['format']
        manga = request.form['mangatitle']
        number = request.form['number']
        howmany = request.form['howmany']
        session["manga"] = manga
        session["number"] = number
        if(fmat=="chapter"):
            if(howmany=="single"):
                session["format"] = "manualsinglechapter"
                preview = mangapreview.manual_single_chapter(manga, number)
                if(preview==False):
                    session["error"] = mangalogging.ERROR_MSG
                    return redirect('/error')
            elif(howmany=="multiple"):
                session["format"] = "manualmultiplechapter"
                preview = mangapreview.manual_multiple_chapter(manga)
                if(preview==False):
                    session["error"] = mangalogging.ERROR_MSG
                    return redirect('/error')
        elif(fmat=="volume"):
            session["format"] = "manualvolume"
            preview = mangapreview.manual_format_volume(manga,number)
            if(preview==False):
                session["error"] = mangalogging.ERROR_MSG
                return redirect('/error')
        session["preview"] = preview
        return redirect('/preview')

@app.route('/preview', methods=['GET','POST'])
def preview():
    mangalogging.log_debug("preview()")
    if(request.method == 'GET'):
        if "preview" in session:
            preview = session["preview"]
        else:
            preview = ""
        return render_template('formatqueue.html',preview=preview, len=len(preview))
    else:
        if "manga" in session:
            manga = session["manga"]
        else:
            manga = ""
        if "number" in session:
            number = session["number"]
        else:
            number = ""
        if "format" in session:
            format = session["format"]
        else:
            format = ""
        commit = request.form['commit']
        if(commit=="Commit"):
            mangalogging.log_debug("commit()")
            if(format=="autochapter"):
                result = mangaformatlib.sql_format_chapter(mangaformatlib.get_manga(manga))
            elif(format=="autovolume"):
                result = mangaformatlib.sql_format_volume(mangaformatlib.get_manga(manga),number)
            elif(format=="manualsinglechapter"):
                result = mangaformatlib.manual_single_chapter(manga, number)
            elif(format=="manualmultiplechapter"):
                result = mangaformatlib.manual_multiple_chapter(manga)
            elif(format=="manualvolume"):
                result = mangaformatlib.manual_format_volume(manga,number)
            else:
                mangalogging.log_critical("MAJOR ERROR")
                session["error"] = "MAJOR ERROR"
        elif(commit=="Abort"):
            return redirect('/')
        if(result==False):
            session["error"] = mangalogging.ERROR_MSG
            return redirect('/error')
        return redirect('/')


@app.route('/error', methods=['GET','POST'])
def error():
    mangalogging.log_debug("error()")
    if(request.method == 'GET'):
        if "error" in session:
            error = session["error"]
        else:
            error = "Unknown"
        return render_template('error.html', error=error)
    else:
        return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)