import sys
import os
import mangaformatlib
from tkinter import *
from tkinter import messagebox

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
    b = Button(masterwindow, text="Format", command= lambda: confirmformat(formatvar,titlevar,entrynumber,masterwindow))
    b.grid(row=3,column=7)


    #Draw window
    masterwindow.mainloop()


#Confirmation Button
def confirmformat(formatvar,titlevar,entrynumber,root):
    formattype = formatvar.get()
    title = titlevar.get()
    number = entrynumber.get()
    if(formatvar.get()=="Chapter Format"):
        #logs = mangaformatlib.manual_format_chapter(title,number)
        mangaformatlib.sql_format_chapter(title)
    elif(formatvar.get()=="Volume Format"):
        #Volume Format Function
        mangaformatlib.sql_format_volume(title,number)
    else:
        print("FATAL ERROR")
    print("destroy format")
    root.destroy()
    print("quit format")
    root.quit()
    #try:
    #    display_logs(logs)  
    #except:
    #    print("no logs")

def error_message(message):
    top = Tk()
    #Avoids root window from being drawn
    top.geometry("0x0")
    messagebox.showwarning(message)

def display_logs(loglist):
    listwindow = Tk()
    listwindow.title("Format Logs")
    listwindow.geometry("1800x400")
    #Create Text
    text = Text(listwindow,height = 20,width=250)
    for i in loglist:
        text.insert(END, i + '\n')
    text.pack()
    text.config(state="disabled")
    text.grid(row=0,column=0)


    #Create OK Button
    #make confirm format
    bcommit = Button(listwindow, text="FORMAT", command= lambda: commitformat(listwindow))
    bcommit.grid(row=1,column=1,sticky=E)

    babort = Button(listwindow, text ="ABORT", command= lambda: abortformat(listwindow))
    babort.grid(row=1,column=0,sticky=W)
    #Draw Window
    listwindow.mainloop()
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
