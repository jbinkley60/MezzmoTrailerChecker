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
