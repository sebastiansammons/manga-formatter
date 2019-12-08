import os
import mangaconfig
import mangaformatlib
import mangaguilib

#Make sure queue isn't empty
try :
    if(len([f for f in os.listdir(mangaconfig.QUEUESRC) if not f.startswith('.')])==0) :
        #Window Message
        mangaguilib.error_message("Empty Queue, Your queue is empty!!")
        exit()
except SystemExit :
    exit()
except :
    mangaguilib.error_message("ERROR! [" + mangaconfig.QUEUESRC + "] NOT FOUND")
    exit()
#Create Format GUI
mangaguilib.formatselectgui()