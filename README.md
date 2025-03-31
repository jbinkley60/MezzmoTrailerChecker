# Mezzmo Trailer Checker
A utility to help you manage your Mezzmo local trailer files.  


## Features:

- Now available in both native Python and Windows x64 EXE formats  <sup>**New**</sup>
- Read current You Tube movie trailer information from the Mezzmo database
- Movie trailers can be fetched by newest, oldest, movie name or movie number
- Track movies which have local trailers, which don't and last checked time
- Download high quality trailers from You Tube and IMDB for local playback
- Fast You Tube and IMDB download speeds with daily limit setting
- Detect You Tube trailers which cannot be downloaded and marks them "Bad"
- Automatically remove bad trailers from Mezzmo 
- Automatically normalize and trim the You Tube and IMDB trailers names
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
- Option to set output trailer output format to mp4 or mkv and perform <a href="https://github.com/jbinkley60/MezzmoTrailerChecker/wiki/Running-Mezzmo-Trailer-Checker#adjusting-formats">bulk adjustments</a> to current local trailers
- Hardware encoding acceleration to improve speed
- Option to prefer official trailers
- Option for only local trailers
- Option to only download TMDB YouTube trailers and ignore clips, featurettes, shorts etc...
- Check feature to update trailer size, resolution and duration after manual trailer changes
- Added checks for missing trailer files and trailer files with invalid names
- Show and delete orphaned local trailer files with do not have a Mezzmo database trailer entry - <b>Mew</b>
- Full detailed logfile
- Full Trailer checker statistics
- <a href="https://github.com/jbinkley60/MezzmoTrailerChecker/wiki/Mezzmo-Trailer-Checker-Data-Export">CSV export</a> of trailer information, checker history and movies in the Mezzmo DB without trailers
- Command line backups of Mezzmo Trailer Checker database
- User ability to clear trailer information by movie name, database number or status 
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
- <b>trailer name</b>   -  Runs trailer checker for movie name (i.e. trailer name "Christmas Vacation" ) <br>
- <b>trailer number</b> -  Runs trailer checker for movie number (i.e. trailer number 1215)  <br> 
- <b>sync</b>           -  Syncs the Mezzmo Trailer Checker to the Mezzmo database without fetching any trailers. <br> 
- <b>csv trailer</b>    -  Creates a CSV file with the trailer information in the Mezzmo Trailer Checker<br> 
- <b>csv history</b>    -  Creates a CSV file with the history information in the Mezzmo Trailer Checker<br>
- <b>csv notrail</b>    -  Creates a CSV file with a listing of all movies in the Mezzmo database with no trailers<br>
- <b>check</b>		-  Updates missing trailer duration, size or resolution information in the Checker database<br>
- <b>check new</b>	-  Updates and overwrites trailer duration, size and resolution fields in Checker database<br>
- <b>adjust frame</b>	-  Adjust trailers by current frame rate (i.e. adjust frame 25)<br>
- <b>adjust number</b>	-  Adjust trailers by movie number or range (i.e. adjust movie 1 or adjust movie 1 10) <br>
- <b>adjust format x</b>-  Adjust trailer output format (i.e. adjust format 20 . Converts format for 20 trailers) 200 is max <br>
- <b>adjust format x number</b>	-  Adjust trailer format output for movie number x  <br>
- <b>stats</b>		-  Generates summary statistics for trailers<br>
- <b>stats frame</b>	-  Generates frame rate summary statistics for local trailers<br>
- <b>show</b>           -  Generates a listing of all Mezzmo trailers with an error status <br>                          
- <b>show name</b>      -  Displays trailer information for movie name (i.e. show name "Christmas Vacation" ) <br>
- <b>show number</b>    -  Displays trailer information for movie number (i.e. show number 1215) <br>
- <b>show files</b>     -  Displays orphaned local trailer files which do not have a Mezzmo database trailer entry <br>
- <b>show status/b>     -  Displays local trailer information with status of Bad, Long, Skip or Missing <br>
- <b>clean name</b>     -  Clears trailer database information for movie name (i.e. clean name "Christmas Vacation" ) <br>
- <b>clean number</b>   -  Clears trailer database information for movie number (i.e. clean number 1215)  <br>
- <b>clean bad</b>      -  Clears trailer database information for trailers with Bad status <br>
- <b>clean long</b>     -  Clears trailer database information for trailers with Long status  <br>
- <b>clean skip</b>     -  Clears trailer database information for trailers with Skip status  <br>
- <b>clean files</b>    -  Deletes orphaned local trailer files which do not have a Mezzmo database trailer entry <br>
- <b>clean missing</b>  -  Clears trailer database information for trailers with Missing trailer file status <br>
- <b>backup</b>         -  Creates a time stamped file name backup of the Mezzmo Trailer Checker database <br>
- <b>update</b>         -  Force update check for yt-dlp.exe.  Otherwise check is once a day. <br> 
          
         
 The CSV export utility currently requires Python version 3 unless you are using the exe version.<br/><br/>

See the latest updates on the <a href="https://github.com/jbinkley60/MezzmoTrailerChecker/wiki">Mezzmo Trailer Checker wiki</a>.

<br>
<br/><img src="icon.png" width="40%" height="40%">   <img src="tmdb.jpg" width="40%" height="40%">




