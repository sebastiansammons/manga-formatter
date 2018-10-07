import sys
import os
import mangaformatlib
from tkinter import *
from tkinter import messagebox


#
#FOR ALL GUIS
#Look into protocols for WM_DELETE_WINDOWS
#
'''
ORIINAL FORMAL SELECT GUI
def formatselectgui():
    masterwindow = Tk()
    masterwindow.title("Manga Formatter")
    masterwindow.geometry('350x100')

    #Format Label
    formatlabel = Label(masterwindow, text="Select Format")
    formatlabel.grid(row=0,column=0,columnspan=6,ipadx=10,sticky=E)
    #Format Option List
    formatlist = ["Chapter Format","Volume Format"]
    formatvar=StringVar()
    formatvar.set(formatlist[0])
    formatoption = OptionMenu(masterwindow,formatvar, *formatlist)
    formatoption.config(width=20)
    formatoption.grid(row=0,column=6,columnspan=2)

    #Manga Label
    mangalabel = Label(masterwindow, text="Select Manga")
    mangalabel.grid(row=1,column=0,columnspan=6,ipadx=10)
    #Manga Title Option List
    titlelist = ["Attack On Titan","Boruto","Dr. Stone","My Hero Academia","One Piece","Platinum End","The Promised Neverland"] 
    titlevar=StringVar()
    titlevar.set(titlelist[0])
    mangalist = OptionMenu(masterwindow,titlevar,*titlelist)
    mangalist.config(width=20)
    mangalist.grid(row=1,column=6,columnspan=2)

    #Text Box (Remove after sql is worked out)
    entrynumber = Entry(masterwindow)
    entrynumber.config(width=5)
    entrynumber.grid(row=3,column=6,sticky=E)
    
    #Create Button
    b = Button(masterwindow, text="Format", command= lambda: startformat(formatvar,titlevar,entrynumber,masterwindow))
    b.grid(row=3,column=7, sticky=E)

    #masterwindow.resizable(False, False)

    #Draw window
    masterwindow.mainloop()
'''

def formatselectgui():
    masterwindow = Tk()
    masterwindow.title("Manga Formatter")
    masterwindow.geometry('350x100')

    #Format Label
    formatlabel = Label(masterwindow, text="Select Format")
    formatlabel.grid(row=0,column=0,columnspan=100,sticky=E)
    #Format Option List
    formatlist = ["Chapter Format","Volume Format"]
    formatvar=StringVar()
    formatvar.set(formatlist[0])
    formatoption = OptionMenu(masterwindow,formatvar, *formatlist)
    formatoption.config(width=12)
    formatoption.grid(row=0,column=100,columnspan=100,sticky=E)

    #Manga Label
    mangalabel = Label(masterwindow, text="Select Manga")
    mangalabel.grid(row=1,column=0,columnspan=100,sticky=E)
    #Manga Title Option List
    titlelist = ["Attack On Titan","Boruto","Dr. Stone","My Hero Academia","One Piece","Platinum End","The Promised Neverland"] 
    titlevar=StringVar()
    titlevar.set(titlelist[0])
    mangalist = OptionMenu(masterwindow,titlevar,*titlelist)
    mangalist.config(width=18)
    mangalist.grid(row=1,column=100,columnspan=100)

    #Last Chapter of New Volume Label
    lconvlabel = Label(masterwindow, text="Volume End At")
    lconvlabel.grid(row=2,column=99,sticky=W)
    #Last Chapter of New Volume Text Box
    entrynumber = Entry(masterwindow)
    entrynumber.config(width=4)
    entrynumber.grid(row=2,column=100,sticky=W)
    
    #Create Button
    b = Button(masterwindow, text="Format", command= lambda: startformat(formatvar,titlevar,entrynumber,masterwindow,rbv))
    b.grid(row=2,column=199, sticky=E)

    #Radiobuttons
    rbv = IntVar()
    rbd = Radiobutton(masterwindow, text = "Detailed",variable = rbv,value = 0)
    rbs = Radiobutton(masterwindow, text = "Simple",variable = rbv, value = 1)
    rbd.grid(row=3,column=99,sticky=E)
    rbs.grid(row=3,column=100,sticky=W)
    rbv.set(1)
    #masterwindow.resizable(False, False)

    #Draw window
    masterwindow.mainloop()



#Confirmation Button
def startformat(formatvar,titlevar,entrynumber,root,rbv):
    if(rbv.get()==1) :
        logtype = "Simple"
    else :
        logtype = "Detailed"
    formattype = formatvar.get()
    title = titlevar.get()
    number = entrynumber.get()
    if(formattype=="Chapter Format"):
        mangaformatlib.sql_format_chapter(title,logtype)
    elif(formattype=="Volume Format"):
        #check for empty field
        if(number=="") :
            error_message("NO CHAPTER NUMBER GIVEN")
            return
        #Make sure entry is an actual Number
        try :
            number = int(number)
        except :
            error_message("CHAPTER NUMBER NOT GIVEN")
            return
        #Make sure that lastchapter is within the bounds of the chapters available
        try :
            otherchaplist = [f for f in os.listdir(mangaformatlib.ROOTPATH + str(title) + mangaformatlib.CHAPTERFORMATPATH) if not f.startswith('.')]
        except :
            error_message("ERROR!! [" + mangaformatlib.QUEUESRC + "] NOT FOUND")
            exit()
        otherchaplist = sorted(otherchaplist)
        if(int(number) > int(otherchaplist[len(otherchaplist)-1])) :
            error_message("ENTRY GIVEN TOO BIG FOR FORMAT")
            return
        if(int(number) < int(otherchaplist[0])) :
            error_message("ENTRY GIVEN TOO SMALL FOR FORMAT")
            return    
        mangaformatlib.sql_format_volume(title,number,logtype)
    else:
        error_message("FATAL ERROR: NO FORMAT TYPE")
    print("destroy first format window")
    root.destroy()
    print("quit first format window")
    root.quit()

def error_message(message):
    top = Tk()
    #Avoids root window from being drawn
    top.geometry("0x0")
    messagebox.showwarning("ERROR",message)
    top.destroy()

def display_logs(loglist,logtype):
    logwindow = Tk()
    logwindow.title("Format Logs")
    if(logtype=="Simple") :
        logwindow.geometry("406x400")
        text = Text(logwindow,height = 24,width=57,bg="grey")
    else :
        logwindow.geometry("1880x400")
        #Create Text
        text = Text(logwindow,height = 24,width=267,bg="grey")
    for i in loglist:
        text.insert(END, i + '\n')
    #text.pack(side=LEFT, fill=BOTH, expand=YES)
    text.config(state="disabled")
    text.grid(row=0,column=0,columnspan=200)


    #Create OK Button
    #make confirm format
    bcommit = Button(logwindow, text="FORMAT", command= lambda: commitformat(logwindow))
    bcommit.grid(row=1,column=101,sticky=E)

    babort = Button(logwindow, text ="ABORT", command= lambda: abortformat(logwindow))
    babort.grid(row=1,column=99,sticky=E)
    
    logwindow.protocol("WM_DELETE_WINDOW", lambda: abortformat(logwindow))
    
    
    #Draw Window
    logwindow.mainloop()
    return

def commitformat(root):
    print("destroy log")
    root.destroy()
    print("quit log")
    root.quit()
    text = "Commit"
    return  text

def abortformat(root):
    root.destroy()
    root.quit()
    exit()
