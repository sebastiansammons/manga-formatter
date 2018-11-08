import sys
import os
import shutil
from shutil import copyfile
import sqlite3
import mangaguilib

#Change these later
ROOTPATH = "/Users/Fridge/Documents/Python/MangaProj/Manga/MangaTest/"
QUEUESRC = "/Users/Fridge/Documents/Python/MangaProj/Manga/Formats/ChapterQueue/"
MANUALDEST = "/Users/Fridge/Documents/Python/MangaProj/Manga/Formats/Manual Destination/"
CHAPTERFORMATPATH = "/Chapter Pictures/Other Chapters/"
VOLUMEFORMATPATH = "/Chapter Pictures/Volume Chapters/"
OPCHAPTERCOVERPATH = "/Users/Fridge/Documents/Python/MangaProj/Manga/MangaTest/One Piece/Cover Pictures/"
MYSQLITEDB = '/Users/Fridge/Documents/Python/MangaProj/fridgemedia.db'



def sql_format_chapter(mangatitle,logtype) :
    #Create list of non-hidden files
    try :
        #Don't really need to "try" this since main already did it. But I guess it doesn't hurt
        chapterpages = [f for f in os.listdir(QUEUESRC) if not f.startswith('.')]
    except :
        mangaguilib.error_message("ERROR!! [" + QUEUESRC + "] NOT FOUND")
        exit()
    #Sort list
    chapterpages = sorted(chapterpages)
    #Get number of pages for the new chapter
    numpages = len(chapterpages)   
    #Connect to SQLite
    try :
        conn = sqlite3.connect(MYSQLITEDB)
    except :
        mangaguilib.error_message("CANNOT CONNECT TO fridgemedia.db")
        exit()
    c = conn.cursor()
    #Get current chapter number from SQLite and increment
    c.execute("Select curchap from manga where title = ?",(mangatitle,))
    sqldata = [tup[0] for tup in c.fetchall()]
    newchapternumber = sqldata[0] + 1
    #Create directory path for new chapter
    newchapterdir = ROOTPATH + mangatitle + CHAPTERFORMATPATH + str(newchapternumber).zfill(3) + "/"
    #Create new directory
    #Check if directory exists
    try :
        os.mkdir(newchapterdir)
    except :
        if(len([f for f in os.listdir(newchapterdir) if not f.startswith('.')])==0) :
            #Directory exists but nothing is in the folder
            pass
        else :
            mangaguilib.error_message("Error Creating Directory: " + newchapterdir)
            exit()
    #Get full source and destination paths for logs and format
    copylog = [None] * numpages
    pagesrc = [None] * numpages
    pagedest = [None] * numpages
    for i in range(0,numpages) :
        pagesrc[i]= QUEUESRC + str(chapterpages[i])
        #Get extension of current page file
        ext=get_extension(pagesrc[i])
        pagedest[i] = newchapterdir + mangatitle + " CH" + str(newchapternumber) +" PG" + str(i+1) + ext
        #Create log based on details wanted
        if(logtype=="Simple") :
            #Simple log
            copylog[i] = "/" + str(chapterpages[i]) + " to /" + mangatitle + " CH" + str(newchapternumber) + " PG" + str(i+1) + ext
        else :
            #Detailed log
            copylog[i] = pagesrc[i] + " to " + pagedest[i]
    #Show copy log
    mangaguilib.display_logs(copylog,logtype)
    #Commit format
    for i in range(0,numpages) :
        try :
            #print("COPY " + pagesrc[i] + " to " + pagedest[i])
            os.rename(pagesrc[i],pagedest[i])
        except :
            mangaguilib.error_message("ERROR copying: " + pagesrc[i] + " to " + pagedest[i])
            exit()
    #Update SQLite with new current chapter number
    c.execute("UPDATE manga set curchap = ? WHERE title = ?",(int(newchapternumber),mangatitle))
    #Check update
    c.execute("Select curchap from manga where title = ?",(mangatitle,))
    newsqldata = [tup[0] for tup in c.fetchall()]
    print("Updated sql curchap to: " + str(newsqldata[0]))
    #conn.commit()
    conn.close()
    #Make copy of chapter cover if One Piece is formatted
    if(mangatitle=="One Piece") :
        #print("One Piece Cover Copy: Currently not creating directories so I can't run this right now")            
        one_piece_cover_copy(newchapterdir,newchapternumber)



def sql_format_volume(mangatitle,lastchapter,logtype) :
    #Get volume cover page
    try :
        volumecoverdir = [f for f in os.listdir(QUEUESRC) if not f.startswith('.')]
    except :
        mangaguilib.error_message("ERROR!! [" + QUEUESRC + "] NOT FOUND")
        exit()
    #Make sure there is only 1 file in the directory (the cover)
    if(len(volumecoverdir)!=1) :
        mangaguilib.error_message("MORE THAN ONE FILE IN QUEUE. DON'T KNOW WHCH ONE IS VOLUME COVER")
        exit()
    #Connect to SQLite
    try :
        conn = sqlite3.connect(MYSQLITEDB)
    except :
        mangaguilib.error_message("CANNOT CONNECT TO fridgemedia.db")
        exit()
    c = conn.cursor()
    #Get current volume number from SQLite and increment
    c.execute("Select curvol from manga where title = ?",(mangatitle,))
    sqldata = [tup[0] for tup in c.fetchall()]
    newvolumenumber = sqldata[0] + 1
    #print("New Volume Number: " + str(newvolumenumber))
    #Get first chapter of new volume
    c.execute("Select fconv from manga where title = ?",(mangatitle,))
    sqldata = [tup[0] for tup in c.fetchall()]
    firstchap = sqldata[0]
    #print("First Chap of next volume: " + str(firstchap))
    #Make sure user entered a chapter number thats newer then the fconv
    if(int(lastchapter)<=firstchap) :
        mangaguilib.error_message("Last Chapter number < First chapter number!!!!")
        exit()
    #Create path for new chapter directory
    if(mangatitle=="One Piece") :
        newvolumedir = ROOTPATH + mangatitle + VOLUMEFORMATPATH + mangatitle + " Volume " + str(newvolumenumber).zfill(3) + "/"
    else :
        newvolumedir = ROOTPATH + mangatitle + VOLUMEFORMATPATH + mangatitle + " Volume " + str(newvolumenumber).zfill(2) + "/"
    #Create new directory (from new path just generated)
    #Check if directory exists
    try :
        os.mkdir(newvolumedir)
    except :
        if(len([f for f in os.listdir(newvolumedir) if not f.startswith('.')])==0) :
            #Directory exists but nothing is in the folder
            pass
        else :
            mangaguilib.error_message("Error Creating Directory: " + newvolumedir)
            exit()
    #Copy volume cover
    volumecoversrc = QUEUESRC + volumecoverdir[0]
    #Get extension of cover file
    ext=get_extension(volumecoversrc)   
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
        chapterdir[chapnum-firstchap] = ROOTPATH + mangatitle + CHAPTERFORMATPATH + str(chapnum).zfill(3) + "/"
        try :
            chapterpagesrc[chapnum-firstchap] = [f for f in os.listdir(chapterdir[chapnum-firstchap]) if not f.startswith('.')]
        except :
            mangaguilib.error_message("ERROR!! [" + chapterdir[chapnum-firstchap] + "] NOT FOUND")
            break
        #Sort the pages (not realy needed tbh)
        chapterpagesrc[chapnum-firstchap] = sorted(chapterpagesrc[chapnum-firstchap])
    #Create and show log
    if(logtype=="Simple") :
        copylog = [None] * numchapters
        for i in range(0,numchapters) :
            #Simple log
            copylog[i] = chapterdir[i].replace(ROOTPATH + mangatitle + CHAPTERFORMATPATH,"/")[:-1] + " to " + newvolumedir.replace(ROOTPATH + mangatitle + VOLUMEFORMATPATH,"/")[:-1]
    else :
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
    #Commit format
    mangaguilib.display_logs(copylog,logtype)
    for i in range(0,numchapters) :
        for j in range(0,len(chapterpagesrc[i])) :  
            try :
                #print("COPY " + chapterdir[i] + chapterpagesrc[i][j] + " to " + newvolumedir + chapterpagesrc[i][j])
                os.rename(chapterdir[i] + chapterpagesrc[i][j],newvolumedir + chapterpagesrc[i][j])
            except :
                mangaguilib.error_message("ERROR unable to copy: " + chapterdir[i] + chapterpagesrc[i][j] + " to " + newvolumedir + chapterpagesrc[i][j])
                exit()
        #Remove old chapter directories
        print("REMOVE: " + chapterdir[i])
        try :
            shutil.rmtree(chapterdir[i])
        except :
            mangaguilib.error_message("ERROR!! UNABLE TO REMOVE [" + chapterdir[i] + "] You need to manually remove it")            
    #Update SQLite with new current volume number
    c.execute("UPDATE manga set curvol = ? WHERE title = ?",(int(newvolumenumber),mangatitle))
    #check update
    c.execute("Select curvol from manga where title = ?",(mangatitle,))
    sqldata = [tup[0] for tup in c.fetchall()]
    print("Updated sql curvol to: " + str(sqldata[0]))
    #Update SQLite with new first chapter of new volume number
    c.execute("UPDATE manga set fconv = ? WHERE title = ?",(int(lastchapter) + 1,mangatitle))
    #check update
    c.execute("Select fconv from manga where title = ?",(mangatitle,))
    sqldata = [tup[0] for tup in c.fetchall()]
    print("Updated sql fconv to: " + str(sqldata[0]))
    #conn.commit()
    conn.close()



def manual_single_chapter(mangatitle,chapternumber,logtype) :
    #Create list of non-hidden filenames
    chapterpages = [f for f in os.listdir(QUEUESRC) if not f.startswith('.')]
    #Sort pages
    chapterpages = sorted(chapterpages)
    #Get number of pages for the new chapter
    numpages = len(chapterpages)   
    #Create new chapter directory
    newchapterdir = MANUALDEST + chapternumber.zfill(3) + "/"
    #Check if directory exists
    #print("Make Directory " + newchapterdir)
    try :
        os.mkdir(newchapterdir)
    except :
        if(len([f for f in os.listdir(newchapterdir) if not f.startswith('.')])==0) :
            #Directory exists but nothing is in the folder
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
        pagesrc[i]= QUEUESRC + str(chapterpages[i])
        #Get extension of current page file
        ext=get_extension(pagesrc[i])
        pagedest[i] = newchapterdir + mangatitle + " CH" + str(chapternumber) + " PG" + str(i+1) + ext
        #Create log based on details wanted
        if(logtype=="Simple") :
            #Simple log
            copylog[i] = "/" + str(chapterpages[i]) + " to /" + mangatitle + " CH" + str(chapternumber) + " PG" + str(i+1) + ext
        else :
            #Detailed log
            copylog[i] = pagesrc[i] + " to " + pagedest[i]
    #Show copy log
    mangaguilib.display_logs(copylog,logtype)
    #Commit format
    for i in range(0,numpages) :
        try :
            #print("COPY " + pagesrc[i] + " to " + pagedest[i])
            os.rename(pagesrc[i],pagedest[i])
        except :
            mangaguilib.error_message("ERROR copying: " + pagesrc[i] + " to " + pagedest[i])
            exit()



def manual_multiple_chapter(title,logtype) :
    #Assume QUESRC is formatted correctly
    #List of chapter directories
    chaptersrclist = [f for f in os.listdir(QUEUESRC) if not f.startswith('.')]
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
        chaptersrcdir[i] = QUEUESRC + chaptersrclist[i] + "/"
        #Get chapter destination directories
        chapterdestdir[i] = MANUALDEST + chaptersrclist[i].zfill(3) + "/"
        #Make chapter destination directories
        #print("Make Directory " + chapterdestdir[i])
        try :
            os.mkdir(chapterdestdir[i])
        except :
            if(len([f for f in os.listdir(chapterdestdir[i]) if not f.startswith('.')])==0) :
                #Directory exists but nothing is in the folder
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
            if(logtype=="Simple") :
                #Simple log
                copylog[logindex] = "/" + chapterpagesrc[i][j] + " to /" + chapterpagedest[i][j]
            else :
                #Detailed log
                copylog[logindex] = chaptersrcdir[i] + chapterpagesrc[i][j] + " to " + chapterdestdir[i] + chapterpagedest[i][j]
            logindex+=1
    #Commit format
    mangaguilib.display_logs(copylog,logtype)
    for i in range(0,numchapters) :
        for j in range(0,len(chapterpagesrc[i])) :  
            try :
                #print("COPY " + chaptersrcdir[i] + chapterpagesrc[i][j] + " to " + chapterdestdir[i] + chapterpagedest[i][j])
                os.rename(chaptersrcdir[i] + chapterpagesrc[i][j], chapterdestdir[i] + chapterpagedest[i][j])
            except :
                mangaguilib.error_message("ERROR unable to copy: " + chaptersrcdir[i] + chapterpagesrc[i][j] + " to " + chapterdestdir[i] + chapterpagedest[i][j])
                exit()
        #Remove old chapter directories
        print("REMOVE: " + chaptersrcdir[i])
        try :
            shutil.rmtree(chaptersrcdir[i])
        except :
            mangaguilib.error_message("ERROR!! UNABLE TO REMOVE [" + chaptersrcdir[i] + "] You need to manually remove it")            


def manual_format_volume(title,number,logtype) :
    manual_multiple_chapter(title,logtype)
    #Get list of chapters
    chapterdir = [f for f in os.listdir(MANUALDEST) if not f.startswith('.')]
    #Sort chaptersrc list
    chapterdir = sorted(chapterdir)
    numchapters = len(chapterdir)
    #list of each chapter page list (2D List)
    chapterpagesrc = [None] * numchapters
    #Get chapter destination directory path
    newvolumedir = MANUALDEST + title + " Volume " + str(number).zfill(2) + "/"
    #Make chapter destination directory
    #print("Make Directory " + newvolumedir)
    try :
       os.mkdir(newvolumedir)
    except :
        if(len([f for f in os.listdir(newvolumedir) if not f.startswith('.')])==0) :
            #Directory exists but nothing is in the folder
            pass
        else :
            mangaguilib.error_message("Error Creating Directory: " + newvolumedir)
            exit()
    #Get list of each chapter's page source
    for i in range(0,numchapters) :
        try :
            chapterpagesrc[i] = [f for f in os.listdir(MANUALDEST + chapterdir[i]) if not f.startswith('.')]
        except :
            mangaguilib.error_message("ERROR!! [" + MANUALDEST + chapterdir[i] + "] NOT FOUND")
            break
        #Sort the directory list (not realy needed tbh)
        chapterpagesrc[i] = sorted(chapterpagesrc[i])
    #Create and show log
    numcopy = 0
    if(logtype=="Simple") :
        #Simple log
        copylog = [None] * numchapters
        for i in range(0,numchapters) :
                copylog[i] = "/" + chapterdir[i] + " to " + "/Volume " + str(number).zfill(2)    
    else :
        #Detailed log
        for i in range(0,numchapters) :
            numcopy+=len(chapterpagesrc[i])
        copylog = [None] * numcopy
        logindex=0
        for i in range(0,numchapters) :
            for j in range(0,len(chapterpagesrc[i])) :       
                #print(MANUALDEST + chapterdir[i] + "/" + chapterpagesrc[i][j] + " to " + MANUALDEST + chapterpagesrc[i][j])
                copylog[logindex] = MANUALDEST + chapterdir[i] + "/" + chapterpagesrc[i][j] + " to " + newvolumedir + chapterpagesrc[i][j]
                logindex+=1
    #Commit format
    mangaguilib.display_logs(copylog,logtype)
    for i in range(0,numchapters) :
        for j in range(0,len(chapterpagesrc[i])) :  
            try :
                #print("COPY " + MANUALDEST + chapterdir[i] + "/" + chapterpagesrc[i][j] + " to " + newvolumedir + chapterpagesrc[i][j])
                os.rename(MANUALDEST + chapterdir[i] + "/" + chapterpagesrc[i][j],newvolumedir + chapterpagesrc[i][j])
            except :
                mangaguilib.error_message("ERROR unable to copy: " + MANUALDEST + chapterdir[i] + "/" + chapterpagesrc[i][j] + " to " + newvolumedir + chapterpagesrc[i][j])
                exit()
        #Remove old chapter directory
        print("REMOVE: " + MANUALDEST + chapterdir[i])
        try :
            shutil.rmtree(MANUALDEST + chapterdir[i])
        except :
            mangaguilib.error_message("ERROR!! UNABLE TO REMOVE [" + MANUALDEST + chapterdir[i] + "] You need to manually remove it")



def one_piece_cover_copy(newchapterpath,newchapternumber) :
    #Get cover page
    newchapterpages = [f for f in os.listdir(newchapterpath) if not f.startswith('.')]
    newchapterpages = sorted(newchapterpages)
    #Get extension of page file
    ext=get_extension(newchapterpages[0])
    newchaptercoverdest = OPCHAPTERCOVERPATH + "CH" + str(newchapternumber) + " Cover" + ext
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

