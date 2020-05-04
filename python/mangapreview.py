import sys
import os
import sqlite3
import mangaconfig
import mangalogging



def sql_format_chapter(mangatitle) :
    mangalogging.log_debug("mangapreview.sql_format_chapter(" + mangatitle + ")")
    #Create list of non-hidden files
    try :
        chapterpages = [f for f in os.listdir(mangaconfig.QUEUESRC) if not f.startswith('.')]
    except :
        mangalogging.log_error("[" + mangaconfig.QUEUESRC + "] NOT FOUND")
        exit()
    #Sort list
    chapterpages = sorted(chapterpages)
    #
    #TODO: make sure the QUEUESRC isn't empty
    #
    #Get number of pages for the new chapter
    numpages = len(chapterpages)   
    #Connect to SQLite
    #Set up mutex?, Lock?
    try :
        conn = sqlite3.connect(mangaconfig.MYSQLITEDB)
        c = conn.cursor()
        #Get current chapter number from SQLite and increment
        c.execute("Select curchap from manga where title = ?",(mangatitle,))
        sqldata = [tup[0] for tup in c.fetchall()]
        newchapternumber = sqldata[0] + 1
        conn.close()
    except :
        mangalogging.log_error("[" + mangaconfig.MYSQLITEDB + "] NOT FOUND")
        exit()
    #Create directory path for new chapter
    newchapterdir = mangaconfig.ROOTPATH + mangatitle + mangaconfig.CHAPTERFORMATPATH + str(newchapternumber).zfill(3) + "/"
    #Get source and destination path
    src = [None] * numpages
    dest = [None] * numpages
    preview = [None] * numpages
    for i in range(0,numpages) :
        src[i] = mangaconfig.QUEUESRC + str(chapterpages[i])
        dest[i] = newchapterdir + mangatitle + " CH" + str(newchapternumber) +" PG" + str(i+1) + get_extension(src[i])
        if(mangaconfig.LOGTYPE=="SIMPLE"):
            preview[i] = "Rename: " + src[i][src[i].rfind("/"):] + " to " + dest[i][dest[i].rfind("/"):]
        elif(mangaconfig.LOGTYPE=="DETAILED"):
            preview[i] = "Rename: " + src[i] + " to " + dest[i]
    return preview



def sql_format_volume(mangatitle,lastchapter) :
    mangalogging.log_debug("mangapreview.sql_format_volume(" + mangatitle + "," + lastchapter + ")")
    #Get volume cover page
    try :
        volumecoverdir = [f for f in os.listdir(mangaconfig.QUEUESRC) if not f.startswith('.')]
    except :
        mangalogging.log_error("[" + mangaconfig.QUEUESRC + "] NOT FOUND")
        exit()
    #Make sure there is only 1 file in the directory (the cover)
    if(len(volumecoverdir)!=1) :
        mangalogging.log_warning("MORE THAN ONE FILE IN QUEUE. DON'T KNOW WHCH ONE IS VOLUME COVER")
        exit()
    #Connect to SQLite
    try :
        #Get data from db
        conn = sqlite3.connect(mangaconfig.MYSQLITEDB)
        c = conn.cursor()
        #Get current volume number
        c.execute("Select curvol from manga where title = ?",(mangatitle,))
        sqldata = [tup[0] for tup in c.fetchall()]
        newvolumenumber = sqldata[0] + 1
        #Get first chapter of new volume
        c.execute("Select fconv from manga where title = ?",(mangatitle,))
        sqldata = [tup[0] for tup in c.fetchall()]
        firstchapnum = sqldata[0]
        conn.close()
    except :
        mangalogging.log_error("[" + mangaconfig.MYSQLITEDB + "] NOT FOUND")
        exit()
    #Make sure user entered a chapter number thats newer then the fconv
    if(int(lastchapter)<=firstchapnum) :
        mangalogging.log_error("[" + lastchapter + "] <= " + str(firstchapnum) + "]")
        exit()
    #Create new volume directory path
    if(mangatitle=="One Piece") :
        newvolumedir = mangaconfig.ROOTPATH + mangatitle + mangaconfig.VOLUMEFORMATPATH + mangatitle + " Volume " + str(newvolumenumber).zfill(3) + "/"
    else :
        newvolumedir = mangaconfig.ROOTPATH + mangatitle + mangaconfig.VOLUMEFORMATPATH + mangatitle + " Volume " + str(newvolumenumber).zfill(2) + "/"
    #Finally move chapters
    numchapters = int(lastchapter) - firstchapnum + 1
    #List of chapter directories
    chapterdir = [None] * numchapters
    #list of each chapter page list (2D List)
    chapterpagesrc = [None] * numchapters
    for chapnum in range(firstchapnum,int(lastchapter) + 1) :
        #Get chapnum's directory and get the list of pages within the directory
        chapterdir[chapnum-firstchapnum] = mangaconfig.ROOTPATH + mangatitle + mangaconfig.CHAPTERFORMATPATH + str(chapnum).zfill(3) + "/"
        try :
            chapterpagesrc[chapnum-firstchapnum] = [f for f in os.listdir(chapterdir[chapnum-firstchapnum]) if not f.startswith('.')]
        except :
            mangalogging.log_error("[" + chapterdir[chapnum-firstchapnum] + "] NOT FOUND")
            break
        #Sort the pages (not realy needed tbh)
        chapterpagesrc[chapnum-firstchapnum] = sorted(chapterpagesrc[chapnum-firstchapnum])
    if(mangaconfig.LOGTYPE=="SIMPLE"):
        preview = [None] * numchapters
        for i in range(0,numchapters):
            preview[i] = "Rename: " + chapterdir[i][chapterdir[i].rfind("/",0,chapterdir[i].rfind("/")):] + " to " + newvolumedir[newvolumedir.rfind("/",0,newvolumedir.rfind("/")):]            
    elif(mangaconfig.LOGTYPE=="DETAILED"):
        #Get Number of pages
        numpages = 0
        for i in range(0,numchapters) :
            numpages+=len(chapterpagesrc[i])
        #Get source and destination path
        pagesrc = [None] * numpages
        pagedest = [None] * numpages
        preview = [None] * numpages
        pagecount = 0
        for i in range(0,numchapters) :
            for j in range(0,len(chapterpagesrc[i])) :
                pagesrc[pagecount] = chapterdir[i] + chapterpagesrc[i][j]
                pagedest[pagecount] = newvolumedir + chapterpagesrc[i][j]
                preview[pagecount] = "Rename: " + pagesrc[pagecount] + " to " + pagedest[pagecount]
                pagecount+=1
    return preview



def manual_single_chapter(mangatitle,chapternumber) :
    mangalogging.log_debug("mangapreview.manual_single_chapter(" + mangatitle + "," + chapternumber + ")")
    #Create list of non-hidden filenames
    chapterpages = [f for f in os.listdir(mangaconfig.QUEUESRC) if not f.startswith('.')]
    #Sort pages
    chapterpages = sorted(chapterpages)
    #Get number of pages for the new chapter
    numpages = len(chapterpages)
    #Create new chapter directory
    newchapterdir = mangaconfig.MANUALDEST + chapternumber.zfill(3) + "/"
    #Get source and destination path
    pagesrc = [None] * numpages
    pagedest = [None] * numpages
    preview = [None] * numpages
    for i in range(0,numpages) :
        #Singe chapter so queue should just be the pages
        pagesrc[i]= mangaconfig.QUEUESRC + str(chapterpages[i])
        pagedest[i] = newchapterdir + mangatitle + " CH" + str(chapternumber) + " PG" + str(i+1) + get_extension(pagesrc[i])
        if(mangaconfig.LOGTYPE=="SIMPLE"):
            preview[i] = "Rename: " + pagesrc[i][pagesrc[i].rfind("/"):] + " to " + pagedest[i][pagedest[i].rfind("/"):]
        elif(mangaconfig.LOGTYPE=="DETAILED"):
            preview[i] = "Rename: " + pagesrc[i] + " to " + pagedest[i]
    return preview



def manual_multiple_chapter(mangatitle) :
    mangalogging.log_debug("mangapreview.manual_multiple_chapter" + mangatitle + ")")
    #Assume QUESRC is formatted correctly (Each chapter is in their own directory with the correct chapter number as directory name)
    #List of chapter directories
    chaptersrclist = [f for f in os.listdir(mangaconfig.QUEUESRC) if not f.startswith('.')]
    #Sort directory list
    chaptersrclist = sorted(chaptersrclist)
    #Get number of chapters
    numchapters = len(chaptersrclist) 
    #List of source directories
    chaptersrcdir = [None] * numchapters
    #List of destination directories
    chapterdestdir = [None] * numchapters
    #Source list of each chapter page list
    chapterpagesrc = [None] * numchapters
    #Destination list of each chapter page list
    chapterpagedest = [None] * numchapters
    #Get source and destination directories and pages
    for i in range(0,numchapters) :
        #Get chapter source directoriy
        chaptersrcdir[i] = mangaconfig.QUEUESRC + chaptersrclist[i] + "/"
        #Get pages for each chapter
        try :
            curchapterpages = [f for f in os.listdir(chaptersrcdir[i]) if not f.startswith('.')]
        except :
            mangalogging.log_error("[" + chaptersrcdir[i] + "] NOT FOUND")
            break
        #Sort the chapter pages (not realy needed tbh)
        curchapterpages = sorted(curchapterpages)
        #Create list for each chapter
        chapterpagesrc[i] = [None] * len(curchapterpages)
        chapterpagedest[i] = [None] * len(curchapterpages)
        #Get each source and destination page
        for j in range(0,len(curchapterpages)) :
            chapterpagesrc[i][j] = curchapterpages[j]
            chapterpagedest[i][j] = mangatitle + " CH" + chaptersrclist[i].lstrip("0") + " PG" + str(j+1) + get_extension(curchapterpages[j])
        #Make chapter destination directories
        chapterdestdir[i] = mangaconfig.MANUALDEST + chaptersrclist[i].zfill(3) + "/"
    numpages = 0
    for i in range(0,numchapters) :
        numpages+=len(chapterpagesrc[i])
    src = [None] * numpages
    dest = [None] * numpages
    preview = [None] * numpages
    pageindex = 0
    for i in range(0,numchapters) :
        for j in range(0,len(chapterpagesrc[i])) :
            src[pageindex] = chaptersrcdir[i] + chapterpagesrc[i][j]
            dest[pageindex] = chapterdestdir[i] + chapterpagedest[i][j]
            if(mangaconfig.LOGTYPE=="SIMPLE"):
                preview[pageindex] = "Rename: " + src[pageindex][src[pageindex].rfind("/"):] + " to " + dest[pageindex][dest[pageindex].rfind("/"):]
            elif(mangaconfig.LOGTYPE=="DETAILED"):
                preview[pageindex] = "Rename: " + src[pageindex] + " to " + dest[pageindex]
            pageindex+=1
    return preview



def manual_format_volume(mangatitle,number) :
    mangalogging.log_debug("mangapreview.manual_format_volume(" + mangatitle + "," + number + ")")
    chapterpreview = manual_multiple_chapter(mangatitle)
    numpages = len(chapterpreview)
    preview = [None] * numpages
    for i in range(0,numpages):
        if(mangaconfig.LOGTYPE=="SIMPLE"):
            preview[i] = chapterpreview[i][:chapterpreview[i].rfind(" to ")] + " to /" + mangatitle + " Volume " + str(number).zfill(2) + chapterpreview[i][chapterpreview[i].rfind("/"):]
        elif(mangaconfig.LOGTYPE=="DETAILED"):
            preview[i] = chapterpreview[i][:chapterpreview[i].rfind(" to ")] + " to " + mangaconfig.MANUALDEST + mangatitle + " Volume " + str(number).zfill(2) + chapterpreview[i][chapterpreview[i].rfind("/"):]
    return preview

def get_extension(chaptersrcpage) :
    mangalogging.log_debug("mangapreview.get_extension(" + chaptersrcpage + ")")
    #Gets the extension of any filename
    #handle for no extension found(folder path passed instead on accident)
    return chaptersrcpage[chaptersrcpage.rfind('.'):]