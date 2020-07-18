Sebastian’s Manga Formatting tool (README.md updated as of 07/17/2020)

This tool is still a work in progress. But for now the functionality works the way I want it to.

Some additional changes I might add:
-update webUI's html, integrate some css and javascript. Basically make a better front end.
-the container is still in "development" mode. Not a "production" tool
-add funtionality to customize the format so if other people want to use this tool with their own format in mind, they can.


This tool is designed to format a chapter, batch of chapters, a volume or an entire collection of a manga into a specific naming convention. I use this naming convention to create directoriess filled with chapter pages(image files) that are sorted to mirror a book. I used to rename every file manually every week but now it's automatic! The tool is written in python, uses SQlite for it's database and uses the flask framework to create the webUI. This was my first project using python, creating and designing a web interface, and creating a Docker container. The tool was designed to become its own container and have it run from my home server along with all of my other containers using docker-compose  There are three main options for formating.

Auto Format
Manual Fortmat
Full Manga Format

The naming conventions are:
    A page(image file):                     [manga] - CH[###]PG[##] - [title]
    A Volume(book) cover(image file):       [manga] Volume [##] - [title]

#Note: Since this tool was designed for a container, all paths are relative to the location you mount the directories /manga and /appdata. If you want to run this tool outside of a the container, you should only have the change manga_config.py. For the preview type you would need to make an environment variable PREVIEW_TYPE to be either "SIMPLE" or "DETAILED". By default the preview will show a simple preview if there is no environemnt variable.

Auto Format:
Auto was designed for ongoing manga's that I read to rename the weekly(or monthly) released chapters and put them in their correct location. The two sub options for Auto Format are:
    Auto Chapter
    Auto Volume

Manual Format:
Manual was mostly designed for any ongoing manga's that I have that have errors in their name or are in order. This is so I can quickly change a single chapter, multiple chapters, or an entire volume if I need to.

Full Manga Format:
Full Manga is used for any new ongoing or completed manga that I want to add to my library.
