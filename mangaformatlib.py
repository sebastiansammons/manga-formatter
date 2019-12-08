import sys
import os
import shutil
from shutil import copyfile
import sqlite3
import mangaconfig
import mangaguilib

def sql_format_chapter(mangatitle) :
    #Create list of non-hidden files
    try :
        #Don't really need to "try" this since main already did it. But I guess it doesn't hurt
        chapterpages = [f for f in os.listdir(mangaconfig.QUEUESRC) if not f.startswith('.')]
    except :
        mangaguilib.error_message("ERROR!! [" + mangaconfig.QUEUESRC + "] NOT FOUND")
        exit()
    #Sort list
    chapterpages = sorted(chapterpages)
    #Get number of pages for the new chapter
    numpages = len(chapterpages)   
    #Connect to SQLite
    try :
        conn = sqlite3.connect(mangaconfig.MYSQLITEDB)
    except :
        mangaguilib.error_message("CANNOT CONNECT TO fridgemedia.db")
        exit()
    c = conn.cursor()
    #Get current chapter number from SQLite and increment
    c.execute("Select curchap from manga where title = ?",(mangatitle,))
    sqldata = [tup[0] for tup in c.fetchall()]
    newchapternumber = sqldata[0] + 1
    #Create directory path for new chapter
    newchapterdir = mangaconfig.ROOTPATH + mangatitle + mangaconfig.CHAPTERFORMATPATH + str(newchapternumber).zfill(3) + "/"
    #Create new directory
    #Check if directory exists
    try :
        os.mkdir(newchapterdir)
    except :
        if(len([f for f in os.listdir(newchapterdir) if not f.startswith('.')])==0) :
            #Directory exists but nothing is in it
            pass
        else :
            mangaguilib.error_message("Error Creating Directory: " + newchapterdir)
            exit()
    #Get full source and destination paths for logs and format
    copylog = [None] * numpages
    pagesrc = [None] * numpages
    pagedest = [None] * numpages
    for i in range(0,numpages) :
        pagesrc[i]= mangaconfig.QUEUESRC + str(chapterpages[i])
        #Get extension of current page file
        ext=get_extension(pagesrc[i])
        pagedest[i] = newchapterdir + mangatitle + " CH" + str(newchapternumber) +" PG" + str(i+1) + ext
        #Create log based on details wanted
        if(mangaconfig.LOGTYPE=="Simple") :
            #Simple log
            copylog[i] = "/" + str(chapterpages[i]) + " to /" + mangatitle + " CH" + str(newchapternumber) + " PG" + str(i+1) + ext
        elif(mangaconfig.LOGTYPE=="Detailed"):
            #Detailed log
            copylog[i] = pagesrc[i] + " to " + pagedest[i]
    #Show copy log
    mangaguilib.display_logs(copylog)
    #Abort format?
        #Currentyl if user selects "ABORT" in the GUI, the directory for the new chapter is still there. If the user selects "ABORT" it should be removed. Here is where we would chagne that
    #Commit format
    for i in range(0,numpages) :
        try :
            os.rename(pagesrc[i],pagedest[i])
        except :
            mangaguilib.error_message("ERROR copying: " + pagesrc[i] + " to " + pagedest[i])
            exit()
    #Update SQLite with new current chapter number
    c.execute("UPDATE manga set curchap = ? WHERE title = ?",(int(newchapternumber),mangatitle))
    #Check update
    c.execute("Select curchap from manga where title = ?",(mangatitle,))
    newsqldata = [tup[0] for tup in c.fetchall()]
    conn.commit()
    conn.close()
    #Make copy of chapter cover if One Piece is formatted
    if(mangatitle=="One Piece") :
        one_piece_cover_copy(newchapterdir,newchapternumber)



def sql_format_volume(mangatitle,lastchapter) :
    #Get volume cover page
    try :
        volumecoverdir = [f for f in os.listdir(mangaconfig.QUEUESRC) if not f.startswith('.')]
    except :
        mangaguilib.error_message("ERROR!! [" + mangaconfig.QUEUESRC + "] NOT FOUND")
        exit()
    #Make sure there is only 1 file in the directory (the cover)
    if(len(volumecoverdir)!=1) :
        mangaguilib.error_message("MORE THAN ONE FILE IN QUEUE. DON'T KNOW WHCH ONE IS VOLUME COVER")
        exit()
    #Connect to SQLite
    try :
        conn = sqlite3.connect(mangaconfig.MYSQLITEDB)
    except :
        mangaguilib.error_message("CANNOT CONNECT TO fridgemedia.db")
        exit()
    c = conn.cursor()
    #Get current volume number from SQLite and increment
    c.execute("Select curvol from manga where title = ?",(mangatitle,))
    sqldata = [tup[0] for tup in c.fetchall()]
    newvolumenumber = sqldata[0] + 1
    #Get first chapter of new volume
    c.execute("Select fconv from manga where title = ?",(mangatitle,))
    sqldata = [tup[0] for tup in c.fetchall()]
    firstchap = sqldata[0]
    #Make sure user entered a chapter number thats newer then the fconv
    if(int(lastchapter)<=firstchap) :
        mangaguilib.error_message("Last Chapter number < First chapter number!!!!")
        exit()
    #Create path for new chapter directory
    if(mangatitle=="One Piece") :
        newvolumedir = mangaconfig.ROOTPATH + mangatitle + mangaconfig.VOLUMEFORMATPATH + mangatitle + " Volume " + str(newvolumenumber).zfill(3) + "/"
    else :
        newvolumedir = mangaconfig.ROOTPATH + mangatitle + mangaconfig.VOLUMEFORMATPATH + mangatitle + " Volume " + str(newvolumenumber).zfill(2) + "/"
    #Create new directory (from new path just generated)
    #Check if directory exists
    try :
        os.mkdir(newvolumedir)
    except :
        if(len([f for f in os.listdir(newvolumedir) if not f.startswith('.')])==0) :
            #Directory exists but nothing is in it
            pass
        else :
            mangaguilib.error_message("Error Creating Directory: " + newvolumedir)
            exit()
    #Copy volume cover
    volumecoversrc = mangaconfig.QUEUESRC + volumecoverdir[0]
    #Get extension of cover file
    ext=get_extension(volumecoversrc)   
    if(mangatitle=="One Piece") :
        volumecoverdest = newvolumedir + mangatitle + " " + str(newvolumenumber).zfill(3) + ext
    else :
        volumecoverdest = newvolumedir + mangatitle + " " + str(newvolumenumber).zfill(2) + ext
    coverlog = "Copy" + volumecoversrc + " to " + volumecoverdest
    #make a pop up for this?
    print(coverlog)
    #Format cover
    try :
        os.rename(volumecoversrc,volumecoverdest)
    except :
        mangaguilib.error_message("ERROR making cover page")
        exit()
    #Move chapters
    numchapters = int(lastchapter) - firstchap + 1
    #List of chapter directories
    chapterdir = [None] * numchapters
    #list of each chapter page list (2D List)
    chapterpagesrc = [None] * numchapters
    for chapnum in range(firstchap,int(lastchapter) + 1) :
        #Get chapnum's directory and get the list of pages within the directory
        chapterdir[chapnum-firstchap] = mangaconfig.ROOTPATH + mangatitle + mangaconfig.CHAPTERFORMATPATH + str(chapnum).zfill(3) + "/"
        try :
            chapterpagesrc[chapnum-firstchap] = [f for f in os.listdir(chapterdir[chapnum-firstchap]) if not f.startswith('.')]
        except :
            mangaguilib.error_message("ERROR!! [" + chapterdir[chapnum-firstchap] + "] NOT FOUND")
            break
        #Sort the pages (not realy needed tbh)
        chapterpagesrc[chapnum-firstchap] = sorted(chapterpagesrc[chapnum-firstchap])
    #Create and show log
    if(mangaconfig.LOGTYPE=="Simple") :
        copylog = [None] * numchapters
        for i in range(0,numchapters) :
            #Simple log
            copylog[i] = chapterdir[i].replace(mangaconfig.ROOTPATH + mangatitle + mangaconfig.CHAPTERFORMATPATH,"/")[:-1] + " to " + newvolumedir.replace(mangaconfig.ROOTPATH + mangatitle + mangaconfig.VOLUMEFORMATPATH,"/")[:-1]
    elif(mangaconfig.LOGTYPE=="Detailed"):
        #Detailed log
        numcopylog = 0
        for i in range(0,numchapters) :
            numcopylog+=len(chapterpagesrc[i])
        copylog = [None] * numcopylog
        logindex = 0
        for i in range(0,numchapters) :
            for j in range(0,len(chapterpagesrc[i])) :
                copylog[logindex] = chapterdir[i] + chapterpagesrc[i][j] + " to " + newvolumedir + chapterpagesrc[i][j]
                logindex+=1
    mangaguilib.display_logs(copylog)
    #Abort format?
        #Things need to get done if user decides to abort. Will work on later
    #Commit format
    for i in range(0,numchapters) :
        for j in range(0,len(chapterpagesrc[i])) :  
            try :
                os.rename(chapterdir[i] + chapterpagesrc[i][j],newvolumedir + chapterpagesrc[i][j])
            except :
                mangaguilib.error_message("ERROR unable to copy: " + chapterdir[i] + chapterpagesrc[i][j] + " to " + newvolumedir + chapterpagesrc[i][j])
                exit()
        #Remove old chapter directories
        try :
            shutil.rmtree(chapterdir[i])
        except :
            mangaguilib.error_message("ERROR!! UNABLE TO REMOVE [" + chapterdir[i] + "] You need to manually remove it")            
    #Update SQLite with new current volume number
    c.execute("UPDATE manga set curvol = ? WHERE title = ?",(int(newvolumenumber),mangatitle))
    #check update
    c.execute("Select curvol from manga where title = ?",(mangatitle,))
    sqldata = [tup[0] for tup in c.fetchall()]
    #Update SQLite with new first chapter of new volume number
    c.execute("UPDATE manga set fconv = ? WHERE title = ?",(int(lastchapter) + 1,mangatitle))
    #check update
    c.execute("Select fconv from manga where title = ?",(mangatitle,))
    sqldata = [tup[0] for tup in c.fetchall()]
    conn.commit()
    conn.close()



def manual_single_chapter(mangatitle,chapternumber) :
    #Create list of non-hidden filenames
    chapterpages = [f for f in os.listdir(mangaconfig.QUEUESRC) if not f.startswith('.')]
    #Sort pages
    chapterpages = sorted(chapterpages)
    #Get number of pages for the new chapter
    numpages = len(chapterpages)   
    #Create new chapter directory
    newchapterdir = mangaconfig.MANUALDEST + chapternumber.zfill(3) + "/"
    #Check if directory exists
    try :
        os.mkdir(newchapterdir)
    except :
        if(len([f for f in os.listdir(newchapterdir) if not f.startswith('.')])==0) :
            #Directory exists but nothing is in it
            pass
        else :
            mangaguilib.error_message("Error Creating Direcotry: " + newchapterdir)
            exit()
    #Get full source and destination paths for logs and format
    copylog = [None] * numpages
    pagesrc = [None] * numpages
    pagedest = [None] * numpages
    for i in range(0,numpages) :
        #Singe chapter so queue should just be the pages
        pagesrc[i]= mangaconfig.QUEUESRC + str(chapterpages[i])
        #Get extension of current page file
        ext=get_extension(pagesrc[i])
        pagedest[i] = newchapterdir + mangatitle + " CH" + str(chapternumber) + " PG" + str(i+1) + ext
        #Create log based on details wanted
        if(mangaconfig.LOGTYPE=="Simple") :
            #Simple log
            copylog[i] = "/" + str(chapterpages[i]) + " to /" + mangatitle + " CH" + str(chapternumber) + " PG" + str(i+1) + ext
        elif(mangaconfig.LOGTYPE=="Detailed"):
            #Detailed log
            copylog[i] = pagesrc[i] + " to " + pagedest[i]
    #Show copy log
    mangaguilib.display_logs(copylog)
    #Abort format?
        #Currentyl if user selects "ABORT" in the GUI, the directory for the new chapter is still there. If the user selects "ABORT" it should be removed. Here is where we would chagne that
    #Commit format
    for i in range(0,numpages) :
        try :
            os.rename(pagesrc[i],pagedest[i])
        except :
            mangaguilib.error_message("ERROR copying: " + pagesrc[i] + " to " + pagedest[i])
            exit()



def manual_multiple_chapter(title) :
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
            os.mkdir(chapterdestdir[i])
        except :
            if(len([f for f in os.listdir(chapterdestdir[i]) if not f.startswith('.')])==0) :
                #Directory exists but nothing is in it
                pass
            else :
                mangaguilib.error_message("Error Creating Directory: " + chapterdestdir[i])
                exit()    
    for i in range(0,numchapters) :
        #Get pages for each chapter
        try :
            curchapterpages = [f for f in os.listdir(chaptersrcdir[i]) if not f.startswith('.')]
            curchapterpages = [f for f in os.listdir(chaptersrcdir[i]) if not f.startswith('.')]
        except :
            mangaguilib.error_message("ERROR!! [" + chaptersrcdir[i] + "] NOT FOUND")
            break
        #Sort the chapter pages (not realy needed tbh)
        curchapterpages = sorted(curchapterpages)
        #Create list for each chapter
        chapterpagesrc[i] = [None] * len(curchapterpages)
        chapterpagedest[i] = [None] * len(curchapterpages)
        #Get each source path and destination format path for each page
        for j in range(0,len(curchapterpages)) :
            chapterpagesrc[i][j] = curchapterpages[j]
            chapterpagedest[i][j] = title + " CH" + chaptersrclist[i].lstrip("0") + " PG" + str(j+1) + get_extension(curchapterpages[j])
    #Create and show log
    numcopylog = 0
    for i in range(0,numchapters) :
        numcopylog+=len(chapterpagesrc[i])
    copylog = [None] * numcopylog
    logindex = 0
    for i in range(0,numchapters) :
        for j in range(0,len(chapterpagesrc[i])) :
            if(mangaconfig.LOGTYPE=="Simple") :
                #Simple log
                copylog[logindex] = "/" + chapterpagesrc[i][j] + " to /" + chapterpagedest[i][j]
            elif(mangaconfig.LOGTYPE=="Detailed"):
                #Detailed log
                copylog[logindex] = chaptersrcdir[i] + chapterpagesrc[i][j] + " to " + chapterdestdir[i] + chapterpagedest[i][j]
            logindex+=1
    mangaguilib.display_logs(copylog)
    #Abort format?
        #Something has to done when user selects abort format. Will deal with later
    #Commit format
    for i in range(0,numchapters) :
        for j in range(0,len(chapterpagesrc[i])) :  
            try :
                os.rename(chaptersrcdir[i] + chapterpagesrc[i][j], chapterdestdir[i] + chapterpagedest[i][j])
            except :
                mangaguilib.error_message("ERROR unable to copy: " + chaptersrcdir[i] + chapterpagesrc[i][j] + " to " + chapterdestdir[i] + chapterpagedest[i][j])
                exit()
        #Remove old chapter directories
        try :
            shutil.rmtree(chaptersrcdir[i])
        except :
            mangaguilib.error_message("ERROR!! UNABLE TO REMOVE [" + chaptersrcdir[i] + "] You need to manually remove it")            


def manual_format_volume(title,number) :
    manual_multiple_chapter(title)
    #Get list of chapters
    chapterdir = [f for f in os.listdir(mangaconfig.MANUALDEST) if not f.startswith('.')]
    #Sort chaptersrc list
    chapterdir = sorted(chapterdir)
    numchapters = len(chapterdir)
    #list of each chapter page list (2D List)
    chapterpagesrc = [None] * numchapters
    #Get chapter destination directory path
    newvolumedir = mangaconfig.MANUALDEST + title + " Volume " + str(number).zfill(2) + "/"
    #Make chapter destination directory
    try :
       os.mkdir(newvolumedir)
    except :
        if(len([f for f in os.listdir(newvolumedir) if not f.startswith('.')])==0) :
            #Directory exists but nothing is in it
            pass
        else :
            mangaguilib.error_message("Error Creating Directory: " + newvolumedir)
            exit()
    #Get list of each chapter's page source
    for i in range(0,numchapters) :
        try :
            chapterpagesrc[i] = [f for f in os.listdir(mangaconfig.MANUALDEST + chapterdir[i]) if not f.startswith('.')]
        except :
            mangaguilib.error_message("ERROR!! [" + mangaconfig.MANUALDEST + chapterdir[i] + "] NOT FOUND")
            break
        #Sort the directory list (not realy needed tbh)
        chapterpagesrc[i] = sorted(chapterpagesrc[i])
    #Create and show log
    numcopy = 0
    if(mangaconfig.LOGTYPE=="Simple") :
        #Simple log
        copylog = [None] * numchapters
        for i in range(0,numchapters) :
                copylog[i] = "/" + chapterdir[i] + " to " + "/Volume " + str(number).zfill(2)    
    elif(mangaconfig.LOGTYPE=="Detailed"):
        #Detailed log
        for i in range(0,numchapters) :
            numcopy+=len(chapterpagesrc[i])
        copylog = [None] * numcopy
        logindex=0
        for i in range(0,numchapters) :
            for j in range(0,len(chapterpagesrc[i])) :       
                copylog[logindex] = mangaconfig.MANUALDEST + chapterdir[i] + "/" + chapterpagesrc[i][j] + " to " + newvolumedir + chapterpagesrc[i][j]
                logindex+=1
    mangaguilib.display_logs(copylog)
    #Abort format?
        #Something has to done when user selects abort format. Will deal with later
    #Commit format
    for i in range(0,numchapters) :
        for j in range(0,len(chapterpagesrc[i])) :  
            try :
                os.rename(mangaconfig.MANUALDEST + chapterdir[i] + "/" + chapterpagesrc[i][j],newvolumedir + chapterpagesrc[i][j])
            except :
                mangaguilib.error_message("ERROR unable to copy: " + mangaconfig.MANUALDEST + chapterdir[i] + "/" + chapterpagesrc[i][j] + " to " + newvolumedir + chapterpagesrc[i][j])
                exit()
        #Remove old chapter directory
        try :
            shutil.rmtree(mangaconfig.MANUALDEST + chapterdir[i])
        except :
            mangaguilib.error_message("ERROR!! UNABLE TO REMOVE [" + mangaconfig.MANUALDEST + chapterdir[i] + "] You need to manually remove it")



def one_piece_cover_copy(newchapterpath,newchapternumber) :
    #Get cover page
    newchapterpages = [f for f in os.listdir(newchapterpath) if not f.startswith('.')]
    newchapterpages = sorted(newchapterpages)
    #Get extension of page file
    ext=get_extension(newchapterpages[0])
    newchaptercoverdest = mangaconfig.OPCHAPTERCOVERPATH + "CH" + str(newchapternumber) + " Cover" + ext
    #Copy cover page
    if(os.path.isfile(newchaptercoverdest)) :
        mangaguilib.error_message(newchaptercoverdest + " already exists!!!")  
    else :
        try :
            copyfile(newchapterpath + newchapterpages[0],newchaptercoverdest)
        except :
            mangaguilib.error_message("ERROR: Unable to Copy " + newchapterpath + newchapterpages[0] + " to " + newchaptercoverdest)



def get_extension(chaptersrcpage) :
    #Gets the extension of any filename
    ext=chaptersrcpage[chaptersrcpage.rfind('.'):]
    return ext
