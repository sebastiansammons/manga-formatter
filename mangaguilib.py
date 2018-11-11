import sys
import os
import mangaformatlib
from tkinter import *
from tkinter import messagebox

def formatselectgui() :
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
    autob = Button(masterwindow, text="Auto Format", command= lambda: autoformat(formatvar,titlevar,entrynumber,masterwindow,rbl))
    autob.grid(row=2,column=199, sticky=E)

    manualb = Button(masterwindow, text="Manual Format", command= lambda: manualformatgui(masterwindow))
    manualb.grid(row=3,column=199, sticky=E)

    #Radiobuttons
    rbl = IntVar()
    rbd = Radiobutton(masterwindow, text = "Detailed",variable = rbl,value = 0)
    rbs = Radiobutton(masterwindow, text = "Simple",variable = rbl, value = 1)
    rbd.grid(row=3,column=99,sticky=E)
    rbs.grid(row=3,column=100,sticky=W)
    rbl.set(1)
    #masterwindow.resizable(False, False)

    #Draw window
    masterwindow.mainloop()



#Confirmation Button
def autoformat(formatvar,titlevar,entrynumber,root,rbl) :
    if(rbl.get()==1) :
        logtype = "Simple"
    else :
        logtype = "Detailed"
    formattype = formatvar.get()
    title = titlevar.get()
    number = entrynumber.get()
    if(formattype=="Chapter Format") :
        mangaformatlib.sql_format_chapter(title,logtype)
    elif(formattype=="Volume Format") :
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
    else :
        error_message("FATAL ERROR: NO FORMAT TYPE")
    root.destroy()
    root.quit()

def manualformatgui(root) :
    #Remove first window
    root.destroy()
    root.quit()
    newmasterwindow = Tk()
    newmasterwindow.title("Manga Formatter")
    newmasterwindow.geometry('350x130')

    #Format Label
    formatlabel = Label(newmasterwindow, text="Select Format")
    formatlabel.grid(row=0,column=0,columnspan=100,sticky=E)
    #Format Option List
    formatlist = ["Chapter Format","Volume Format"]
    formatvar=StringVar()
    formatvar.set(formatlist[0])
    formatoption = OptionMenu(newmasterwindow,formatvar, *formatlist)
    formatoption.config(width=12)
    formatoption.grid(row=0,column=100,columnspan=100,sticky=E)

    #Manga Label
    mangalabel = Label(newmasterwindow, text="Manga Title")
    mangalabel.grid(row=1,column=0,columnspan=100,sticky=E)
    #Manga Title Option List
    mangatitle = Entry(newmasterwindow)
    mangatitle.config(width=18)
    mangatitle.grid(row=1,column=100,columnspan=100)
    
    #Single Chapter Number or Volume Number
    entrylabel = Label(newmasterwindow, text="Number")
    entrylabel.grid(row=2,column=99,sticky=E)
    #Last Chapter of New Volume Text Box
    entrynumber = Entry(newmasterwindow)
    entrynumber.config(width=4)
    entrynumber.grid(row=2,column=100,sticky=W)
    

    rbn = IntVar()
    rbmc = Radiobutton(newmasterwindow, text = "Multiple",variable = rbn,value = 0)
    rbsc = Radiobutton(newmasterwindow, text = "Single",variable = rbn, value = 1)
    rbmc.grid(row=3,column=99,sticky=E)
    rbsc.grid(row=3,column=100,sticky=W)
    rbn.set(1)

    manualb = Button(newmasterwindow, text="Manual Format", command= lambda: manualformat(formatvar,mangatitle,entrynumber,newmasterwindow,rbn,rbl))
    manualb.grid(row=4,column=199, sticky=E)

    #Radiobuttons
    rbl = IntVar()
    rbd = Radiobutton(newmasterwindow, text = "Detailed",variable = rbl,value = 0)
    rbs = Radiobutton(newmasterwindow, text = "Simple",variable = rbl, value = 1)
    rbd.grid(row=4,column=99,sticky=E)
    rbs.grid(row=4,column=100,sticky=W)
    rbl.set(1)
    #masterwindow.resizable(False, False)

    #Draw window
    newmasterwindow.mainloop()
    return

def manualformat(formatvar,mangatitle,entrynumber,newmasterwindow,rbn,rbl) :
    formattype = formatvar.get()
    title = mangatitle.get()
    number = entrynumber.get()
    if(rbn.get()==1) :
        counttype = "Single"
    else :
        counttype = "Multiple"
    if(rbl.get()==1) :
        logtype = "Simple"
    else :
        logtype = "Detailed"
    if(title=="") :
        error_message("NO MANGA TITLE GIVEN")
        return
    #check for empty field
    if(number=="") :
        if(counttype=="Single") :
            error_message("NO CHAPTER NUMBER GIVEN")
            return    
    if(formattype=="Chapter Format") :
        if(counttype=="Single") :
            mangaformatlib.manual_single_chapter(title,number,logtype)
        else :
            mangaformatlib.manual_multiple_chapter(title,logtype)
    elif(formattype=="Volume Format") :
        #Make Sure user didn't select Volume & Multiple (I could ignore this)
        if(counttype=="Multiple") :
            error_message("CAN'T FORMAT MULTIPLE VOLUMES")
            return
        #Make sure entry is an actual Number
        try :
            number = int(number)
        except :
            error_message("VOLUME NUMBER NOT GIVEN")
            return
        mangaformatlib.manual_format_volume(title,number,logtype)
    else :
        error_message("FATAL ERROR: NO FORMAT TYPE")
    newmasterwindow.destroy()
    newmasterwindow.quit()    

#
#Work on this later
#
def error_message(message) :
    top = Tk()
    #Avoids root window from being drawn
    top.geometry("0x0")
    messagebox.showwarning("ERROR",message)
    top.destroy()

def display_logs(loglist,logtype) :
    logwindow = Tk()
    logwindow.title("Format Logs")
    if(logtype=="Simple") :
        logwindow.geometry("406x400")
        text = Text(logwindow,height = 24,width=57,bg="grey")
    else :
        logwindow.geometry("1880x400")
        #Create Text
        text = Text(logwindow,height = 24,width=267,bg="grey")
    for i in loglist :
        text.insert(END, i + '\n')
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

#
#Work on this Later
#
def commitformat(root) :
    root.destroy()
    root.quit()
    #text = "Commit"
    #return  text

#
#Work on this Later
#
def abortformat(root) :
    root.destroy()
    root.quit()
    exit()