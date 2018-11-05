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
        chaptersrclist = [f for f in os.listdir(QUEUESRC) if not f.startswith('.')]
    except :
        mangaguilib.error_message("ERROR!! [" + QUEUESRC + "] NOT FOUND")
        exit()
    #Sort list
    chaptersrclist = sorted(chaptersrclist)
    #Get number of pages for the new chapter
    pagecount = len(chaptersrclist)   
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
    newchapterpath = ROOTPATH + mangatitle + CHAPTERFORMATPATH + str(newchapternumber).zfill(3) + "/"
    #Create new directory (from new path just generated)
    #Check if directory exists
    #try :
    #    os.mkdir(newchapterpath)
    #except :
        #might be error with path, not just existing already deal with later
    #    print(newchapterpath + " Exists")    
    #    if(len([f for f in os.listdir(newchapterpath) if not f.startswith('.')])>0) :
    #        mangaguilib.error_message("Chapter already formatted? ABORT!")
    #        exit()
    #    else :
    #        pass
    copylog = [None] * pagecount
    pagesrc = [None] * pagecount
    pagedest = [None] * pagecount
    #get full source and destination paths for copy & log
    for i in range(0,pagecount) :
        pagesrc[i]= QUEUESRC + str(chaptersrclist[i])
        #Get extension of current source page file
        ext=get_extension(pagesrc[i])
        pagedest[i] = newchapterpath + mangatitle + " CH" + str(newchapternumber) +" PG" + str(i+1) + ext
        #toggle to pick detailed or simple log?
        if(logtype=="Simple") :
            #Simple log
            copylog[i] = "/" + str(chaptersrclist[i]) + " to /" + mangatitle + " CH" + str(newchapternumber) + " PG" + str(i+1) + ext
        else :
            #detailed log
            copylog[i] = pagesrc[i] + " to " + pagedest[i]
    #print copy log & confirm format
    mangaguilib.display_logs(copylog,logtype)
    #Commit Format
    for i in range(0,pagecount) :
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
        #one_piece_cover_copy(newchapterpath,newchapternumber)



def sql_format_volume(mangatitle,lastchapter,logtype) :
    #Get Cover page file
    try :
        volumesrc = [f for f in os.listdir(QUEUESRC) if not f.startswith('.')]
    except :
        mangaguilib.error_message("ERROR!! [" + QUEUESRC + "] NOT FOUND")
        exit()
    #Make sure there is only 1 file in the directory (the cover)
    if(len(volumesrc)!=1) :
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
        newvolumepath = ROOTPATH + mangatitle + VOLUMEFORMATPATH + mangatitle + " Volume " + str(newvolumenumber).zfill(3) + "/"
    else :
        newvolumepath = ROOTPATH + mangatitle + VOLUMEFORMATPATH + mangatitle + " Volume " + str(newvolumenumber).zfill(2) + "/"
    #Create new directory (from new path just generated)
    #Check if directory exists
    #try :
    #    os.mkdir(newvolumepath)
    #except :
    #    #possible newvolumepath isn't valid instead of already existing check later
    #    print(newvolumepath + " Exists")
    #    if(len([f for f in os.listdir(newvolumepath) if not f.startswith('.')])>0) :     
    #        print("Volume already formatted? ABORT!")
    #        exit()
    #    else :
    #        pass
    #Copy Volume Cover
    volcoversrc = QUEUESRC + volumesrc[0]
    #Get extension of source file
    ext=get_extension(volcoversrc)   
    volcoverdest = newvolumepath + mangatitle + " " + str(newvolumenumber) + ext ##add leading zeros?
    coverlog = "Copy" + volcoversrc + " to " + volcoverdest
    #make a pop up for this?
    print(coverlog)
    #Format cover
    #try :
    #    os.rename(volcoversrc,volcoverdest)
    #except :
    #    mangaguilib.error_message("ERROR making cover page")
    #    exit()
    #Move chapters
    numchapters = int(lastchapter) - firstchap + 1
    #each chapter directory path
    chapterdir = [None] * numchapters
    #list of each chapter page src list (2D List)
    chaptersrc = [None] * numchapters
    for chapnum in range(firstchap,int(lastchapter) + 1) :
        #get this chapnum's directory + create list of pages in that directory
        chapterdir[chapnum-firstchap] = ROOTPATH + mangatitle + CHAPTERFORMATPATH + str(chapnum).zfill(3) + "/"
        try :
            curchapsrclist = [f for f in os.listdir(chapterdir[chapnum-firstchap]) if not f.startswith('.')]
        except :
            mangaguilib.error_message("ERROR!! [" + chapterdir[chapnum-firstchap] + "] NOT FOUND")
            break
        #sort the directory list (not realy needed tbh)
        curchapsrclist = sorted(curchapsrclist)
        #create list for this chapnum's filenames
        chaptersrc[chapnum-firstchap] = [None] * len(curchapsrclist)
        #get each chapter page filename
        for i in range(0,len(curchapsrclist)) :
            chaptersrc[chapnum-firstchap][i] = curchapsrclist[i]
    #Create & show log
    if(logtype=="Simple") :
        copylog = [None] * numchapters
        for i in range(0,numchapters) :
            #Simple log
            copylog[i] = chapterdir[i].replace(ROOTPATH + mangatitle + CHAPTERFORMATPATH,"/")[:-1] + " to " + newvolumepath.replace(ROOTPATH + mangatitle + VOLUMEFORMATPATH,"/")[:-1]
    else :
        numcopylog = 0
        for i in range(0,numchapters) :
            numcopylog+=len(chaptersrc[i])
        copylog = [None] * numcopylog
        logindex = 0
        #increment each chapter
        for i in range(0,numchapters) :
            #increment each page in the chapter
            for j in range(0,len(chaptersrc[i])) :
                #detailed log
                copylog[logindex] = chapterdir[i] + chaptersrc[i][j] + " to " + newvolumepath + chaptersrc[i][j]
                logindex+=1
    #Confirm & Format
    mangaguilib.display_logs(copylog,logtype)
    #increment each chapter
    for i in range(0,numchapters) :
        #increment each page in the chapter
        for j in range(0,len(chaptersrc[i])) :  
            try :
                print("COPY " + chapterdir[i] + chaptersrc[i][j] + " to " + newvolumepath + chaptersrc[i][j])
                #os.rename(chapterdir[i] + chaptersrc[i][j],newvolumepath + chaptersrc[i][j])
            except :
                mangaguilib.error_message("ERROR unable to copy: " + chapterdir[i] + chaptersrc[i][j] + " to " + newvolumepath + chaptersrc[i][j])
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
    chaptersrclist = [f for f in os.listdir(QUEUESRC) if not f.startswith('.')]
    #Sort chaptersrc list
    chaptersrclist = sorted(chaptersrclist)
    #Get number of pages in new chapter
    pagecount = len(chaptersrclist)   
    #Create path for new chapter directory (Keep in same directory)
    newchapterpath = MANUALDEST + chapternumber.zfill(3) + "/"
    #Create new directory (from new path just generated)
    #Check if directory exists
    try :
        os.mkdir(newchapterpath)
    except :
        print(newchapterpath + " Exists")
        if(len([f for f in os.listdir(newchapterpath) if not f.startswith('.')])>0) :
            mangaguilib.error_message("Chapter already formatted? ABORT!")
            exit()
        else :
            pass
    copylog = [None] * pagecount
    pagesrc = [None] * pagecount
    pagedest = [None] * pagecount
    #Move & format new chapter
    for i in range(0,pagecount) :
        #Singe Chapter so Queue Should just be the pages
        pagesrc[i]= QUEUESRC + str(chaptersrclist[i])
        #Get extension of current source page file
        ext=get_extension(pagesrc[i])
        pagedest[i] = newchapterpath + mangatitle + " CH" + str(chapternumber) + " PG" + str(i+1) + ext
        if(logtype=="Simple") :
            #Simple log
            copylog[i] = "/" + str(chaptersrclist[i]) + " to /" + mangatitle + " CH" + str(chapternumber) + " PG" + str(i+1) + ext
        else :
            #detailed log
            copylog[i] = pagesrc[i] + " to " + pagedest[i]
    #print copy log & confirm format
    mangaguilib.display_logs(copylog,logtype)
    #Commit Format
    for i in range(0,pagecount) :
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
    chaptercount = len(chaptersrclist)   
    #Src Directory path
    chaptersrcdir = [None] * chaptercount
    #Dest Directory Path
    chapterdestdir = [None] * chaptercount
    #Full path of all page sources
    allpagessrc = [None] * chaptercount
    #FUll path of all page destinations
    allpagesdest = [None] * chaptercount
    #Get Source & Destination Directories
    for i in range(0,chaptercount) :
        print("-" + chaptersrclist[i] + "-")
        #Get Chapter Source Directory path
        chaptersrcdir[i] = QUEUESRC + chaptersrclist[i] + "/"
        #Get Chapter Destination Directory path
        chapterdestdir[i] = MANUALDEST + chaptersrclist[i] + "/"
        #Make Chapter Destination Directory
        print("Make Directory " + chapterdestdir[i])
#        try :
#            os.mkdir(chapterdestdir[i])
#        except :
#            print(chapterdestdir[i] + " Exists")
#            if(len([f for f in os.listdir(chapterdestdir[i]) if not f.startswith('.')])>0) :
#                mangaguilib.error_message("Chapter already formatted? ABORT!")
#                exit()
#            else :
#                pass
    numcopylog = 0
    for i in range(0,chaptercount) :
        #Get List of current chapter source pages
        try :
            curchapsrclist = [f for f in os.listdir(chaptersrcdir[i]) if not f.startswith('.')]
        except :
            mangaguilib.error_message("ERROR!! [" + chaptersrcdir[i] + "] NOT FOUND")
            break
        #sort the directory list (not realy needed tbh)
        curchapsrclist = sorted(curchapsrclist)
        #create list for this chapnum's filenames
        allpagessrc[i] = [None] * len(curchapsrclist)
        allpagesdest[i] = [None] * len(curchapsrclist)
        #get each src and dest chapter page filename
        for j in range(0,len(curchapsrclist)) :
            allpagessrc[i][j] = curchapsrclist[j]
            allpagesdest[i][j] = title + " CH" + chaptersrclist[i].lstrip("0") + " PG" + str(j+1) + get_extension(curchapsrclist[j])
        #Add log Length
        numcopylog+=len(curchapsrclist)
    copylog = [None] * numcopylog    
    logindex = 0
    for i in range(0,chaptercount) :
        for j in range(0,len(allpagessrc[i])) :
            if(logtype=="Simple") :
                copylog[logindex] = "/" + allpagessrc[i][j] + " to /" + allpagesdest[i][j]
            else :
                copylog[logindex] = chaptersrcdir[i] + allpagessrc[i][j] + " to " + chapterdestdir[i] + allpagesdest[i][j]
            logindex+=1
    #Confirm & Format
    mangaguilib.display_logs(copylog,logtype)
    #increment each chapter
    for i in range(0,chaptercount) :
        #increment each page in the chapter
        for j in range(0,len(allpagessrc[i])) :  
            try :
                print("COPY " + chaptersrcdir[i] + allpagessrc[i][j] + " to " + chapterdestdir[i] + allpagesdest[i][j])
                #os.rename(chaptersrcdir[i] + allpagessrc[i][j], chapterdestdir[i] + allpagesdest[i][j])
            except :
                mangaguilib.error_message("ERROR unable to copy: " + chaptersrcdir[i] + allpagessrc[i][j] + " to " + chapterdestdir[i] + allpagesdest[i][j])
                exit()
        #remove old chapter directory
        print("REMOVE: " + chaptersrcdir[i])
        #try :
        #    shutil.rmtree(chaptersrcdir[i])
        #except :
        #    mangaguilib.error_message("ERROR!! UNABLE TO REMOVE [" + chaptersrcdir[i] + "] You need to manually remove it")            

    
def manual_format_volume(title,number,logtype) :
    manual_multiple_chapter(title,logtype)

    

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

