from flask import Flask, render_template, request, redirect
import mangaconfig
import mangaformatlib

app = Flask(__name__)

@app.route('/')
def index():
    print("Loading Main Page")
    return render_template('index.html')

# @app.route('/', methods=['POST'])
# def getAuto():
#     print("Auto Click?")
#     format = request.form['auto']
#     if(format == "auto"):
#         return redirect('/auto')

# @app.route('/', methods=['POST'])
# def getManual():
#     print("Manual Click?")
#     format = request.form['manual']
#     if(format == "manual"):
#         return redirect('/manual')

@app.route('/', methods=['POST'])
def get_format():
    print("Loading something?")
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
    print("Loading AutoFormat Page")
    return render_template('autoformat.html')

@app.route('/auto', methods=['POST'])
def get_auto_format():
    fmat = request.form['fmat']
    manga = request.form['manga']
    volendat = request.form['volendat']
    # autoformat = request.form['autoformat']
    if(fmat=="chapter"):
        print("You Are running sql_format_chapter!")
        mangaformatlib.sql_format_chapter(mangaformatlib.get_manga(manga))
    elif():
        print("You Are running sql_format_volume")
        mangaformatlib.sql_format_volume(mangaformatlib.get_manga(manga),volendat)
    return redirect('/')
    # return render_template('autoformat.html')    

@app.route('/logs')
def logs():
    return render_template('formatqueue.html')


@app.route('/manual', methods=['GET','POST'])
def manual_format():
    return render_template('manualformat.html') 

# @app.route('/logs', methods=['POST', 'GET'])
# def logs():
#     if request.method == 'POST':
#         return redirect('/commit')
#     else:
#         #return render_template('formatqueue.html')
#         return render_template('formatqueue.html')


# @app.route('/commit', methods=['GET', 'POST'])
# def commit():
# #def commit(src,dest)
#     #commit, do the rename
#     #try: task
#     #except:?
#     return redirect('/')

# @app.route('/abort')
# def abort():
#     #abort, clean up anything that was before the rename (i.e. removing new directory)
#     #try: task
#     #except: ?
#     return redirect('/logs')

if __name__ == "__main__":
    app.run(debug=True)