import sys
import os
from shutil import copyfile
import sqlite3
import mangaguilib


def sql_format_chapter(mangatitle):
    #Default PATHS
    #Change when I get new mac/final location
    ROOTPATH = "/Users/Fridge/Documents/Python/MangaProj/Manga/MangaTest/"
    CHAPTERFORMATPATH = "/Chapter Pictures/Other Chapters/"   
    #New chapter source
    #Change when I get new mac/final location
    chaptersrc = "/Users/Fridge/Documents/Python/MangaProj/Manga/ChapterQueue/"
    #Create list of non-hidden filenames
    chaptersrclist = [f for f in os.listdir(chaptersrc) if not f.startswith('.')]
    #Sort chaptersrc list
    chaptersrclist = sorted(chaptersrclist)
    #Get number of pages in new chapter
    pagecount = len(chaptersrclist)   
    #Connect to SQLite
    #change when final location
    try :
        conn = sqlite3.connect('/Users/Fridge/Documents/Python/MangaProj/fridgemedia.db')
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
    #        #make a message popup later            
    #        mangaguilib.error_message("Chapter already formatted? ABORT!")
    #        exit()
    #    else:
    #        pass
    copylog = [None] * pagecount
    pagesrc = [None] * pagecount
    pagedest = [None] * pagecount
    #get full source and destination paths
    for i in range(0,pagecount):
        pagesrc[i]= chaptersrc+str(chaptersrclist[i])
        #Get extension of current source page file
        ext=get_extension(pagesrc[i])
        pagedest[i] = newchapterpath + mangatitle + " CH" + str(newchapternumber)+" PG"+str(i+1)+ext
        copylog[i] = pagesrc[i] + " to "+pagedest[i]
    #print copy log
    mangaguilib.display_logs(copylog)
    #ask to confirm copy
    #for i in range(0,pagecount):    
        #rename
        #os.rename(pagesrc[i],pagedest[i])
    #update sql with new current chapter number
    #
    #Out of range error coming from here, got late so i had to leave it
    #
    c.execute("UPDATE manga set curchap = ? WHERE title = ?",(newchapternumber,mangatitle))
    #c.execute("UPDATE manga set curchap = ? WHERE title = ?",(int(newchapternumber),mangatitle))
    newsqldata = [tup[0] for tup in c.fetchall()]
    print("Update sql curchap to: "+str(newsqldata[0]))
    #conn.commit()
    conn.close()
    #Check if Title is One Piece
    if(mangatitle=="One Piece"):
        print("One Piece, Not Moving Cover Yet. Still Need To Fix Some Things")            
        #one_piece_cover_copy(newchapterpath,newchapternumber)

    return copylog



def manual_format_chapter(mangatitle,newchapternumber):
    #Default PATHS
    #Change when I get new mac/final location
    ROOTPATH = "/Users/Fridge/Documents/Python/MangaProj/Manga/MangaTest/"
    CHAPTERFORMATPATH = "/Chapter Pictures/Other Chapters/"   
    #New chapter source
    #Don't need to check if src is empty, main did that already
    #Change when I get new mac/final location
    chaptersrc = "/Users/Fridge/Documents/Python/MangaProj/Manga/ChapterQueue/"
    #Create list of non-hidden filenames
    chaptersrclist = [f for f in os.listdir(chaptersrc) if not f.startswith('.')]
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
        pagesrc[i]= chaptersrc+str(chaptersrclist[i])
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

    return copylog

#need to *fix* later (find cases)
#check if file is already there
def one_piece_cover_copy(newchapterpath,newchapternumber):
    #change later in final version
    CHAPTERCOVERPATH = "/Users/Fridge/Documents/Python/MangaProj/Manga/MangaTest/One Piece/Cover Pictures/"    
    newchapterpages = os.listdir(newchapterpath)
    newchapterpages = sorted(newchapterpages)
    print("Cover page is " + newchapterpath + newchapterpages[0])
    #Get extension of source file
    ext=get_extension(newchapterpages[0])
    newchaptercover = CHAPTERCOVERPATH + "CH" + str(newchapternumber) + " Cover" + ext
    print("Copy "+ newchapterpath + newchapterpages[0] + " to " + newchaptercover)
    if(os.path.isfile(newchaptercover)):
        #create pop up message
        mangaguilib.error_message(newchaptercover + " already exists!!!")  
    else:    
        copyfile(newchapterpath + newchapterpages[0],newchaptercover)



def get_extension(chaptersrcpage):
    #gets the extension of the filename
    ext=chaptersrcpage[chaptersrcpage.rfind('.'):]
    return ext

def sql_format_volume(mangatitle,lastchapter):
    #Default PATHS
    #Change when I get new mac/final location
    ROOTPATH = "/Users/Fridge/Documents/Python/MangaProj/Manga/MangaTest/"
    CHAPTERFORMATPATH = "/Chapter Pictures/Other Chapters/"
    VOLUMEFORMATPATH = "/Chapter Pictures/Volume Chapters/"
    
    coversrc = "/Users/Fridge/Documents/Python/MangaProj/Manga/ChapterQueue/"
    #Get Cover page file
    volumesrc = [f for f in os.listdir(coversrc) if not f.startswith('.')]
    #Make sure there is only 1 file in the directory
    if(len(volumesrc)!=1):
        #make message pop up
        mangaguilib.error_message("ERROR MORE THAN ONE FILE IN SOURCE. DON'T KNOW WHCH ONE IS VOLUME COVER")
        exit()
    else:
        #Connect to SQLite
        #change when final location
        try :
            conn = sqlite3.connect('/Users/Fridge/Documents/Python/MangaProj/fridgemedia.db')
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
        #        #make a message popup later            
        #        print("Volume already formatted? ABORT!")
        #        exit()
        #    else:
        #        pass
        #Copy Volume Cover
        volcoversrc = coversrc + volumesrc[0]
        #Get extension of source file
        ext=get_extension(volcoversrc)   
        volcoverdest = newvolumepath + mangatitle +" "+ str(newvolumenumber) + ext
        coverlog ="Copy" + volcoversrc + " to "+ volcoverdest
        print(coverlog)
        #actual copy line here
        if(int(lastchapter)>firstchap):
            numchapters = int(lastchapter) - firstchap + 1
            chapterdir = [None] * numchapters
            chaptersrc = [None] * numchapters  
            for chapnum in range(firstchap,int(lastchapter)+1):
                print(str(chapnum)+" chapter")
                chapterdir[chapnum-firstchap] = ROOTPATH + mangatitle + CHAPTERFORMATPATH +str(chapnum).zfill(3)+"/"
                curvolchaplist = [f for f in os.listdir(chapterdir[chapnum-firstchap]) if not f.startswith('.')]
                curvolchaplist = sorted(curvolchaplist)
                chaptersrc[chapnum-firstchap] = [None] * len(curvolchaplist)
                for i in range(0,len(curvolchaplist)):
                    chaptersrc[chapnum-firstchap][i] = curvolchaplist[i]
            #show log
            for i in range(0,numchapters):
                for j in range(0,len(chaptersrc[i])):     
                    print(chapterdir[i] +chaptersrc[i][j]+ " to")
                    print(newvolumepath+chaptersrc[i][j])
                print()
            #confirm & Format
            for i in range(0,numchapters):
                for j in range(0,len(chaptersrc[i])):  
                    #os.rename(chapterdir[i] +chaptersrc[i][j],newvolumepath+chaptersrc[i][j])
                    print(str(i) + ":" + str(j))
        else:
            mangaguilib.error_message("Incorrect value of last chapter")
        #updatesql curvol + fconv
        #update sql with new current chapter number
        c.execute("UPDATE manga set curvol = ? WHERE title = ?",(int(newvolumenumber),mangatitle))
        c.execute("Select curvol from manga where title = ?",(mangatitle,))
        sqldata = [tup[0] for tup in c.fetchall()]
        print("Update sql curvol to: "+str(sqldata[0]))
        c.execute("UPDATE manga set fconv = ? WHERE title = ?",(int(lastchapter)+1,mangatitle))
        c.execute("Select fconv from manga where title = ?",(mangatitle,))
        sqldata = [tup[0] for tup in c.fetchall()]
        print("Update sql fconv to: "+str(sqldata[0]))
        #conn.commit()
        conn.close()