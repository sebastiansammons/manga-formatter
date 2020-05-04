import sys
import os
import shutil
import sqlite3
import mangaconfig
import mangalogging

def sql_format_chapter(mangatitle) :
    mangalogging.log_debug("mangaformatlib.sql_format_chapter(" + mangatitle + ")")
    #Create list of non-hidden files
    try :
        #Don't really need to "try" this since main already did it. But I guess it doesn't hurt
        chapterpages = [f for f in os.listdir(mangaconfig.QUEUESRC) if not f.startswith('.')]
    except :
        mangalogging.log_error("[" + mangaconfig.QUEUESRC + "] NOT FOUND")
        exit()
    #Sort list
    chapterpages = sorted(chapterpages)
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
        #unlock mutex?
    except :
        mangalogging.log_error("[" + mangaconfig.MYSQLITEDB + "] NOT FOUND")
        exit()
    #Create directory path for new chapter
    newchapterdir = mangaconfig.ROOTPATH + mangatitle + mangaconfig.CHAPTERFORMATPATH + str(newchapternumber).zfill(3) + "/"
    try :
        #Make new directory
        mangalogging.log_info("os.mkdir(" + newchapterdir + ")")
        os.mkdir(newchapterdir)
    except :
        #Check if directory exists
        if(len([f for f in os.listdir(newchapterdir) if not f.startswith('.')])==0) :
            #Directory exists but has nothing in it
            pass
        else :
            mangalogging.log_error("[" + newchapterdir + "] NOT CREATED")
            exit()
    #Get source and destination path
    pagesrc = [None] * numpages
    pagedest = [None] * numpages
    for i in range(0,numpages) :
        pagesrc[i] = mangaconfig.QUEUESRC + str(chapterpages[i])
        pagedest[i] = newchapterdir + mangatitle + " CH" + str(newchapternumber) +" PG" + str(i+1) + get_extension(pagesrc[i])
    #Rename
    #lock mutex?
    rename(pagesrc, pagedest)
    #unlock mutex?
    #Update SQLite with new current chapter number
    c.execute("UPDATE manga set curchap = ? WHERE title = ?",(int(newchapternumber),mangatitle))
    #lock mutex?
    #conn.commit()
    #unlock mutex?
    conn.close()
    #Make copy of chapter cover if One Piece
    if(mangatitle=="One Piece") :
        one_piece_cover_copy(newchapterdir,newchapternumber)



def sql_format_volume(mangatitle,lastchapter) :
    mangalogging.log_debug("mangaformatlib.sql_format_volume(" + mangatitle + "," + lastchapter + ")")
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
        conn = sqlite3.connect(mangaconfig.MYSQLITEDB)
        c = conn.cursor()
        #Get current volume number from SQLite and increment
        c.execute("Select curvol from manga where title = ?",(mangatitle,))
        sqldata = [tup[0] for tup in c.fetchall()]
        newvolumenumber = sqldata[0] + 1
        #Get first chapter of new volume
        c.execute("Select fconv from manga where title = ?",(mangatitle,))
        sqldata = [tup[0] for tup in c.fetchall()]
        firstchapnum = sqldata[0]
    except :
        mangalogging.log_error("[" + mangaconfig.MYSQLITEDB + "] NOT FOUND")
        exit()
    #Make sure user entered a chapter number thats newer then the fconv
    if(int(lastchapter)<=firstchapnum) :
        mangalogging.log_warning("[" + lastchapter + "] <= " + str(firstchapnum) + "]")
        exit()
    #Create new volume directory path
    if(mangatitle=="One Piece") :
        newvolumedir = mangaconfig.ROOTPATH + mangatitle + mangaconfig.VOLUMEFORMATPATH + mangatitle + " Volume " + str(newvolumenumber).zfill(3) + "/"
    else :
        newvolumedir = mangaconfig.ROOTPATH + mangatitle + mangaconfig.VOLUMEFORMATPATH + mangatitle + " Volume " + str(newvolumenumber).zfill(2) + "/"
    #Create new directory (from new path just generated)
    #Check if directory exists
    try :
        #TODO: CHANGE log_info formatting?
        mangalogging.log_info("os.mkdir(" + newvolumedir + ")")
        os.mkdir(newvolumedir)
    except :
        if(len([f for f in os.listdir(newvolumedir) if not f.startswith('.')])==0) :
            #Directory exists but nothing is in it
            pass
        else :
            mangalogging.log_error("[" + newvolumedir + "] ALREADY EXISTS")
            exit()
    #Rename volume cover
    volumecoversrc = mangaconfig.QUEUESRC + volumecoverdir[0]
    if(mangatitle=="One Piece") :
        volumecoverdest = newvolumedir + mangatitle + " " + str(newvolumenumber).zfill(3) + get_extension(volumecoversrc)
    else :
        volumecoverdest = newvolumedir + mangatitle + " " + str(newvolumenumber).zfill(2) + get_extension(volumecoversrc)
    #Rename cover
    rename(volumecoversrc,volumecoverdest)
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
    #Get Number of pages
    numpages = 0
    for i in range(0,numchapters) :
        numpages+=len(chapterpagesrc[i])
    #Get source and destination path
    pagesrc = [None] * numpages
    pagedest = [None] * numpages
    pagecount = 0
    for i in range(0,numchapters) :
        for j in range(0,len(chapterpagesrc[i])) :
            pagesrc[pagecount] = chapterdir[i] + chapterpagesrc[i][j]
            pagedest[pagecount] = newvolumedir + chapterpagesrc[i][j]
            pagecount+=1
    #Rename
    rename(pagesrc,pagedest)
    #Remove old directories
    for i in range(0,numchapters) :
        try :
            mangalogging.log_info("shutil.rmtree(" + chapterdir[i] + ")")
            shutil.rmtree(chapterdir[i])
        except :
            mangalogging.log_warning("[" + chapterdir[i] + "] COULD NOT BE REMOVED")
    #Update SQLite with new current volume number
    c.execute("UPDATE manga set curvol = ? WHERE title = ?",(int(newvolumenumber),mangatitle))
    #Update SQLite with new first chapter of new volume number
    c.execute("UPDATE manga set fconv = ? WHERE title = ?",(int(lastchapter) + 1,mangatitle))
    #conn.commit()
    conn.close()



def manual_single_chapter(mangatitle,chapternumber) :
    mangalogging.log_debug("mangaformatlib.manual_single_chapter(" + mangatitle + "," + chapternumber + ")")
    #Create list of non-hidden filenames
    chapterpages = [f for f in os.listdir(mangaconfig.QUEUESRC) if not f.startswith('.')]
    #Sort pages
    chapterpages = sorted(chapterpages)
    #Get number of pages for the new chapter
    numpages = len(chapterpages)   
    #Create new chapter directory
    newchapterdir = mangaconfig.MANUALDEST + chapternumber.zfill(3) + "/"
    #Check if directory exists
    try:
        mangalogging.log_info("os.mkdir(" +  newchapterdir + ")")
        os.mkdir(newchapterdir)
    except :
        if(len([f for f in os.listdir(newchapterdir) if not f.startswith('.')])==0) :
            #Directory exists but nothing is in it
            pass
        else :
            mangalogging.log_error("[" + newchapterdir + "] ALREADY EXISTS")
            exit()
    #Get source and destination path
    pagesrc = [None] * numpages
    pagedest = [None] * numpages
    for i in range(0,numpages) :
        #Singe chapter so queue should just be the pages
        pagesrc[i]= mangaconfig.QUEUESRC + str(chapterpages[i])
        pagedest[i] = newchapterdir + mangatitle + " CH" + str(chapternumber) + " PG" + str(i+1) + get_extension(pagesrc[i])
    #Rename
    rename(pagesrc,pagedest)



def manual_multiple_chapter(mangatitle) :
    mangalogging.log_debug("mangaformatlib.manual_multiple_chapter" + mangatitle + ")")
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
    #Source list of each chapter page list (2D List)
    chapterpagesrc = [None] * numchapters
    #Destination list of each chapter page list (2D List)
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
        try :
            mangalogging.log_info("os.mkdir(" + chapterdestdir[i] + ")")
            os.mkdir(chapterdestdir[i])
        except :
            if(len([f for f in os.listdir(chapterdestdir[i]) if not f.startswith('.')])==0) :
                #Directory exists but nothing is in it
                pass
            else :
                mangalogging.log_error("[" + chapterdestdir[i] + "] ALREADY EXISTS")
                exit()
    numpages = 0
    for i in range(0,numchapters) :
        numpages+=len(chapterpagesrc[i])
    src = [None] * numpages
    dest = [None] * numpages
    pageindex = 0
    for i in range(0,numchapters) :
        for j in range(0,len(chapterpagesrc[i])) :
            src[pageindex] = chaptersrcdir[i] + chapterpagesrc[i][j]
            dest[pageindex] = chapterdestdir[i] + chapterpagedest[i][j]
            pageindex+=1
    rename(src,dest)
    #Remove old directories
    for i in range(0,numchapters):
        try :
            mangalogging.log_info("shutil.rmtree(" + chaptersrcdir[i] + ")")
            shutil.rmtree(chaptersrcdir[i])
        except :
            mangalogging.log_warning("[" + chaptersrcdir[i] + "] COULD NOT REMOVE")            



def manual_format_volume(mangatitle,number) :
    mangalogging.log_debug("mangaformatlib.manual_format_volume(" + mangatitle + "," + number + ")")
    #make sure src has consistend volume to format (chapters are in sequential order)
    manual_multiple_chapter(mangatitle)
    #Get list of chapters
    chapterdir = [f for f in os.listdir(mangaconfig.MANUALDEST) if not f.startswith('.')]
    #Sort chaptersrc list
    chapterdir = sorted(chapterdir)
    numchapters = len(chapterdir)
    chapterpagesrc = [None] * numchapters
    #Get chapter destination directory path
    newvolumedir = mangaconfig.MANUALDEST + mangatitle + " Volume " + str(number).zfill(2) + "/"
    #Make chapter destination directory
    try :
        mangalogging.log_info("os.mkdir( " + newvolumedir + ")")
        os.mkdir(newvolumedir)
    except :
        if(len([f for f in os.listdir(newvolumedir) if not f.startswith('.')])==0) :
            #Directory exists but nothing is in it
            pass
        else :
            mangalogging.log_error("[" + newvolumedir + "] ALREADY EXISTS")
            exit()
    #Get list of each chapter's page source
    for i in range(0,numchapters):
        try :
            chapterpagesrc[i] = [f for f in os.listdir(mangaconfig.MANUALDEST+chapterdir[i]) if not f.startswith('.')]
        except :
            mangalogging.log_error("[" + mangaconfig.MANUALDEST+chapterdir[i] + "] NOT FOUND")
            break
        chapterpagesrc[i] = sorted(chapterpagesrc[i])
    numpages = 0
    for i in range(0,numchapters) :
        numpages +=len(chapterpagesrc[i])
    src = [None] * numpages
    dest = [None] * numpages
    pageindex = 0
    for i in range(0,numchapters) :
        for j in range(0,len(chapterpagesrc[i])) :
            src[pageindex] = mangaconfig.MANUALDEST + chapterdir[i] + "/" +chapterpagesrc[i][j]
            dest[pageindex] = newvolumedir + chapterpagesrc[i][j]
            pageindex+=1
    rename(src,dest)           
    #Remove old chapter direcotry
    for i in range(0,numchapters):
        try : 
            shutil.rmtree(mangaconfig.MANUALDEST + chapterdir[i])
        except :
            mangalogging.log_warning("[" + mangaconfig.MANUALDEST + chapterdir[i] + "] COULD NOT BE REMOVED")


def rename(src,dest):
    mangalogging.log_debug("mangaformatlib.rename()")
    #single page rename
    if(isinstance(src,str) & isinstance(dest,str)):
        try:
            mangalogging.log_info("os.rename(" + src + "," + dest + ")")
            os.rename(src,dest)
        except:
            mangalogging.log_error("[" + src + " TO " + dest + "] COULD NOT RENAME")
            exit()
    else:
        #multiple page rename
        if(len(src)!=len(dest)):
            mangalogging.log_error("UNEVEN PAGES FOR RENAME")
            exit()
        for i in range(0,len(src)) :
            try :
                mangalogging.log_info("os.rename(" + src[i] + "," + dest[i] + ")")
                os.rename(src[i],dest[i])
            except :
                mangalogging.log_error("[" + src[i] + " TO " + dest[i] + "] COULD NOT RENAME")
                exit()
        


#set up mutex with this?
def one_piece_cover_copy(newchapterpath,newchapternumber) :
    mangalogging.log_debug("mangaformatlib.one_piece_cover_copy(" + newchapterpath + "," + str(newchapternumber) + ")")
    #Get cover page
    newchapterpages = [f for f in os.listdir(newchapterpath) if not f.startswith('.')]
    newchapterpages = sorted(newchapterpages)
    newchaptercoverdest = mangaconfig.OPCHAPTERCOVERPATH + "CH" + str(newchapternumber) + " Cover" + get_extension(newchapterpages[0])
    #Copy cover page
    if(os.path.isfile(newchaptercoverdest)) :
        mangalogging.log_error("[" + newchaptercoverdest + "] ALREADY EXISTS")  
    else :
        try :
            mangalogging.log_info("Copy: " + newchapterpath + newchapterpages[0] + " to " + newchaptercoverdest)
            copyfile(newchapterpath + newchapterpages[0],newchaptercoverdest)
        except :
            mangalogging.log_error("[" + newchapterpath + newchapterpages[0] + " TO " + newchaptercoverdest + "] COULD NOT COPY")



def get_extension(chaptersrcpage) :
    mangalogging.log_debug("mangaformatlib.get_extension(" + chaptersrcpage + ")")
    #Gets the extension of any filename
    #handle for no extension found(folder path passed instead on accident)
    return chaptersrcpage[chaptersrcpage.rfind('.'):]


#temp workaround
def get_manga(manga):
    mangalogging.log_debug("mangaformatlib.get_manga(" + manga + ")")
    if(manga=="aot"):
        return "Attack On Titan"
    elif(manga=="op"):
        return "One Piece"
    elif(manga=="mha"):
        return "My Hero Academia"
    elif(manga=="dstone"):
        return "Dr. Stone"
    elif(manga=="pnl"):
        return "The Promised Neverland"
    elif(manga=="boruto"):
        return "Boruto"
    elif(manga=='platend'):
        return "Platinum End"