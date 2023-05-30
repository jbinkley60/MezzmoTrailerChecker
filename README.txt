v0.0.11 5/30/2023

-  Added "clean files" and "show files" commands to display and delete orphaned
   trailer files which do not have a Mezzmo trailer entry in the Mezzmo library
-  Added IMDB movie numbers to the mTrailers table to prepare for upcoming
   support for local IMDB trailers
-  Added commit to trailer database after each 500 checks during large full 
   library trailer database checks 

v0.0.10 5/26/2023

-  Added hardware encoding support for nVidia to speed up converting trailers
-  Fixed minor bug introduced with v0.0.9 which would cause long trailers to
   go through frame rate adjustments and be copied into the trailer folder 
   vs. being discarded.

v0.0.9  5/20/2023

-  Added statistics for count of movies with local trailers and those with no
   movie trailers in Mezzmo.
-  Added trailer fps check to add trailer frame rate to trailer checker database
-  Fixed bug where a check new would continually check the same trailers vs. 
   checking the oldest last checked trailers.
-  Fixed minor bug where check new would not check a local trailer with "youtube"
   trailer in the file name.
-  Added the ability to automatically adjust / standardize local trailer frame
   rates and audio levels as new local trailers are fetched with a backup option
   to retain the original unmodified local trailer.
-  Added on demand feature to adjust frame rate and audio levels by trailer frame
   rate, movie number or a range of movies by number.
-  Added frame rate statistics display.


v0.0.8 5/2/2023

-  Improved trailer file naming for You Tube trailers with very short names
   filled with odd characters.
-  Fixed command line error if the first argument was invalid.  Now the help
   screen will appear vs. a Python error.

v0.0.7 4/27/2023

-  Improved trailer file name dupe checking when a movie has many trailers with
   the same name after trimming extraneous You Tube characters.
-  Added average trailer file size calculation to the stats output
-  Added "CSV notrail" command to generate a listing of all movies in the Mezzmo
   database which have no trailers.
-  Increased movies per fetch maximum to 50 per run and You Tube trailer fetches
   per day to 400.
-  Code cleanup and additional Python level error checking

v0.0.6 4/22/2023

-  Added detection for trailer files where the video stream is missing or the 
   resolution cannot properly be determined by ffmpeg.
-  Fixed minor bug which could cause a movie file viewed with "show name" to 
   have it also cleaned from the Mezzmo Trailer Checker database.
-  Added the ability to fetch specific movie trailers by name or number

v0.0.5 4/21/2023

-  Added # of files and storage consumed by the trailer folder to the stats output.
-  Fixed another minor bug which was causing Long and Invalid statuses to be changed
   to bad in the mTrailer table.
-  Fixed issue where after trimming extraneous You Tube characters in local trailer
   names, a duplicate trailer name might exist. 
-  Added the ability to delete trailers from the Mezzmo Trailer Checker database by
   movie name or number.  This is useful when you want to update trailers in Mezzmo
   and have the tracker learn/check them again.
-  Added backup command to create backups of the Mezzmo Trailer Checker database    
 
v0.0.4 4/19/2023

-  Fixed minor bug where official trailers weren't always put at the top of the list 
   when preferred official was set in the settings.
-  Fixed minor bug which was causing some of the bad trailer statuses to be overwritten
   to good during trailer check by movie function.
-  Fixed minor bug which would cause Bad trailers to be readded to Mezzmo
-  Major performance improvement over version 0.0.3 when syncing with Mezzmo by modifying
   the trailer checker database indexes.
-  Added "show" command to provide a screen display of all trailers with errors. The 
   status for all trailers can be seen with the "csv trailer" command.

v0.0.3 4/17/2023

-  Fixed bug with unicode characters in ffmpeg output file when calculating duration
   during check function that would cause Trailer Checker to stop. 
-  Added additional error checking for check function and a status display output for
   every 100 media file checks.
-  Added checking for invalid trailer file names which ffmpeg cannot process.  Trailer
   files which contain an &. These would be manually added trailers since the checker
   will automatically remove an & from a trailer file name.
-  Added checking for missing trailer files which are in Mezzmo but are not found in
   the trailer folder.
-  Fixed issue where duplicate trailer entries could end up in mTrailer table after
   reordering due to user preferences causing Mezzmo trailer sequence renumbering and
   mTemp table not being cleared between movie trailer fetching.   

v0.0.2  4/16/2023

- Added checking to ensure ffmpeg, yt-dlp and the Mezzmo database files are found.
- Added checking for trailer resolution and duration  
- Added additional options including local trailers only, You Tube download limit,
  prefer local trailers, prefer official trailers and trailer checker option
- Added command line options for checking / updating trailer resolution, size and
  duration, and statistics

***  No upgrade from 0.0.1 to 0.0.2 is available.  
     Trailer database file mezzmo_trailer.db must be deleted and rebuilt
     Future seamless upgardes will be allowed. 
     There were too many database updates between v0.0.1 and 0.0.2 to support this  

v0.0.1  4/9/2023

- Inital alpha test release 
