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

@app.route('/')
def index():
    mangalogging.log_debug("index()")
    return render_template('index.html')

@app.route('/', methods=['POST'])
def get_format():
    #need to be able to handle different forms, this is a workaround
    mangalogging.log_debug("get_format()")
    format = request.form["format"]
    if(format=="auto"):
        return redirect('/auto')
    elif(format=="manual"):
        return redirect('/manual')

@app.route('/auto')
def auto_format():
    mangalogging.log_debug("auto_format()")
    return render_template('autoformat.html')

@app.route('/auto', methods=['POST'])
def get_auto_format():
    mangalogging.log_debug("get_auto_format()")
    fmat = request.form['fmat']
    manga = request.form['manga']
    number = request.form['volendat']
    session["manga"] = manga
    session["number"] = number
    if(fmat=="chapter"):
        session["format"] = "autochapter"
        preview = mangapreview.sql_format_chapter(mangaformatlib.get_manga(manga))
        if(preview==False):
            mangalogging.log_warning("PREVIEW ERROR AUTO CHAPTER")
            return redirect('/')
    elif(fmat=="volume"):
        session["format"] = "autovolume"
        preview = mangapreview.sql_format_volume(mangaformatlib.get_manga(manga),number)
        if(preview==False):
            mangalogging.log_warning("PREVIEW ERROR AUTO VOLUME")
            return redirect('/')
    session["preview"] = preview
    return redirect('/preview') 


@app.route('/manual')
def manual_format():
    mangalogging.log_debug("manual_format()")
    return render_template('manualformat.html')

@app.route('/manual', methods=['POST'])
def get_manual_format():
    mangalogging.log_debug("get_manual_format()")
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
                mangalogging.log_warning("PREVIEW ERROR MANUAL SINGLE CHAPTER")
                return redirect('/')
        elif(howmany=="multiple"):
            session["format"] = "manualmultiplechapter"
            preview = mangapreview.manual_multiple_chapter(manga)
            if(preview==False):
                mangalogging.log_warning("PREVIEW ERROR MANUAL MULTI CHAPTER")
                return redirect('/')
    elif(fmat=="volume"):
        session["format"] = "manualvolume"
        preview = mangapreview.manual_format_volume(manga,number)
        if(preview==False):
            mangalogging.log_warning("PREVIEW ERROR MANUAL VOLUME")
            return redirect('/')
    session["preview"] = preview
    return redirect('/preview')

@app.route('/preview')
def preview():
    mangalogging.log_debug("preview()")
    if "preview" in session:
        preview = session["preview"]
    else:
        preview = ""
    return render_template('formatqueue.html',preview=preview, len=len(preview))

@app.route('/preview', methods=['POST'])
def determine_commit():
    #need to be able to handle different forms, this is a workaround
    mangalogging.log_debug("determine_commit()")
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
            mangaformatlib.sql_format_chapter(mangaformatlib.get_manga(manga))
            #TODO return values based on errors, then redirect (i.e. db not connected, path can't be created, etc)
        elif(format=="autovolume"):
            mangaformatlib.sql_format_volume(mangaformatlib.get_manga(manga),number)
            #TODO return values based on errors, then redirect (i.e. db not connected, path can't be created, etc)
        elif(format=="manualsinglechapter"):
            mangaformatlib.manual_single_chapter(manga, number)
            #TODO return values based on errors, then redirect (i.e. db not connected, path can't be created, etc)
        elif(format=="manualmultiplechapter"):
            mangaformatlib.manual_multiple_chapter(manga)
            #TODO return values based on errors, then redirect (i.e. db not connected, path can't be created, etc)
        elif(format=="manualvolume"):
            mangaformatlib.manual_format_volume(manga,number)
            #TODO return values based on errors, then redirect (i.e. db not connected, path can't be created, etc)
        else:
            mangalogging.log_critical("MAJOR ERROR")
    elif(commit=="Abort"):
        return redirect('/')
    session.pop("manga", None)
    session.pop("number", None)
    session.pop("preview", None)
    #put these on first page?
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)