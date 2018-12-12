# Project-GoodToKnow

Site domain: https://goodtoknow1.herokuapp.com

Git pointer: https://github.com/NogaBar/Project-GoodToKnow.git

this project includes:
"booklets" and "index" folders are found in:
https://drive.google.com/drive/folders/1RkIVdGOZxw78g6RF1cOBFfG1TjaDF75G?usp=sharing

"booklets" folder - raw material of booklets
"index" folder - entire website
    index.php - main page
    image - all images
    includes - all repeating parts of  pages - nav, pager...
    folder for each booklet
    all other pages

"script" folder - python script
    script_web.py - the script
    page templates

Android Compiled App - app-debug.apk file
Android Studio Project File in App.zip

Add a New Booklet Instructions:
1. Put in one parent directory "booklets", "index" and "script" directories (Unzipped)
2. Create a new directory inside "booklets" directory named in English
   This directory will contain the ebup file and the pdf file (pdf name must be in English)
3. save in index\image the header image (this image will apear in the main app page)
4. In index\all_booklets_list.php add new booklets parameters':
   $booklets[n-1] = "<English Name>"; //the name of the directory from stage 2
   $images[n-1] = "<Header Image File>";
   $booklet_description[n-1] = "<Hebrew Name>";
   note: the indicies in all the arrays are the same and is 1 index above the last index exits
5. Run "script_web" from "script" directory
6. The website domain in currently in heroku, for upload the new booklet please
    push your changes to heroku git repository - https://git.heroku.com/goodtoknow1.git/ 
