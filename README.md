# Mezzmo Trailer Checker
A utility to help you manage your Mezzmo local trailer files.  


## Features:

- Read current You Tube movie trailer information from the Mezzmo database
- Track movies which have local trailers, which don't and last checked time
- Download high quality trailers from You Tube for local hosting
- Fast You Tube download speeds
- Detect You Tube trailers which cannot be downloaded and marks them "Bad" 
- Automatically normalize and trim the You Tube trailers names
- User selectable feature of 480P, 720P or 1080P quality trailers (if available, otherwise best quality available)
- Automatically move trailers to designated location (i.e. NAS, local disk etc.)
- Option for automatically <a href="https://github.com/Conceiva/MezzmoKodiPlugin/wiki/Managing-Your-Library#metadata-locking">locking the Mezzmo metadata</a> to avoid overriding trailer information
- Option for how many movies to check in each batch run of the Mezzmo Trailer Checker (1-20)
- Option to limit how many trailers per movie (1-20)
- Option to order trailers by size
- Option for supporting prefer <a href="https://github.com/Conceiva/MezzmoKodiPlugin/wiki/Movie-Trailers#prefer-local-trailers">local trailer capability</a> to allow You Tube trailers for Mezzmo web interface
- Option for only local trailers
- Full detailed logfile
<br/>

## Installation and usage:

-  Download the Mezzmo Trailer Checker release zipfile
-  Unzip file into an empty folder on your system
-  Ensure you have Python installed on Windows or Linux.  Preferably version 3.x 
-  Edit the config.text file with the location of your Mezzmo
   database and trailer folder. 
-  Open a command window and run trailer_checker.py<br/>
   See optional command line arguments below.    
-  Recommended usage sequence is:
   - run trailer_checker.py sync
   - run trailer_checker.py trailer or
   - run trailer_checker.py new
   - run trailer_checker.py csv trailer
   - review CSV file which has a complete listing of Mezzmo trailers 

   
## Command line arguments:  (Limit 1 at a time)

- <b>trailer</b>	-  Runs the trailer checker normally starting with the first movie in the Mezzmo database. <br>
- <b>trailer new</b>    -  Runs the trailer checker normally starting with the newest movie in the Mezzmo database.<br/> 
- <b>sync</b>           -  Syncs the Mezzmo Trailer Checker to the Mezzmo database without fetching any trailers. <br/> 
- <b>csv trailer</b>    -  Creates a CSV file with the trailer information in the Mezzmo Trailer Checker<br/> 
- <b>csv history</b>    -  Creates a CSV file with the history information in the Mezzmo Trailer Checker</br>          
         
 The CSV export utility currently requires Python version 3.<br/><br/>


