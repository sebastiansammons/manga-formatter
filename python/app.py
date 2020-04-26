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
    print("get_from()")
    format = request.form["format"]
    if(format=="auto"):
        return redirect('/auto',301)
    elif(format=="manual"):
        return redirect('/manual',301)

# #WORKING Auto/Manual Pick
# @app.route('/', methods=['GET','POST'])
# def getValue():
#     format = request.form['format']
#     if(format == "auto"):
#         return redirect('/auto')
#     elif(format == "manual"):
#         return redirect('/manual')
#     else:
#         print("No Auto or Manual")
#         return redirect('/auto')

# #Before
# @app.route('/', methods=['POST'])
# def getValue():
#     fmat = request.form['fmat']
#     manga = request.form['manga']
#     volendat = request.form['volendat']
#     autoformat = request.form['autoformat']
#     #manualformat = request.form['manualformat']
#     if(autoformat == "Auto Format"):
#         print("Auto Selected")
#         return render_template('autoformat.html', f=fmat, m=manga, vea=volendat, af=autoformat)
#     elif(manualformat == "Manual Format"):
#         print("Manual Selected")
#         return render_template('manualformat.html')
#     else:
#         print("No Auto or Manual")
#         return render_template('formatqueue.html', f=fmat, m=manga, vea=volendat, af=autoformat)

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
        print("You Are running sql_format_chapter!")
        mangaformatlib.sql_format_chapter(mangaformatlib.get_manga(manga))
        #^ return values based on errors, then redirect (i.e. db not connected, path can't be created, etc)
    elif(fmat=="volume"):
        #make sure queue isn't empty
        print("You Are running sql_format_volume")
        #mangaformatlib.sql_format_volume(mangaformatlib.get_manga(manga),volendat)
        #^ return values based on errors, then redirect (i.e. db not connected, path can't be created, etc)
    return redirect('/')
    # return render_template('autoformat.html')    

@app.route('/logs')
def logs():
    print("logs()")
    return render_template('formatqueue.html')

@app.route('/manual', methods=['GET','POST'])
def manual_format():
    print("manual_format()")
    #make sure queue isn't empty
    return render_template('manualformat.html') 

# @app.route('/logs', methods=['POST', 'GET'])
# def logs():
#     if request.method == 'POST':
#         return redirect('/commit')
#     else:
#         #return render_template('formatqueue.html')
#         return render_template('formatqueue.html')


if __name__ == "__main__":
    app.run(debug=True)