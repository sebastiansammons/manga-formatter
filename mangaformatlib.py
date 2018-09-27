import sys
import os
from shutil import copyfile
import sqlite3
import mangaguilib

#Change these later
ROOTPATH = "/Users/Fridge/Documents/Python/MangaProj/Manga/MangaTest/"
QUEUESRC = "/Users/Fridge/Documents/Python/MangaProj/Manga/ChapterQueue/"
CHAPTERFORMATPATH = "/Chapter Pictures/Other Chapters/"
VOLUMEFORMATPATH = "/Chapter Pictures/Volume Chapters/"
OPCHAPTERCOVERPATH = "/Users/Fridge/Documents/Python/MangaProj/Manga/MangaTest/One Piece/Cover Pictures/"
MYSQLITEDB = '/Users/Fridge/Documents/Python/MangaProj/fridgemedia.db'

def sql_format_chapter(mangatitle):
    #Create list of non-hidden filenames
    chaptersrclist = [f for f in os.listdir(QUEUESRC) if not f.startswith('.')]
    #Sort list
    chaptersrclist = sorted(chaptersrclist)
    #Get number of pages for the new chapter
    pagecount = len(chaptersrclist)   
    #Connect to SQLite
    try :
        conn = sqlite3.connect(MYSQLITEDB)
        c = conn.cursor()
        #Get Current Chapter number from SQLite and increment
        c.execute("Select curchap from manga where title = ?",(mangatitle,))
        sqldata = [tup[0] for tup in c.fetchall()]
        newchapternumber = sqldata[0] + 1
    except :
        mangaguilib.error_message("CANNOT CONNECT TO fridgemedia.db")
        exit()
    #Create path for new chapter directory
    newchapterpath = ROOTPATH + mangatitle + CHAPTERFORMATPATH + str(newchapternumber).zfill(3)+"/"  
    #Create new directory (from new path just generated)
    #Check if directory exists
    #try :
    #    os.mkdir(newchapterpath)
    #except :
    #    print(newchapterpath + " Exists")
    #    if(len(os.listdir(newchapterpath))>0):
    #        mangaguilib.error_message("Chapter already formatted? ABORT!")
    #        exit()
    #    else:
    #        pass
    copylog = [None] * pagecount
    pagesrc = [None] * pagecount
    pagedest = [None] * pagecount
    #get full source and destination paths for copy
    for i in range(0,pagecount):
        pagesrc[i]= QUEUESRC+str(chaptersrclist[i])
        #Get extension of current source page file
        ext=get_extension(pagesrc[i])
        pagedest[i] = newchapterpath + mangatitle + " CH" + str(newchapternumber)+" PG"+str(i+1)+ext
        #detailed log
        #copylog[i] = pagesrc[i] + " to "+pagedest[i]
        #simple log
        copylog[i] = str(chaptersrclist[i]) + " to "+ mangatitle + " CH" + str(newchapternumber)+" PG"+str(i+1)+ext
    #print copy log & confirm format
    mangaguilib.display_logs(copylog)
    #rename
    #for i in range(0,pagecount):        
        #os.rename(pagesrc[i],pagedest[i])
    #update sql with new current chapter number
    c.execute("UPDATE manga set curchap = ? WHERE title = ?",(int(newchapternumber),mangatitle))
    c.execute("Select curchap from manga where title = ?",(mangatitle,))
    newsqldata = [tup[0] for tup in c.fetchall()]
    print("Updated sql curchap to: "+str(newsqldata[0]))
    #conn.commit()
    conn.close()
    #Check if Title is One Piece
    if(mangatitle=="One Piece"):
        print("One Piece Cover Copy: Currently not creating directories so I can't run this right now")            
        #one_piece_cover_copy(newchapterpath,newchapternumber)


#
#Update this later
#
def manual_format_chapter(mangatitle,newchapternumber):
    #Create list of non-hidden filenames
    chaptersrclist = [f for f in os.listdir(QUEUESRC) if not f.startswith('.')]
    #Sort chaptersrc list
    chaptersrclist = sorted(chaptersrclist)
    #Get number of pages in new chapter
    pagecount = len(chaptersrclist)   
    #Create path for new chapter directory
    newchapterpath = ROOTPATH + mangatitle + CHAPTERFORMATPATH + newchapternumber.zfill(3)+"/"  
    #Create new directory (from new path just generated)
    #Check if directory exists
    try :
        os.mkdir(newchapterpath)
    except :         
        print(newchapterpath + " Exists")
        if(len(os.listdir(newchapterpath))>0):
            mangaguilib.error_message("Chapter already formatted? ABORT!")
            exit()
        else:
            pass
    copylog = [None] * pagecount
    pagesrc = [None] * pagecount
    pagedest = [None] * pagecount
    
    
    #Move & format new chapter
    for i in range(0,pagecount):
        pagesrc[i]= QUEUESRC+str(chaptersrclist[i])
        #Get extension of current source page file
        ext=get_extension(pagesrc[i])
        pagedest[i] = newchapterpath + mangatitle + " CH" + str(newchapternumber)+" PG"+str(i+1)+ext
        copylog[i] = pagesrc[i] + " to "+pagedest[i]
        #print log
        #ask to confirm copy
        #rename
        #os.rename(pagesrc[i],pagedest[i])
    
    #Check if Title is One Piece
    if(mangatitle=="One Piece"):
        print("One Piece, Not Moving Cover Yet. Still Need To Fix Some Things")            
        #one_piece_cover_copy(newchapterpath,newchapternumber)

#need to *fix* later (find cases)
#check if file is already there
def one_piece_cover_copy(newchapterpath,newchapternumber):
    #get cover page
    newchapterpages = os.listdir(newchapterpath)
    newchapterpages = sorted(newchapterpages)
    print("Cover page is " + newchapterpath + newchapterpages[0])
    #Get extension of source file
    ext=get_extension(newchapterpages[0])
    newchaptercover = OPCHAPTERCOVERPATH + "CH" + str(newchapternumber) + " Cover" + ext
    print("Copy "+ newchapterpath + newchapterpages[0] + " to " + newchaptercover)
    if(os.path.isfile(newchaptercover)):
        #create pop up message
        mangaguilib.error_message(newchaptercover + " already exists!!!")  
    #else:
        #copy cover 
        #copyfile(newchapterpath + newchapterpages[0],newchaptercover)


def get_extension(chaptersrcpage):
    #gets the extension of the filename
    ext=chaptersrcpage[chaptersrcpage.rfind('.'):]
    return ext

def sql_format_volume(mangatitle,lastchapter):
    #Get Cover page file
    volumesrc = [f for f in os.listdir(QUEUESRC) if not f.startswith('.')]
    #Make sure there is only 1 file in the directory (the cover)
    if(len(volumesrc)!=1):
        mangaguilib.error_message("MORE THAN ONE FILE IN QUEUE. DON'T KNOW WHCH ONE IS VOLUME COVER")
        exit()
    else:
        #Connect to SQLite
        #change when final location
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
        print(newvolumenumber)
        #Get first chapter of new volume
        c.execute("Select fconv from manga where title = ?",(mangatitle,))
        sqldata = [tup[0] for tup in c.fetchall()]
        firstchap = sqldata[0]
        print(firstchap)
        #Create path for new chapter directory
        if(mangatitle=="One Piece"):
            newvolumepath = ROOTPATH + mangatitle + VOLUMEFORMATPATH + "Volume " + str(newvolumenumber).zfill(3)+"/"
        else:
            newvolumepath = ROOTPATH + mangatitle + VOLUMEFORMATPATH + "Volume " + str(newvolumenumber).zfill(2)+"/"
        #Create new directory (from new path just generated)
        #Check if directory exists
        #try :
        #    os.mkdir(newvolumepath)
        #except :         
        #    print(newvolumepath + " Exists")
        #    if(len(os.listdir(newvolumepath))>0):        
        #        print("Volume already formatted? ABORT!")
        #        exit()
        #    else:
        #        pass
        #Copy Volume Cover
        volcoversrc = QUEUESRC + volumesrc[0]
        #Get extension of source file
        ext=get_extension(volcoversrc)   
        volcoverdest = newvolumepath + mangatitle +" "+ str(newvolumenumber) + ext
        coverlog ="Copy" + volcoversrc + " to "+ volcoverdest
        #make a pop up for this?
        print(coverlog)
        #Format cover
        #os.rename(volcoversrc,volcoverdest)
        #Move chapters
        if(int(lastchapter)>firstchap):
            numchapters = int(lastchapter) - firstchap + 1
            chapterdir = [None] * numchapters
            chaptersrc = [None] * numchapters  
            for chapnum in range(firstchap,int(lastchapter)+1):
                chapterdir[chapnum-firstchap] = ROOTPATH + mangatitle + CHAPTERFORMATPATH +str(chapnum).zfill(3)+"/"
                curchapsrcpages = [f for f in os.listdir(chapterdir[chapnum-firstchap]) if not f.startswith('.')]
                curchapsrcpages = sorted(curchapsrcpages)
                chaptersrc[chapnum-firstchap] = [None] * len(curchapsrcpages)
                for i in range(0,len(curchapsrcpages)):
                    chaptersrc[chapnum-firstchap][i] = curchapsrcpages[i]
            #create & show log
            numlog = 0
            for i in range(0,numchapters):
                numlog+=len(chaptersrc[i])
            copylog = [None] * numlog
            logindex = 0
            for i in range(0,numchapters):
                for j in range(0,len(chaptersrc[i])):
                    #detailed log
                    #copylog[logindex] = chapterdir[i] +chaptersrc[i][j]+ " to "+ newvolumepath+chaptersrc[i][j]
                    #simple log
                    copylog[logindex] = chapterdir[i] + " to "+ newvolumepath
                    logindex+=1
            #confirm & Format
            mangaguilib.display_logs(copylog)
            #for i in range(0,numchapters):
            #    for j in range(0,len(chaptersrc[i])):  
            #        #os.rename(chapterdir[i] +chaptersrc[i][j],newvolumepath+chaptersrc[i][j])
        else:
            mangaguilib.error_message("Last Chapter number < First chapter number!!!!")
        #updatesql curvol + fconv
        #update sql with new current chapter number
        c.execute("UPDATE manga set curvol = ? WHERE title = ?",(int(newvolumenumber),mangatitle))
        c.execute("Select curvol from manga where title = ?",(mangatitle,))
        sqldata = [tup[0] for tup in c.fetchall()]
        print("Updated sql curvol to: "+str(sqldata[0]))
        c.execute("UPDATE manga set fconv = ? WHERE title = ?",(int(lastchapter)+1,mangatitle))
        c.execute("Select fconv from manga where title = ?",(mangatitle,))
        sqldata = [tup[0] for tup in c.fetchall()]
        print("Updated sql fconv to: "+str(sqldata[0]))
        #conn.commit()
        conn.close()