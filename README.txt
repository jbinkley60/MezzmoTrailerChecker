v0.0.23 04/20/2024

- Fixed bug where Clean Files command was only checking .mp4 trailer files and 
  not .mkv trailer files.
- Updated yt-dlp.exe to eliminate Android warning messages

v0.0.22 3/25/2024

- Fixed getting IMDB trailer information when using an IMDB-API key.  IMDB-API
  changed their URL to TV-API.  This release fixes the issue and previous IMDB-API
  keys should continue to work normally.

v0.0.21 3/14/2024

- Updated yt-dlp.exe to eliminate 404 error messages
- Fixed minor bug detecting 1080P / 49k audio  format (140/139)
- Added logging of fetch and trailer formats results commands to logfile for
  easier troubleshooting

v0.0.20 2/22/2024

- Added the ability to manually enter your own IMDB trailer URLs vs. needing
  an IMDB key.  See config file.
- Updated version of yt-dlp.exe to address IMDB download issues with certain
  newer trailers
- Minor bugfix where trailer format conversion from mp4 to mkv would stall
  if destination file name already existed.

v0.0.19 10/8/2023

- Fixed a bug where a You Tube trailer URL which started with http:// vs. 
  https:// would cause an index out of range error. 

v0.0.18 9/29/2023

- Fixed a bug which would occur when an IMDB movie trailer had a comma in the 
  name when fetched and the trailer needed the frame rate or audio adjusted.
- Added option to output trailers in mkv format instead of mp4.  This allows
  Roku devices and similar which don't support higher resolution mp4 video
  playback to be able to play local trailers.  There is also a new "adjust 
  format" command to do bulk conversions from mp4 to mkv up to 200 trailers
  for each run.  

v0.0.17 8/9/2023

- Fixed bug introduced in v0.0.15 which was causing You Tube 403 errors due to 
  an improper trailer format response parsing.  This would cause You Tube 720P
  trailer fetch attempts when a 720P trailer format was not available.
- Added logging to show format for attempted fetch trailer requests for IMDB or
  You tube. Previously only successful trailer fetch results would be logged.
- Updated yt-dlp.exe from v2023.02.17 to v2023.07.06

v0.0.16 8/5/2023

- Fixed a bug where a You Tube server 403 error would cause the trailer checker
  to stop fetching any further trailers.  Now trailers which cause a 403 error
  will be marked as bad and removed from Mezzmo.

v0.0.15 7/5/2023

- Added option to prepend "ytube_" to You Tube trailer names to assist with 
  future trailer soruces, including manual local trailers. 

v0.0.14 6/27/2023

- Simplified the IMDB trailer naming, removing random generated characters by
  the trailer checker.  Now random characters will only be added to IMDB 
  trailers  if the tailer file name is a duplicate of an already existing 
  trailer file. This is consitent with how You Tube trailers are named.  The
  prior IMDB naming structure will continue to work fine.  This only impacts 
  new IMDB local trailers.
- Added "clean bad" and "clean long" commands to remove trailer records from
  the Trailer Checker database which are displayed with a 'Show" command.  
  Trailers that are long or bad do not get updated into mezzmo but will stay
  in the Trailer Checker database until cleaned.  This do not cause a problem.
  These new commands just help keep the trailer database cleaner.
- Improved duplicate trailer name checking when multiple You Tube trailer URLs 
  point to the same file name for the same new movie fetch.  

v0.0.13 6/23/2023

- Finally stomped out the bug with invalid characters in the trailer names for
  both You Tube and IMDB trailers which would not allow local trailers to be 
  copied to the local trailer folder.
- Improved available formats matching for both You Tube and IMDB trailers.

v0.0.12 6/22/2023

- Fixed a bug where file names which contained a + character could not be re-
  encoded by ffmpeg and the trailer file would not be copied to the local trailer
  folder
- Added support for fetching IMDB trailers.  When enabled and an IMDB trailer
  is found, they will be placed first in the list in Mezzmo. 

v0.0.11

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
