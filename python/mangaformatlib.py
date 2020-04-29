import sys
import os
import shutil
from shutil import copyfile
import sqlite3
import mangaconfig
import mangalogging

def sql_format_chapter(mangatitle) :
    mangalogging.log_debug("sql_format_chapter(" + mangatitle + ")")
    #Create list of non-hidden files
    try :
        #Don't really need to "try" this since main already did it. But I guess it doesn't hurt
        mangalogging.log_debug("chapterpages = [f for f in os.listdir(" + mangaconfig.QUEUESRC + ") if not f.startswith('.')]")
        chapterpages = [f for f in os.listdir(mangaconfig.QUEUESRC) if not f.startswith('.')]
    except :
        mangalogging.log_error("ERROR!! [" + mangaconfig.QUEUESRC + "] NOT FOUND")
        exit()
    #Sort list
    chapterpages = sorted(chapterpages)
    #Get number of pages for the new chapter
    numpages = len(chapterpages)   
    #Connect to SQLite
    #Set up mutex?, Lock?
    try :
        mangalogging.log_debug("conn = sqlite3.connect(" + mangaconfig.MYSQLITEDB + ")")
        conn = sqlite3.connect(mangaconfig.MYSQLITEDB)
        c = conn.cursor()
        #Get current chapter number from SQLite and increment
        c.execute("Select curchap from manga where title = ?",(mangatitle,))
        sqldata = [tup[0] for tup in c.fetchall()]
        newchapternumber = sqldata[0] + 1
        #unlock mutex?
    except :
        mangalogging.log_error("CANNOT CONNECT TO fridgemedia.db")
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
            mangalogging.log_debug("len([f for f in os.listdir(" + newchapterdir + ") if not f.startswith('.')])==0")
            pass
        else :
            mangalogging.log_error("Error Creating Directory: " + newchapterdir)
            exit()
    #Get source and destination paths for "preview" and format
    pagesrc = [None] * numpages
    pagedest = [None] * numpages
    for i in range(0,numpages) :
        mangalogging.log_debug("pagesrc[ " +str(i) + "] = " + mangaconfig.QUEUESRC + str(chapterpages[i]))
        pagesrc[i] = mangaconfig.QUEUESRC + str(chapterpages[i])
        mangalogging.log_debug("pagedest[" + str(i) + "] =" + newchapterdir + mangatitle + " CH" + str(newchapternumber) +" PG" + str(i+1) + get_extension(pagesrc[i]))
        pagedest[i] = newchapterdir + mangatitle + " CH" + str(newchapternumber) +" PG" + str(i+1) + get_extension(pagesrc[i])
    #Show "preview"
    preview(pagesrc, pagedest)
    #Rename
    #lock mutex?
    rename(pagesrc, pagedest)
    #unlock mutex?
    #Update SQLite with new current chapter number
    c.execute("UPDATE manga set curchap = ? WHERE title = ?",(int(newchapternumber),mangatitle))
    #lock mutex?
    mangalogging.log_debug("conn.commit()")
    #conn.commit()
    #unlock mutex?
    mangalogging.log_debug("conn.close")
    conn.close()
    #Make copy of chapter cover if One Piece is formatted
    if(mangatitle=="One Piece") :
        one_piece_cover_copy(newchapterdir,newchapternumber)



def sql_format_volume(mangatitle,lastchapter) :
    mangalogging.log_debug("sql_format_volume(" + mangatitle + "," + lastchapter + ")")
    #Get volume cover page
    try :
        mangalogging.log_debug("volumecoverdir = [f for f in os.listdir(" + mangaconfig.QUEUESRC + ") if not f.startswith('.')]")
        volumecoverdir = [f for f in os.listdir(mangaconfig.QUEUESRC) if not f.startswith('.')]
    except :
        mangalogging.log_error("ERROR!! [" + mangaconfig.QUEUESRC + "] NOT FOUND")
        exit()
    #Make sure there is only 1 file in the directory (the cover)
    if(len(volumecoverdir)!=1) :
        mangalogging.log_error("MORE THAN ONE FILE IN QUEUE. DON'T KNOW WHCH ONE IS VOLUME COVER")
        exit()
    #Connect to SQLite
    try :
        mangalogging.log_debug("conn = sqlite3.connect(" + mangaconfig.MYSQLITEDB + ")")
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
        mangalogging.log_error("CANNOT CONNECT TO fridgemedia.db")
        exit()
    #Make sure user entered a chapter number thats newer then the fconv
    if(int(lastchapter)<=firstchapnum) :
        mangalogging.log_error("Last Chapter number < First chapter number!!!!")
        exit()
    #Create path for new chapter directory
    if(mangatitle=="One Piece") :
        mangalogging.log_debug("newvolumedir = " + mangaconfig.ROOTPATH + mangatitle + mangaconfig.VOLUMEFORMATPATH + mangatitle + " Volume " + str(newvolumenumber).zfill(3) + "/")
        newvolumedir = mangaconfig.ROOTPATH + mangatitle + mangaconfig.VOLUMEFORMATPATH + mangatitle + " Volume " + str(newvolumenumber).zfill(3) + "/"
    else :
        mangalogging.log_debug("newvolumedir = " + mangaconfig.ROOTPATH + mangatitle + mangaconfig.VOLUMEFORMATPATH + mangatitle + " Volume " + str(newvolumenumber).zfill(2) + "/")
        newvolumedir = mangaconfig.ROOTPATH + mangatitle + mangaconfig.VOLUMEFORMATPATH + mangatitle + " Volume " + str(newvolumenumber).zfill(2) + "/"
    #Create new directory (from new path just generated)
    #Check if directory exists
    try :
        mangalogging.log_info("os.mkdir(" + newvolumedir + ")")
        os.mkdir(newvolumedir)
    except :
        if(len([f for f in os.listdir(newvolumedir) if not f.startswith('.')])==0) :
            #Directory exists but nothing is in it
            mangalogging.log_debug("len([f for f in os.listdir(" + newvolumedir + ") if not f.startswith('.')])==0")
            pass
        else :
            mangalogging.log_error("Error Creating Directory: " + newvolumedir)
            exit()
    #Format volume cover
    volumecoversrc = mangaconfig.QUEUESRC + volumecoverdir[0]
    if(mangatitle=="One Piece") :
        mangalogging.log_debug("volumecoverdest = " + newvolumedir + mangatitle + " " + str(newvolumenumber).zfill(3) + get_extension(volumecoversrc))
        volumecoverdest = newvolumedir + mangatitle + " " + str(newvolumenumber).zfill(3) + get_extension(volumecoversrc)
    else :
        mangalogging.log_debug("volumecoverdest = " + newvolumedir + mangatitle + " " + str(newvolumenumber).zfill(2) + get_extension(volumecoversrc))
        volumecoverdest = newvolumedir + mangatitle + " " + str(newvolumenumber).zfill(2) + get_extension(volumecoversrc)
    #Format cover
    try :
        rename(volumecoversrc,volumecoverdest)
    except :
        mangalogging.log_error("ERROR formatting cover page")
        exit()
    #Finally move chapters
    numchapters = int(lastchapter) - firstchapnum + 1
    #List of chapter directories
    chapterdir = [None] * numchapters
    #list of each chapter page list (2D List)
    chapterpagesrc = [None] * numchapters
    for chapnum in range(firstchapnum,int(lastchapter) + 1) :
        #Get chapnum's directory and get the list of pages within the directory
        mangalogging.log_debug("chapterdir[" + str(chapnum-firstchapnum) + "] = " + mangaconfig.ROOTPATH + mangatitle + mangaconfig.CHAPTERFORMATPATH + str(chapnum).zfill(3) + "/")
        chapterdir[chapnum-firstchapnum] = mangaconfig.ROOTPATH + mangatitle + mangaconfig.CHAPTERFORMATPATH + str(chapnum).zfill(3) + "/"
        try :
            mangalogging.log_debug("chapterpagesrc[" + str(chapnum-firstchapnum) + "] = [f for f in os.listdir(chapterdir[" + str(chapnum-firstchapnum) + "]) if not f.startswith('.')]")
            chapterpagesrc[chapnum-firstchapnum] = [f for f in os.listdir(chapterdir[chapnum-firstchapnum]) if not f.startswith('.')]
        except :
            mangalogging.log_error("ERROR!! [" + chapterdir[chapnum-firstchapnum] + "] NOT FOUND")
            break
        #Sort the pages (not realy needed tbh)
        chapterpagesrc[chapnum-firstchapnum] = sorted(chapterpagesrc[chapnum-firstchapnum])
    #Get Number of pages
    numpages = 0
    for i in range(0,numchapters) :
        numpages+=len(chapterpagesrc[i])
    #Get Source and Dest
    pagesrc = [None] * numpages
    pagedest = [None] * numpages
    pagecount = 0
    for i in range(0,numchapters) :
        for j in range(0,len(chapterpagesrc[i])) :
            pagesrc[pagecount] = chapterdir[i] + chapterpagesrc[i][j]
            pagedest[pagecount] = newvolumedir + chapterpagesrc[i][j]
            # preview[pagecount] = chapterdir[i] + chapterpagesrc[i][j] + " to " + newvolumedir + chapterpagesrc[i][j]
            pagecount+=1
    #"Preview" changes
    preview(pagesrc,pagedest)
    #Rename
    rename(pagesrc,pagedest)
    #Remove old directories
    for i in range(0,numchapters) :
        try :
            mangalogging.log_info("shutil.rmtree(" + chapterdir[i] + ")")
            shutil.rmtree(chapterdir[i])
        except :
            mangalogging.log_error("ERROR!! UNABLE TO REMOVE [" + chapterdir[i] + "] You need to manually remove it")
    #Update SQLite with new current volume number
    c.execute("UPDATE manga set curvol = ? WHERE title = ?",(int(newvolumenumber),mangatitle))
    #Update SQLite with new first chapter of new volume number
    c.execute("UPDATE manga set fconv = ? WHERE title = ?",(int(lastchapter) + 1,mangatitle))
    mangalogging.log_debug("conn.commit()")
    #conn.commit()
    mangalogging.log_debug("conn.close()")
    conn.close()



def manual_single_chapter(mangatitle,chapternumber) :
    mangalogging.log_debug("manual_single_chapter(" + mangatitle + "," + chapternumber + ")")
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
            mangalogging.log_debug("len([f for f in os.listdir(" + newchapterdir + ") if not f.startswith('.')])==0")
            pass
        else :
            mangalogging.log_error("Error Creating Directory: " + newchapterdir)
            exit()
    #Get full source and destination paths for logs and format
    pagesrc = [None] * numpages
    pagedest = [None] * numpages
    for i in range(0,numpages) :
        #Singe chapter so queue should just be the pages
        pagesrc[i]= mangaconfig.QUEUESRC + str(chapterpages[i])
        pagedest[i] = newchapterdir + mangatitle + " CH" + str(chapternumber) + " PG" + str(i+1) + get_extension(pagesrc[i])
    #Show "preview"
    preview(pagesrc,pagedest)    
    #Rename
    rename(pagesrc,pagedest)



def manual_multiple_chapter(mangatitle) :
    mangalogging.log_debug("manual_multiple_chapter" + mangatitle + ")")
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
    #Get source and destination directories
    for i in range(0,numchapters) :
        #Get chapter source directories
        chaptersrcdir[i] = mangaconfig.QUEUESRC + chaptersrclist[i] + "/"
        #Get chapter destination directories
        chapterdestdir[i] = mangaconfig.MANUALDEST + chaptersrclist[i].zfill(3) + "/"
        #Make chapter destination directories
        try :
            mangalogging.log_info("os.mkdir(" + chapterdestdir[i] + ")")
            os.mkdir(chapterdestdir[i])
        except :
            if(len([f for f in os.listdir(chapterdestdir[i]) if not f.startswith('.')])==0) :
                mangalogging.log_debug("len([f for f in os.listdir(" + chapterdestdir[i] + ") if not f.startswith('.')])==0")
                #Directory exists but nothing is in it
                pass
            else :
                mangalogging.log_error("Error Creating Directory: " + chapterdestdir[i])
                exit()
    #Get Source and Destination for each chapter
    for i in range(0,numchapters) :
        #Get pages for each chapter
        try :
            mangalogging.log_debug("curchapterpages = [f for f in os.listdir(" + chaptersrcdir[i] + ") if not f.startswith('.')]")
            curchapterpages = [f for f in os.listdir(chaptersrcdir[i]) if not f.startswith('.')]
        except :
            mangalogging.log_error("ERROR!! [" + chaptersrcdir[i] + "] NOT FOUND")
            break
        #Sort the chapter pages (not realy needed tbh)
        curchapterpages = sorted(curchapterpages)
        #Create list for each chapter
        chapterpagesrc[i] = [None] * len(curchapterpages)
        chapterpagedest[i] = [None] * len(curchapterpages)
        #Get each source path and destination format path for each page
        for j in range(0,len(curchapterpages)) :
            chapterpagesrc[i][j] = curchapterpages[j]
            chapterpagedest[i][j] = mangatitle + " CH" + chaptersrclist[i].lstrip("0") + " PG" + str(j+1) + get_extension(curchapterpages[j])
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
    #New Preview and Rename
    preview(src,dest)
    rename(src,dest)
    #Remove old directories
    for i in range(0,numchapters):
        try :
            mangalogging.log_info("shutil.rmtree(" + chaptersrcdir[i] + ")")
            shutil.rmtree(chaptersrcdir[i])
        except :
            mangalogging.log_error("ERROR!! UNABLE TO REMOVE [" + chaptersrcdir[i] + "] You need to manually remove it")            



def manual_format_volume(mangatitle,number) :
    mangalogging.log_debug("manual_format_volume(" + mangatitle + "," + number + ")")
    #make sure src has consistend volume to format (chapters are in sequential order)
    manual_multiple_chapter(mangatitle)
    #Get list of chapters
    chapterdir = [f for f in os.listdir(mangaconfig.MANUALDEST) if not f.startswith('.')]
    #Sort chaptersrc list
    chapterdir = sorted(chapterdir)
    numchapters = len(chapterdir)
    src = [None] * numchapters
    dest = [None] * numchapters
    #Get chapter destination directory path
    newvolumedir = mangaconfig.MANUALDEST + mangatitle + " Volume " + str(number).zfill(2) + "/"
    #Make chapter destination directory
    try :
        mangalogging.log_info("os.mkdir( " + newvolumedir + ")")
        os.mkdir(newvolumedir)
    except :
        if(len([f for f in os.listdir(newvolumedir) if not f.startswith('.')])==0) :
            mangalogging.log_debug("len([f for f in os.listdir(" + newvolumedir + ") if not f.startswith('.')])==0")
            #Directory exists but nothing is in it
            pass
        else :
            mangalogging.log_error("ERROR Creating Directory: " + newvolumedir)
            exit()
    #Move chapters to new volume directory
    for i in range(0,numchapters) :
        src[i] = mangaconfig.MANUALDEST + chapterdir[i]
        dest[i] = newvolumedir
    preview(src,dest)
    for i in range(0,numchapters) :
        mangalogging.log_info("shutil.move(" + src[i] + "," + dest[i] + ")") 
        shutil.move(src[i],dest[i])



def rename(src,dest):
    mangalogging.log_debug("rename(" + src + "," + dest + ")")
    if(len(src)!=len(dest)):
        mangalogging.log_error("SRC and DEST DON'T MATCH")
        exit()
    for i in range(0,len(src)) :
        try :
            mangalogging.log_info("os.rename(" + src[i] + "," + dest[i] + ")")
            os.rename(src[i],dest[i])
        except :
            mangalogging.log_error("ERROR renaming: " + src[i] + " to " + dest[i])
            exit()



def preview(src, dest):
    #TODO: update preview for simple volume?
    mangalogging.log_debug("preview(" + src + "," + dest + ")")
    if(mangaconfig.LOGTYPE=="Simple"):
        for i in range(len(src)):
            simplesrc  = src[i][src[i].rfind("/"):]
            simpledest = dest[i][dest[i].rfind("/"):]
            mangalogging.log_debug("Rename: " + simplesrc + " to " + simpledest)
    elif(mangaconfig.LOGTYPE=="Detailed"):
        for i in range(len(src)):
            mangalogging.log_debug("Rename: " + src[i] + " to " + dest[i])
        


#set up mutex with this?
def one_piece_cover_copy(newchapterpath,newchapternumber) :
    mangalogging.log_debug("one_piece_cover_copy(" + newchapterpath + "," + str(newchapternumber) + ")")
    #Get cover page
    newchapterpages = [f for f in os.listdir(newchapterpath) if not f.startswith('.')]
    newchapterpages = sorted(newchapterpages)
    newchaptercoverdest = mangaconfig.OPCHAPTERCOVERPATH + "CH" + str(newchapternumber) + " Cover" + get_extension(newchapterpages[0])
    #Copy cover page
    if(os.path.isfile(newchaptercoverdest)) :
        mangalogging.log_error(newchaptercoverdest + " already exists!!!")  
    else :
        try :
            mangalogging.log_info("Copy: " + newchapterpath + newchapterpages[0] + " to " + newchaptercoverdest)
            copyfile(newchapterpath + newchapterpages[0],newchaptercoverdest)
        except :
            mangalogging.log_error("ERROR: Unable to Copy " + newchapterpath + newchapterpages[0] + " to " + newchaptercoverdest)



def get_extension(chaptersrcpage) :
    mangalogging.log_debug("get_extension(" + chaptersrcpage + ")")
    #Gets the extension of any filename
    #handle for no extension found(folder path passed instead)
    return chaptersrcpage[chaptersrcpage.rfind('.'):]


#temp workaround
def get_manga(manga):
    mangalogging.log_debug("get_manga(" + manga + ")")
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