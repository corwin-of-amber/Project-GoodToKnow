# Project-GoodToKnow

### In this README:
* In this README
* Useful links
* Project files information - in this git
* Instructions - add a new booklet

### Useful links:
* Final product - site domain:  
https://goodtoknow1.herokuapp.com
* Git pointer:  
https://github.com/NogaBar/Project-GoodToKnow.git

### Project files information - in this git
* **app-debug.apk** file - Android Compiled App
* **App.zip** - Android Studio Project File
* **"booklets" folder** - Unprocessed material of booklets used as input to the script.
    - Files: For each booklet, a directory with an EPub file, a PDF file and logo image file.
    - [Link to "booklets" in google drive](https://drive.google.com/open?id=1pY6eHzhuz9r0Y_X69vPdhNrjtkMVyO2s) *(Too large for git)*
* **"index" folder** - the entire website  
    - Files & Folders:
        - index.php - main page; separated to included parts.
        - about, donors, initiator pages; separated to included parts
        - image - general images
        - includes - all repeating parts of pages - nav, pager...
        - folder for each booklet - created by the script
     - [Link to "index" in google drive](https://drive.google.com/open?id=1PRrcQlAiAfnzpS9tPqtXNyjaIgKB1Awo) *(Too large for git)*
* **"script" folder** - python "Add a new booklet" script
    - Files:
        - script_web.py - the script
        - all_booklets_list.php - file that holds some user input for the script
        - 2 templates to be used by the script

### Instructions - add a new booklet:
1. Under directory "booklets", create a directory with the English name of the new booklet, henceforth *booklet_name*
1. Under directory booklets\\*booklet_name*, copy your booklet's EPub file, PDF file and logo image file (henceforth *image_logo_name*). The PDF's file name must be in English.
1. The script will add the last booklet in "all_booklets_list.php" to the website:  
Under "script\all_booklets_list.php", add new booklet's parameters to the end of the list in the file, as follows:  
    - \$booklets\[n] = "*name*";  
\$images\[n] = "*image_logo_name*";  
\$booklet_description\[n] = "*Hebrew Name to be presented in website*";
    - n is the 1 + the last booklet's index in the "all_booklets_list.php" file.  
    - Follow the regularity of previous booklets
1. Run "script_web" from "script" directory
1. The website domain in currently in heroku. To upload the new booklet, push your changes to heroku git repository.  
  https://git.heroku.com/goodtoknow1.git
