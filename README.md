# Mezzmo Trailer Checker
A utility to help you manage your Mezzmo local trailer files.  


## Features:

- Read current You Tube movie trailer information from the Mezzmo database
- Movie trailers can be fetched by newest, oldest, movie name or movie number
- Track movies which have local trailers, which don't and last checked time
- Download high quality trailers from You Tube for local playback
- Fast You Tube download speeds with daily limit setting
- Detect You Tube trailers which cannot be downloaded and marks them "Bad"
- Automatically remove bad trailers from Mezzmo 
- Automatically normalize and trim the You Tube trailers names
- User selectable feature of 480P, 720P or 1080P quality trailers (if available, otherwise best quality available)
- Option to set the maximum duration of trailers
- Automatically move trailers to designated location (i.e. NAS, local disk etc.)
- Option for automatically <a href="https://github.com/Conceiva/MezzmoKodiPlugin/wiki/Managing-Your-Library#metadata-locking">locking the Mezzmo metadata</a> to avoid overriding trailer information
- Option for how many movies to check in each batch run of the Mezzmo Trailer Checker (1-20)
- Option to limit how many trailers per movie (1-20)
- Option to order trailers by size
- Option for supporting prefer <a href="https://github.com/Conceiva/MezzmoKodiPlugin/wiki/Movie-Trailers#prefer-local-trailers">local trailer capability</a> to allow You Tube trailers for Mezzmo web interface
- Option to automatically adjust / standardize trailer frame rates
- Option to automatically adjust trailer audio level
- Hardware encoding acceleration to improve speed
- Option to prefer official trailers
- Option for only local trailers
- Check feature to update trailer size, resolution and duration after manual trailer changes
- Added checks for missing trailer files and trailer files with invalid names
- Show and delete orphaned local trailer files with do not have a Mezzmo database trailer entry - <b>Mew</b>
- Full detailed logfile
- Full Trailer checker statistics
- <a href="https://github.com/jbinkley60/MezzmoTrailerChecker/wiki/Mezzmo-Trailer-Checker-Data-Export">CSV export</a> of trailer information, checker history and movies in the Mezzmo DB without trailers
- Command line backups of Mezzmo Trailer Checker database
- User ability to clear trailer information by movie name or database number 
<br/>

## Installation and usage:

-  Download the Mezzmo Trailer Checker release zipfile
-  Unzip file into an empty folder on your system
-  Ensure you have Python installed on Windows.  Minimum version 3.x 
-  Edit the config.text file with the location of your Mezzmo
   database and trailer folder. 
-  Open a command window and run trailer_checker.py<br/>
   See optional command line arguments below.    
-  Recommended usage sequence is:
   - run trailer_checker.py sync
   - run trailer_checker.py trailer
   - run trailer_checker.py check
   - run trailer_checker.py csv trailer
   - review CSV file which has a complete listing of Mezzmo trailers 

   
## Command line arguments:  (Limit 1 at a time)

- <b>trailer</b>	-  Runs the trailer checker normally starting with the first movie in the Mezzmo database. <br>
- <b>trailer new</b>    -  Runs the trailer checker normally starting with the newest movie in the Mezzmo database. <br>
- <b>trailer name </b>  -  Runs trailer checker for movie name (i.e. trailer name "Christmas Vacation" ) <br>
- <b>trailer number</b> -  Runs trailer checker for movie number (i.e. trailer number 1215)  <br> 
- <b>sync</b>           -  Syncs the Mezzmo Trailer Checker to the Mezzmo database without fetching any trailers. <br> 
- <b>csv trailer</b>    -  Creates a CSV file with the trailer information in the Mezzmo Trailer Checker<br> 
- <b>csv history</b>    -  Creates a CSV file with the history information in the Mezzmo Trailer Checker<br>
- <b>csv notrail</b>    -  Creates a CSV file with a listing of all movies in the Mezzmo database with no trailers<br>
- <b>check</b>		-  Updates missing trailer duration, size or resolution information in the Checker database<br>
- <b>check new</b>	-  Updates and overwrites trailer duration, size and resolution fields in Checker database<br>
- <b>adjust frame</b>	-  Adjust trailers by current frame rate (i.e. adjust frame 25)<br>
- <b>adjust number</b>	-  Adjust trailers by movie number or range (i.e. adjust movie 1 or adjust movie 1 10)
- <b>stats</b>		-  Generates summary statistics for trailers<br>
- <b>stats frame</b>	-  Generates frame rate summary statistics for local trailers<br>
- <b>show</b>           -  Generates a listing of all Mezzmo trailers with an error status <br>                          
- <b>show name</b>      -  Displays trailer information for movie name (i.e. show name "Christmas Vacation" ) <br>
- <b>show number</b>    -  Displays trailer information for movie number (i.e. show number 1215) <br>
- <b>show files</b>     -  Displays orphaned local trailer files which do not have a Mezzmo database trailer entry <br>
- <b>clean name</b>     -  Clears trailer trailer information for movie name (i.e. clean name "Christmas Vacation" ) <br>
- <b>clean number</b>   -  Clears trailer database information for movie number (i.e. clean number 1215)  <br>
- <b>clean files</b>    -  Deletes orphaned local trailer files which do not have a Mezzmo database trailer entry <br> 
- <b>backup</b>         -  Creates a time stamped file name backup of the Mezzmo Trailer Checker database <br> 
          
         
 The CSV export utility currently requires Python version 3.<br/><br/>

See the latest updates on the <a href="https://github.com/jbinkley60/MezzmoTrailerChecker/wiki">Mezzmo Trailer wiki</a>.


