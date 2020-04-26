Sebastian’s manga formatter (README.md not updated as of 11/11/2018)

This project formats a new chapter or volume of manga into my specific file structure. I use the formatted volumes to create pdf’s for me to read on my phone or tablet. Every file is typically a jpg or png image mirroring a page of manga. 
I use SQLite to keep track of every manga title’s
-currently released chapter number
-currently released volume number 
-the first chapter number that will be in the next volume.

When the formatter starts the user selects which type of format to run, and which manga title to format. It has an optional text field used for volume format. 

For chapter format, a new directory is created based on the new chapter’s number at a specific location. The formatter grabs each page from a queue directory, renames each page based on the manga title, chapter number, and page number and moves the files to the new directory. The DB table is then updated with the new current chapter number.

For volume format, the formatter grabs the volume cover from the queue, creates the new directory and renames the cover page file accordingling. Then the formatter will move all the chapter pages that are going to be in the new volume into the new directory. This is done by grabbing the first chapter number of the new volume from sql and the value that the user entered in the text field [e.g. first chapter is chapter 98(sql) and last chapter is chapter 108(user entry) volume has 11 chapters]. This creates one directory with every page in the volume. (Then I manually create the pdf outside of this program). The DB table is then updated with the new volume number and first chapter of new volume number (108++)

Both formats will show a log of every move/copy being made so I can double check before committing to the format.

This project is still a work in progress. The GUI needs to be touched up, I have a lot of other error handling I need to work on, and I need to clean up my code