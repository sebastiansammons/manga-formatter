import os
from flask import Flask, render_template, request, redirect
import mangaconfig
import mangaformatlib

#Get template path
template_path = os.path.abspath('../html')
app = Flask(__name__, template_folder=template_path)

#
#Make sure mangaconfig.py is reachable
#

#Default version when template is local folder
#app = Flask(__name__)

@app.route('/')
def index():
    print("index()")
    return render_template('index.html')

@app.route('/', methods=['POST'])
def get_format():
    #need to be able to handle different forms, this is a workaround
    print("get_format()")
    format = request.form["format"]
    if(format=="auto"):
        return redirect('/auto')
    elif(format=="manual"):
        return redirect('/manual')

@app.route('/auto')
def auto_format():
    print("auto_format()")
    return render_template('autoformat.html')

@app.route('/auto', methods=['POST'])
def get_auto_format():
    print("get_auto_format()")
    fmat = request.form['fmat']
    manga = request.form['manga']
    volendat = request.form['volendat']
    # autoformat = request.form['autoformat']
    if(fmat=="chapter"):
        #make sure queue isn't empty
        print("mangaformatlib.sql_format_chapter!")
        #send values in logs() ##later
        mangaformatlib.sql_format_chapter(mangaformatlib.get_manga(manga))
        #^ return values based on errors, then redirect (i.e. db not connected, path can't be created, etc)
    elif(fmat=="volume"):
        #make sure queue isn't empty
        print("mangaformatlib.sql_format_volume")
        #send values in logs() ##later
        mangaformatlib.sql_format_volume(mangaformatlib.get_manga(manga),volendat)
        #^ return values based on errors, then redirect (i.e. db not connected, path can't be created, etc)
    return redirect('/logs')
    # return render_template('autoformat.html')    


@app.route('/manual')
def manual_format():
    print("manual_format()")
    #make sure queue isn't empty
    return render_template('manualformat.html')

@app.route('/manual', methods=['POST'])
def get_manual_format():
    print("get_manual_format()")
    fmat = request.form['format']
    manga = request.form['mangatitle']
    number = request.form['number']
    howmany = request.form['howmany']
    if(fmat=="chapter"):
        if(howmany=="single"):
            #make sure queue isn't empty
            print("mangaformatlib.manual_single_chapter()")
            #send values in logs() ##later
            mangaformatlib.manual_single_chapter(manga, number)
            #^ return values based on errors, then redirect (i.e. db not connected, path can't be created, etc)
        elif(howmany=="multiple"):
            #make sure queue isn't empty
            print("mangaformatlib.manual_multiple_chapter()")
            #send values in logs() ##later
            mangaformatlib.manual_multiple_chapter(manga)
            #^ return values based on errors, then redirect (i.e. db not connected, path can't be created, etc)
    elif(fmat=="volume"):
        #make sure queue isn't empty
        print("mangaformatlib.manual_format_volume()")
        #send values in logs() ##later
        mangaformatlib.manual_format_volume(manga,number)
        #^ return values based on errors, then redirect (i.e. db not connected, path can't be created, etc)  
    return redirect('/logs')

@app.route('/logs')
def logs():
    print("logs()")
    return render_template('formatqueue.html')

@app.route('/logs', methods=['POST'])
def determine_commit():
    print("determine_commit()")
    commit = request.form['commit']
    if(commit=="Commit"):
        print("commit()")
    #need to be able to handle different forms
    # if(abort=="Abort"):
    #     print("abort()")
    print(commit)
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)