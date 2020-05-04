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
        #make sure queue isn't empty
        preview = mangapreview.sql_format_chapter(mangaformatlib.get_manga(manga))
        session["format"] = "autochapter"
    elif(fmat=="volume"):
        #make sure queue isn't empty
        preview = mangapreview.sql_format_volume(mangaformatlib.get_manga(manga),number)
        session["format"] = "autovolume"
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
            #make sure queue isn't empty
            preview = mangapreview.manual_single_chapter(manga, number)
        elif(howmany=="multiple"):
            session["format"] = "manualmultiplechapter"
            #make sure queue isn't empty
            preview = mangapreview.manual_multiple_chapter(manga)
    elif(fmat=="volume"):
        session["format"] = "manualvolume"
        #make sure queue isn't empty
        preview = mangapreview.manual_format_volume(manga,number)
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
            print("autochapter: " + mangaformatlib.get_manga(manga))
            #mangaformatlib.sql_format_chapter(mangaformatlib.get_manga(manga))
            #^ return values based on errors, then redirect (i.e. db not connected, path can't be created, etc)
        elif(format=="autovolume"):
            print("autovolume: " +mangaformatlib.get_manga(manga) + ": " + number)
            #mangaformatlib.sql_format_volume(mangaformatlib.get_manga(manga),number)
            #^ return values based on errors, then redirect (i.e. db not connected, path can't be created, etc)
        elif(format=="manualsinglechapter"):
            print("manualsinglechapter: " + manga + ": " + number)
            #mangaformatlib.manual_single_chapter(manga, number)
            #^ return values based on errors, then redirect (i.e. db not connected, path can't be created, etc)
        elif(format=="manualmultiplechapter"):
            print("manualmultiplechapter: " + manga)
            #mangaformatlib.manual_multiple_chapter(manga)
            #^ return values based on errors, then redirect (i.e. db not connected, path can't be created, etc)
        elif(format=="manualvolume"):
            print("manualvolume: " + manga + ": " + number)
            #mangaformatlib.manual_format_volume(manga,number)
            #^ return values based on errors, then redirect (i.e. db not connected, path can't be created, etc)
        else:
            print("MAJOR ERROR")
    elif(commit=="Abort"):
        print("ABORT")
    session.pop("manga", None)
    session.pop("number", None)
    session.pop("preview", None)
    #put these on first page?
    print("End Session")
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)