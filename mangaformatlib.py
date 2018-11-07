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
    #Create list of non-hidden filenames
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
    #Get Current Chapter number from SQLite and increment
    c.execute("Select curchap from manga where title = ?",(mangatitle,))
    sqldata = [tup[0] for tup in c.fetchall()]
    newchapternumber = sqldata[0] + 1
    #Create path for new chapter directory
    #Make a One Piece case?
    newchapterdir = ROOTPATH + mangatitle + CHAPTERFORMATPATH + str(newchapternumber).zfill(3) + "/"
    #Create new directory (from new path just generated)
    #Check if directory exists
    #try :
    #    os.mkdir(newchapterdir)
    #except :
        #might be error with path, not just existing already deal with later
    #    print(newchapterdir + " Exists")    
    #    if(len([f for f in os.listdir(newchapterdir) if not f.startswith('.')])>0) :
    #        mangaguilib.error_message("Chapter already formatted? ABORT!")
    #        exit()
    #    else :
    #        pass
    copylog = [None] * numpages
    pagesrc = [None] * numpages
    pagedest = [None] * numpages
    #get full source and destination paths for copy & log
    for i in range(0,numpages) :
        pagesrc[i]= QUEUESRC + str(chapterpages[i])
        #Get extension of current source page file
        ext=get_extension(pagesrc[i])
        pagedest[i] = newchapterdir + mangatitle + " CH" + str(newchapternumber) +" PG" + str(i+1) + ext
        #toggle to pick detailed or simple log?
        if(logtype=="Simple") :
            #Simple log
            copylog[i] = "/" + str(chapterpages[i]) + " to /" + mangatitle + " CH" + str(newchapternumber) + " PG" + str(i+1) + ext
        else :
            #detailed log
            copylog[i] = pagesrc[i] + " to " + pagedest[i]
    #print copy log & confirm format
    mangaguilib.display_logs(copylog,logtype)
    #Commit Format
    for i in range(0,numpages) :
        try :
            print("COPY " + pagesrc[i] + " to " + pagedest[i])
            #os.rename(pagesrc[i],pagedest[i])
        except :
            mangaguilib.error_message("ERROR copying: " + pagesrc[i] + " to " + pagedest[i])
            exit()
    #update sql with new current chapter number
    c.execute("UPDATE manga set curchap = ? WHERE title = ?",(int(newchapternumber),mangatitle))
    #check update
    c.execute("Select curchap from manga where title = ?",(mangatitle,))
    newsqldata = [tup[0] for tup in c.fetchall()]
    print("Updated sql curchap to: " + str(newsqldata[0]))
    #conn.commit()
    conn.close()
    #Check if Title is One Piece
    if(mangatitle=="One Piece") :
        print("One Piece Cover Copy: Currently not creating directories so I can't run this right now")            
        #one_piece_cover_copy(newchapterdir,newchapternumber)



def sql_format_volume(mangatitle,lastchapter,logtype) :
    #Get Cover page file
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
    #Get Current Volume number from SQLite and increment
    c.execute("Select curvol from manga where title = ?",(mangatitle,))
    sqldata = [tup[0] for tup in c.fetchall()]
    newvolumenumber = sqldata[0] + 1
    print("New Volume Number: " + str(newvolumenumber))
    #Get first chapter of new volume
    c.execute("Select fconv from manga where title = ?",(mangatitle,))
    sqldata = [tup[0] for tup in c.fetchall()]
    firstchap = sqldata[0]
    print("First Chap of next volume: " + str(firstchap))
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
    #try :
    #    os.mkdir(newvolumedir)
    #except :
    #    #possible newvolumedir isn't valid instead of already existing check later
    #    print(newvolumedir + " Exists")
    #    if(len([f for f in os.listdir(newvolumedir) if not f.startswith('.')])>0) :     
    #        print("Volume already formatted? ABORT!")
    #        exit()
    #    else :
    #        pass
    #Copy Volume Cover
    volumecoversrc = QUEUESRC + volumecoverdir[0]
    #Get extension of source file
    ext=get_extension(volumecoversrc)   
    volumecoverdest = newvolumedir + mangatitle + " " + str(newvolumenumber) + ext ##add leading zeros?
    coverlog = "Copy" + volumecoversrc + " to " + volumecoverdest
    #make a pop up for this?
    print(coverlog)
    #Format cover
    #try :
    #    os.rename(volumecoversrc,volumecoverdest)
    #except :
    #    mangaguilib.error_message("ERROR making cover page")
    #    exit()
    #Move chapters
    numchapters = int(lastchapter) - firstchap + 1
    #each chapter directory path
    chapterdir = [None] * numchapters
    #list of each chapter page src list (2D List)
    chapterpagesrc = [None] * numchapters
    for chapnum in range(firstchap,int(lastchapter) + 1) :
        #get this chapnum's directory + create list of pages in that directory
        chapterdir[chapnum-firstchap] = ROOTPATH + mangatitle + CHAPTERFORMATPATH + str(chapnum).zfill(3) + "/"
        try :
            curchapterpages = [f for f in os.listdir(chapterdir[chapnum-firstchap]) if not f.startswith('.')]
            #?chapterpagesrc[i] = [f for f in os.listdir(chapterdir[chapnum-firstchap]) if not f.startswith('.')]
        except :
            mangaguilib.error_message("ERROR!! [" + chapterdir[chapnum-firstchap] + "] NOT FOUND")
            break
        #sort the directory list (not realy needed tbh)
        curchapterpages = sorted(curchapterpages)
        #?chapterpagesrc[i] = sorted(chapterpagesrc[i])
        #DONT?
        #create list for this chapnum's filenames
        chapterpagesrc[chapnum-firstchap] = [None] * len(curchapterpages)
        #get each chapter page filename
        for i in range(0,len(curchapterpages)) :
            chapterpagesrc[chapnum-firstchap][i] = curchapterpages[i]
        #NEED?
    #Create & show log
    if(logtype=="Simple") :
        copylog = [None] * numchapters
        for i in range(0,numchapters) :
            #Simple log
            copylog[i] = chapterdir[i].replace(ROOTPATH + mangatitle + CHAPTERFORMATPATH,"/")[:-1] + " to " + newvolumedir.replace(ROOTPATH + mangatitle + VOLUMEFORMATPATH,"/")[:-1]
    else :
        numcopylog = 0
        for i in range(0,numchapters) :
            numcopylog+=len(chapterpagesrc[i])
        copylog = [None] * numcopylog
        logindex = 0
        #increment each chapter
        for i in range(0,numchapters) :
            #increment each page in the chapter
            for j in range(0,len(chapterpagesrc[i])) :
                #detailed log
                copylog[logindex] = chapterdir[i] + chapterpagesrc[i][j] + " to " + newvolumedir + chapterpagesrc[i][j]
                logindex+=1
    #Confirm & Format
    mangaguilib.display_logs(copylog,logtype)
    #increment each chapter
    for i in range(0,numchapters) :
        #increment each page in the chapter
        for j in range(0,len(chapterpagesrc[i])) :  
            try :
                print("COPY " + chapterdir[i] + chapterpagesrc[i][j] + " to " + newvolumedir + chapterpagesrc[i][j])
                #os.rename(chapterdir[i] + chapterpagesrc[i][j],newvolumedir + chapterpagesrc[i][j])
            except :
                mangaguilib.error_message("ERROR unable to copy: " + chapterdir[i] + chapterpagesrc[i][j] + " to " + newvolumedir + chapterpagesrc[i][j])
                exit()
        #remove old chapter directory
        print("REMOVE: " + chapterdir[i])
        #try :
        #    shutil.rmtree(chapterdir[i])
        #except :
        #    mangaguilib.error_message("ERROR!! UNABLE TO REMOVE [" + chapterdir[i] + "] You need to manually remove it")            
    #updatesql curvol + fconv
    #update sql with new current chapter number
    c.execute("UPDATE manga set curvol = ? WHERE title = ?",(int(newvolumenumber),mangatitle))
    #check update
    c.execute("Select curvol from manga where title = ?",(mangatitle,))
    sqldata = [tup[0] for tup in c.fetchall()]
    print("Updated sql curvol to: " + str(sqldata[0]))
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
    #Sort chaptersrc list
    chapterpages = sorted(chapterpages)
    #Get number of pages in new chapter
    numpages = len(chapterpages)   
    #Create path for new chapter directory (Keep in same directory)
    newchapterdir = MANUALDEST + chapternumber.zfill(3) + "/"
    #Create new directory (from new path just generated)
    #Check if directory exists
    print("Make Directory " + newchapterdir)
    #try :
    #    os.mkdir(newchapterdir)
    #except :
    #    print(newchapterdir + " Exists")
    #    if(len([f for f in os.listdir(newchapterdir) if not f.startswith('.')])>0) :
    #        mangaguilib.error_message("Chapter already formatted? ABORT!")
    #        exit()
    #    else :
    #        pass
    copylog = [None] * numpages
    pagesrc = [None] * numpages
    pagedest = [None] * numpages
    #Move & format new chapter
    for i in range(0,numpages) :
        #Singe Chapter so Queue Should just be the pages
        pagesrc[i]= QUEUESRC + str(chapterpages[i])
        #Get extension of current source page file
        ext=get_extension(pagesrc[i])
        pagedest[i] = newchapterdir + mangatitle + " CH" + str(chapternumber) + " PG" + str(i+1) + ext
        if(logtype=="Simple") :
            #Simple log
            copylog[i] = "/" + str(chapterpages[i]) + " to /" + mangatitle + " CH" + str(chapternumber) + " PG" + str(i+1) + ext
        else :
            #detailed log
            copylog[i] = pagesrc[i] + " to " + pagedest[i]
    #print copy log & confirm format
    mangaguilib.display_logs(copylog,logtype)
    #Commit Format
    for i in range(0,numpages) :
        try :
            print("COPY " + pagesrc[i] + " to " + pagedest[i])
            #os.rename(pagesrc[i],pagedest[i])
        except :
            mangaguilib.error_message("ERROR copying: " + pagesrc[i] + " to " + pagedest[i])
            exit()

#Fix Comments + variable names later
def manual_multiple_chapter(title,logtype) :
    #Assume QUESRC is formatted correctly
    #Create list of directories? filenames
    chaptersrclist = [f for f in os.listdir(QUEUESRC) if not f.startswith('.')]
    #Sort chaptersrc list
    chaptersrclist = sorted(chaptersrclist)
    #Get number of pages in new chapter
    numchapters = len(chaptersrclist)   
    #Src Directory path
    chaptersrcdir = [None] * numchapters
    #Dest Directory Path
    chapterdestdir = [None] * numchapters
    #Full path of all page sources
    chapterpagesrc = [None] * numchapters
    #FUll path of all page destinations
    chapterpagedest = [None] * numchapters
    #Get Source & Destination Directories
    for i in range(0,numchapters) :
        print("-" + chaptersrclist[i] + "-")
        #Get Chapter Source Directory path
        chaptersrcdir[i] = QUEUESRC + chaptersrclist[i] + "/"
        #Get Chapter Destination Directory path
        chapterdestdir[i] = MANUALDEST + chaptersrclist[i] + "/"
        #Make Chapter Destination Directory
        print("Make Directory " + chapterdestdir[i])
    #    try :
    #        os.mkdir(chapterdestdir[i])
    #   except :
    #        print(chapterdestdir[i] + " Exists")
    #        if(len([f for f in os.listdir(chapterdestdir[i]) if not f.startswith('.')])>0) :
    #            mangaguilib.error_message("Chapter already formatted? ABORT!")
    #            exit()
    #        else :
    #            pass
    for i in range(0,numchapters) :
        #Get List of current chapter source pages
        try :
            curchapterpages = [f for f in os.listdir(chaptersrcdir[i]) if not f.startswith('.')]
        except :
            mangaguilib.error_message("ERROR!! [" + chaptersrcdir[i] + "] NOT FOUND")
            break
        #sort the directory list (not realy needed tbh)
        curchapterpages = sorted(curchapterpages)
        #create list for this chapnum's filenames
        chapterpagesrc[i] = [None] * len(curchapterpages)
        chapterpagedest[i] = [None] * len(curchapterpages)
        #get each src and dest chapter page filename
        for j in range(0,len(curchapterpages)) :
            chapterpagesrc[i][j] = curchapterpages[j]
            chapterpagedest[i][j] = title + " CH" + chaptersrclist[i].lstrip("0") + " PG" + str(j+1) + get_extension(curchapterpages[j])
    numcopylog = 0
    for i in range(0,numchapters) :
        numcopylog+=len(chapterpagesrc[i])
    copylog = [None] * numcopylog
    logindex = 0
    for i in range(0,numchapters) :
        for j in range(0,len(chapterpagesrc[i])) :
            if(logtype=="Simple") :
                copylog[logindex] = "/" + chapterpagesrc[i][j] + " to /" + chapterpagedest[i][j]
            else :     
               copylog[logindex] = chaptersrcdir[i] + chapterpagesrc[i][j] + " to " + chapterdestdir[i] + chapterpagedest[i][j]
            logindex+=1
    #Confirm & Format
    mangaguilib.display_logs(copylog,logtype)
    #increment each chapter
    for i in range(0,numchapters) :
        #increment each page in the chapter
        for j in range(0,len(chapterpagesrc[i])) :  
            try :
                print("COPY " + chaptersrcdir[i] + chapterpagesrc[i][j] + " to " + chapterdestdir[i] + chapterpagedest[i][j])
                #os.rename(chaptersrcdir[i] + chapterpagesrc[i][j], chapterdestdir[i] + chapterpagedest[i][j])
            except :
                mangaguilib.error_message("ERROR unable to copy: " + chaptersrcdir[i] + chapterpagesrc[i][j] + " to " + chapterdestdir[i] + chapterpagedest[i][j])
                exit()
        #remove old chapter directory
        print("REMOVE: " + chaptersrcdir[i])
        #try :
        #    shutil.rmtree(chaptersrcdir[i])
        #except :
        #    mangaguilib.error_message("ERROR!! UNABLE TO REMOVE [" + chaptersrcdir[i] + "] You need to manually remove it")            

    
def manual_format_volume(title,number,logtype) :
    manual_multiple_chapter(title,logtype)
    #Get list of chapters
    chapterdir = [f for f in os.listdir(MANUALDEST) if not f.startswith('.')]
    #Sort chaptersrc list
    chapterdir = sorted(chapterdir)
    numchapters = len(chapterdir)
    #list of each chapter page src list (2D List)
    chapterpagesrc = [None] * numchapters
    #Get Chapter Destination Directory path
    newvolumedir = MANUALDEST + "Volume " + str(number).zfill(2) + "/"
    #Make Chapter Destination Directory
    print("Make Directory " + newvolumedir)
    #try :
    #   os.mkdir(newvolumedir)
    #except :
    #    print(newvolumedir + " Exists")
    #    if(len([f for f in os.listdir(newvolumedir) if not f.startswith('.')])>0) :
    #        mangaguilib.error_message("Chapter already formatted? ABORT!")
    #        exit()
    #    else :
    #        pass
    for i in range(0,numchapters) :
        try :
            chapterpagesrc[i] = [f for f in os.listdir(MANUALDEST + chapterdir[i]) if not f.startswith('.')]
        except :
            mangaguilib.error_message("ERROR!! [" + MANUALDEST + chapterdir[i] + "] NOT FOUND")
            break
        #sort the directory list (not realy needed tbh)
        chapterpagesrc[i] = sorted(chapterpagesrc[i])
    numcopy = 0
    if(logtype=="Simple") :
        copylog = [None] * numchapters
        for i in range(0,numchapters) :
                copylog[i] = "/" + chapterdir[i] + " to " + "/Volume " + str(number).zfill(2)    
    else :
        for i in range(0,numchapters) :
            numcopy+=len(chapterpagesrc[i])
        copylog = [None] * numcopy
        logindex=0
        for i in range(0,numchapters) :
            for j in range(0,len(chapterpagesrc[i])) :       
                #print(MANUALDEST + chapterdir[i] + "/" + chapterpagesrc[i][j] + " to " + MANUALDEST + chapterpagesrc[i][j])
                copylog[logindex] = MANUALDEST + chapterdir[i] + "/" + chapterpagesrc[i][j] + " to " + newvolumedir + chapterpagesrc[i][j]
                logindex+=1
    mangaguilib.display_logs(copylog,logtype)
    #increment each chapter
    for i in range(0,numchapters) :
        #increment each page in the chapter
        for j in range(0,len(chapterpagesrc[i])) :  
            try :
                print("COPY " + MANUALDEST + chapterdir[i] + "/" + chapterpagesrc[i][j] + " to " + newvolumedir + chapterpagesrc[i][j])
                #os.rename(chapterdir[i] + chapterpagesrc[i][j],newvolumedir + chaptersrc[i][j])
            except :
                mangaguilib.error_message("ERROR unable to copy: " + MANUALDEST + chapterdir[i] + "/" + chapterpagesrc[i][j] + " to " + newvolumedir + chapterpagesrc[i][j])
                exit()
        #remove old chapter directory
        print("REMOVE: " + MANUALDEST + chapterdir[i])
        #try :
        #    shutil.rmtree(chapterdir[i])
        #except :
        #    mangaguilib.error_message("ERROR!! UNABLE TO REMOVE [" + chapterdir[i] + "] You need to manually remove it")

#need to *fix* later (find cases)
#check if file is already there
def one_piece_cover_copy(newchapterpath,newchapternumber) :
    #get cover page
    newchapterpages = [f for f in os.listdir(newchapterpath) if not f.startswith('.')]
    newchapterpages = sorted(newchapterpages)
    #print("Cover page is " + newchapterpath + newchapterpages[0])
    #Get extension of source file
    ext=get_extension(newchapterpages[0])
    newchaptercoverdest = OPCHAPTERCOVERPATH + "CH" + str(newchapternumber) + " Cover" + ext
    #print("Copy " + newchapterpath + newchapterpages[0] + " to " + newchaptercoverdest)
    if(os.path.isfile(newchaptercoverdest)) :
        mangaguilib.error_message(newchaptercoverdest + " already exists!!!")  
    else :
        #copy cover
        try :
            copyfile(newchapterpath + newchapterpages[0],newchaptercoverdest)
        except :
            mangaguilib.error_message("ERROR: Unable to Copy " + newchapterpath + newchapterpages[0] + " to " + newchaptercoverdest)



def get_extension(chaptersrcpage) :
    #gets the extension of the filename
    ext=chaptersrcpage[chaptersrcpage.rfind('.'):]
    return ext

