import mangaformatlib
import mangaguilib
import os

#Make sure queue isn't empty
try :
    if(len([f for f in os.listdir(mangaformatlib.QUEUESRC) if not f.startswith('.')])==0):
        print("Queue is empty, ABORT")
        #Window Message
        mangaguilib.error_message("Empty Queue, Your queue is empty!!")
        exit()
except SystemExit :
    exit()
except :
    mangaguilib.error_message("ERROR! [" + mangaformatlib.QUEUESRC + "] NOT FOUND")
    exit()
#Create Format GUI
mangaguilib.formatselectgui()
print("hey this is the end")
