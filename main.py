import mangaformatlib
import mangaguilib
import os


#Constant Values
#CHAPTERSRC = "/Users/Fridge/Documents/Python/MangaProj/Manga/ChapterQueue/"
#ROOTPATH = "/Users/Fridge/Documents/Python/MangaProj/Manga/MangaTest/"
#MANGAFORMATPATH = "/Chapter Pictures/Other Chapters/"


#Make sure queue isn't empty    
if(len(os.listdir(mangaformatlib.QUEUESRC))==0):
    print("Queue is empty, ABORT")
    #Window Message
    mangaguilib.error_message("Empty Queue","Your queue is empty!!")
    exit()
#Create Format GUI
mangaguilib.formatselectgui()
print("hey this is the end")
