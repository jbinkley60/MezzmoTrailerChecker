# -*- coding: utf-8 -*-
# #!/usr/bin/python
import os, fnmatch, sys, csv, json, glob
from datetime import datetime, timedelta
import time
import urllib.request, urllib.parse, urllib.error
import http.client
import mimetypes
import subprocess
import string, random, re, base64
from urllib.request import Request, urlopen

trailerdb = 'mezzmo_trailers.db'
tr_config = {}
totcount = bdcount = gdcount = mvcount = nontrcount = 0
trlcount = skipcount = longcount = 0

movie_url = 'https://api.themoviedb.org/3/movie/{}?'
headers = {'User-Agent': 'Mezzmo Trailer Checker 0.0.29'}
tmdb_key = 'a6898792995042896256585082db0842'

version = 'version 0.0.29'

sysarg1 = sysarg2 = sysarg3 = sysarg4 = ''

if len(sys.argv) == 2:
    sysarg1 = sys.argv[1]
if len(sys.argv) == 3:
    sysarg1 = sys.argv[1]   
    sysarg2 = sys.argv[2]

if len(sys.argv) == 4:
    sysarg1 = sys.argv[1]   
    sysarg2 = sys.argv[2]
    sysarg3 = sys.argv[3]
 
if len(sys.argv) == 5:
    sysarg1 = sys.argv[1]   
    sysarg2 = sys.argv[2]
    sysarg3 = sys.argv[3]
    sysarg4 = sys.argv[4]

def getConfig():

    try: 

        global tr_config, version      
        fileh = open("config.txt")                                     # open the config file
        linecount = len(fileh.readlines())
        fileh.seek(0)                                                  # Move file pointer to the beginning            
        data = fileh.readline()                                        # Get Mezzmo database location
        dataa = data.split('#')                                        # Remove comments
        data = dataa[0].strip().rstrip("\n")                           # cleanup unwanted characters
        mezzmodbfile = data + "Mezzmo.db"

        data = fileh.readline()                                        # Get local trailer location
        datab = data.split('#')                                        # Remove comments
        ltrailerloc = datab[0].strip().rstrip("\n")                    # cleanup unwanted characters

        data = fileh.readline()                                        # Get Mezzmo trailer location
        dataj = data.split('#')                                        # Remove comments
        mtrailerloc = dataj[0].strip().rstrip("\n")                    # cleanup unwanted characters

        data = fileh.readline()                                        # Get number of movies to fetch
        datac = data.split('#')                                        # Remove comments
        mfetchcount = datac[0].strip().rstrip("\n")                    # cleanup unwanted characters
        if int(mfetchcount) > 50:
            mfetchcount = 50                                           # Max number of movies to fetch is 50

        data = fileh.readline()                                        # Get number of trailers per movie
        datad = data.split('#')                                        # Remove comments
        trfetchcount = datad[0].strip().rstrip("\n")                   # cleanup unwanted characters
        if int(trfetchcount) > 100:
            trfetchcount = 100                                          # Max trailer per movie is 100

        data = fileh.readline()                                        # Get trailer max resolution
        datae = data.split('#')                                        # Remove comments
        maxres = datae[0].strip().rstrip("\n")                         # cleanup unwanted characters
        if maxres not in ['1080', '720', '480'] :
            maxres = '720'                                             # Default to 720P

        data = fileh.readline()                                        # Maximum trailer duration
        datan = data.split('#')                                        # Remove comments
        maxdur = datan[0].strip().rstrip("\n")                         # cleanup unwanted characters

        data = fileh.readline()                                        # Get metadata lock option
        if data != '':
            dataf = data.split('#')                                    # Remove comments
            mlock = dataf[0].strip().rstrip("\n")                      # cleanup unwanted characters
        else:
            mlock = 'Yes'                                              # Default to Yes

        data = fileh.readline()                                        # Get Prefer Local Trailers
        if data != '':
            datag = data.split('#')                                    # Remove comments
            mperf = datag[0].strip().rstrip("\n")                      # cleanup unwanted characters
        else:
            mperf = 'Yes'                                              # Default to yes  

        data = fileh.readline()                                        # Get Prefer Official Trailers
        if data != '':
            datao = data.split('#')                                    # Remove comments
            ofperf = datao[0].strip().rstrip("\n")                     # cleanup unwanted characters
        else:
            ofperf = 'Yes'                                             # Default to yes  

        data = fileh.readline()                                        # Get Order by size
        if data != '':
            datah = data.split('#')                                    # Remove comments
            obsize = datah[0].strip().rstrip("\n")                     # cleanup unwanted characters
        else:
            obsize = 'No'                                              # Default to No

        data = fileh.readline()                                        # Get Loal Trailers Only
        if data != '':
            datak = data.split('#')                                    # Remove comments
            onlylt = datak[0].strip().rstrip("\n")                     # cleanup unwanted characters
        else:
            onlylt = 'Yes'                                             # Default to Yes

        data = fileh.readline()                                        # Logfile location
        if data != '':
            datai = data.split('#')                                    # Remove comments
            logoutfile = datai[0].strip().rstrip("\n")                 # cleanup unwanted characters         
        else:
            logoutfile = 'logfile.txt'                                 # Default to logfile.txt

        data = fileh.readline()                                        # Maximum number of movies to check
        datal = data.split('#')                                        # Remove comments
        maxcheck = datal[0].strip().rstrip("\n")                       # cleanup unwanted characters
        if int(maxcheck) > 10000:
            maxcheck = 10000                                           # Max movies to check is 10,000

        data = fileh.readline()                                        # Get number of daily You Tube downloads
        datam = data.split('#')                                        # Remove comments
        youlimit = datam[0].strip().rstrip("\n")                       # cleanup unwanted characters
        if int(youlimit) > 400:
            youlimit = 400                                             # Max daily downloads is 400

        data = fileh.readline()                                        # Get trailer frame rate
        if data != '':
            datap = data.split('#')                                    # Remove comments
            trfrate = datap[0].strip().rstrip("\n")                    # cleanup unwanted characters
        else:
            trfrate = '0'  

        data = fileh.readline()                                        # Keep original trailer backup
        if data != '':
            dataq = data.split('#')                                    # Remove comments
            trback = dataq[0].strip().rstrip("\n")                     # cleanup unwanted characters
        else:
            trback = 'No'                                              # Default to No

        data = fileh.readline()                                        # Get audio level adjustment in %
        datar = data.split('#')                                        # Remove comments
        audiolvl = datar[0].strip().rstrip("\n")                       # cleanup unwanted characters
        if int(audiolvl) > 200 or int(audiolvl) < 30:
            audiolvl = '100'                                           # Min and max are 30% and 200%

        data = fileh.readline()                                        # Get HW encoding
        if data != '':
            datas = data.split('#')                                    # Remove comments
            hwenc = datas[0].strip().rstrip("\n")                      # cleanup unwanted characters
        else:
            hwenc = 'None'                                             # Default to None  

        data = fileh.readline()                                        # Get IMDB key
        if data != '':
            datat = data.split('#')                                    # Remove comments
            if 'none' not in datat[0].lower():
                imdbky = datat[0].strip().rstrip("\n")                 # cleanup unwanted characters
            else:
                imdbky = 'None'
        else:
            imdbky = 'None'                                            # Default to None

        data = fileh.readline()                                        # Get You Tube prepend option
        if data != '':
            datau = data.split('#')                                    # Remove comments
            ytube = datau[0].strip().rstrip("\n")                      # cleanup unwanted characters
        else:
            ytube = 'Yes'

        data = fileh.readline()                                        # Get output format option
        if data != '':
            datav = data.split('#')                                    # Remove comments
            tformat = datav[0].strip().rstrip("\n").lower()            # cleanup unwanted characters
        else:
            tformat = 'mp4'

        if linecount > 22:
            data = fileh.readline()                                    # Check for trailers only option
            if data != '':
                dataw = data.split('#')                                # Remove comments
                tronly = dataw[0].strip().rstrip("\n")                 # cleanup unwanted characters
            else:
                tronly = "No"
        else:
            tronly = "No" 

        if linecount > 23:
            data = fileh.readline()                                    # Check for clean skipped tailers option
            if data != '':
                datax = data.split('#')                                # Remove comments
                cleanskp = datax[0].strip().rstrip("\n")                 # cleanup unwanted characters
            else:
                cleanskp = "No"
        else:
            cleanskp = "No"                
     
        fileh.close()                                                  # close the file
        
        tr_config = {
                     'dbfile': mezzmodbfile,
                     'ltrailerloc': ltrailerloc,
                     'mtrailerloc': mtrailerloc,
                     'mcount': mfetchcount,
                     'trcount': trfetchcount,
                     'maxres': maxres,
                     'maxdur': maxdur,
                     'mlock': mlock,
                     'mperf': mperf,
                     'ofperf': ofperf,
                     'obsize': obsize,
                     'onlylt': onlylt,
                     'logoutfile': logoutfile,
                     'maxcheck': maxcheck,
                     'youlimit': youlimit,
                     'trfrate': trfrate,
                     'trback': trback,
                     'audiolvl': audiolvl,
                     'hwenc': hwenc,
                     'imdbky': imdbky,
                     'ytube': ytube,
                     'tformat': tformat,
                     'tronly': tronly,
                     'cleanskp': cleanskp,
                    }

        if not tformat in ['mkv', 'mp4']:
            tformat = 'mp4'
            mgenlog = 'Invalid output format in config file.  Defaulting to mp4 format'
            genLog(mgenlog)
            print(mgenlog) 

        configuration = [mezzmodbfile, ltrailerloc, mtrailerloc, mfetchcount, trfetchcount]
        configuration1 = [maxres, maxdur, mlock, mperf, ofperf, obsize, onlylt, logoutfile]
        configuration2 = [maxcheck, youlimit, trfrate, trback, hwenc, tformat, tronly, cleanskp]
        mgenlog = ("Mezzmo Trailer Checker started - " + version)
        print(mgenlog)
        genLog(mgenlog)
        mgenlog = 'Number of lines in the config file: ' + str(linecount)
        genLog(mgenlog)
        genLog(str(configuration))               # Record configuration to logfile
        genLog(str(configuration1))
        genLog(str(configuration2))        
        mgenlog = "Finished reading config file."
        genLog(mgenlog)       
        return 
 
    except Exception as e:
        #print (e)
        mgenlog = 'There was a problem parsing the config file. ' + str(e)
        genLog(mgenlog)
        print(mgenlog)


def checkCommands(sysarg1, sysarg2):                                   # Check for valid commands
  
    if len(sysarg1) > 1 and sysarg1.lower() not in ['trailer', 'csv', 'sync', 'help', 'check', 'stats',   \
        'show', 'clean', 'backup', 'adjust', 'update']:
        displayHelp(sysarg1)
        sys.exit()
    if len(sysarg1) <= 1 or '?' in sysarg1.lower() or sysarg1.lower() == 'help':
        displayHelp(sysarg1)
        sys.exit()


def displayHelp(sysarg1):                                 #  Command line help menu display

        print('\n=====================================================================================================')
        print('\nThe only valid commands are -  trailer, sync, csv, check, stats, show, clean, backup, adjust, update and help  ')
        print('\nExample:  trailer_checker.py trailer')      
        print('\ntrailer\t\t - Runs the trailer checker normally starting with the first movie in the Mezzmo database')
        print('trailer new\t - Runs the trailer checker normally starting with the newest movie in the Mezzmo database')
        print('trailer name\t - Runs trailer checker for movie name (i.e. trailer name "Christmas Vacation" )')
        print('trailer number\t - Runs trailer checker for movie number (i.e. trailer number 1215) ')
        print('\nsync\t\t - Syncs the Mezzmo Trailer Checker to the Mezzmo database without fetching any trailers')
        print('\ncsv trailer\t - Creates a CSV file with the trailer information in the Mezzmo Trailer Checker')
        print('csv history\t - Creates a CSV file with the history information in the Mezzmo Trailer Checker')
        print('csv notrail\t - Creates a CSV file with a listing of all movies in the Mezzmo database with no trailers')
        print('\ncheck\t\t - Updates missing trailer duration, size or resolution information in the Checker database')
        print('check new\t - Updates and overwrites trailer duration, size and resolution fields in Checker database')
        print('\nadjust frame\t - Adjust trailers by current frame rate (i.e. adjust frame 25)')
        print('adjust number\t - Adjust trailers by movie number or range (i.e. adjust movie 1 or adjust movie 1 10)')
        print('adjust format\t - Adjust trailer output format (i.e. adjust format 20 .  Converts format for 20 trailers)')
        print('adjust format x number\t - Adjust trailer output format for movie with number x.')
        print('\nstats\t\t - Generates summary statistics for trailers')
        print('stats frame\t - Generates frame rate summary statistics for local trailers')
        print('\nshow\t\t - Generates a listing of all Mezzmo trailers with an error status')
        print('show name\t - Displays trailer information for movie name (i.e. show name "Christmas Vacation" )')
        print('show number\t - Displays trailer information for movie number (i.e. show number 1215) ')
        print('show files\t - Displays orphaned local trailer files which do not have a Mezzmo database trailer entry')
        print('show status\t - Displays local trailer information with status of Bad, Long, Skip or Missing')
        print('\nclean name\t - Clears trailer database information for movie name (i.e. clean name "Christmas Vacation" )')
        print('clean number\t - Clears trailer database information for movie number (i.e. clean number 1215) ')
        print('clean Bad\t - Clears trailer database information for trailers with Bad status ')
        print('clean Long\t - Clears trailer database information for trailers with Long status ')
        print('clean files\t - Deletes orphaned local trailer files which do not have a Mezzmo database trailer entry')
        print('clean skip\t - Clears trailer database information for trailers with Skip status ')
        print('clean missing\t - Clears trailer database information for trailers with Missing trailer file status ')
        print('\nbackup\t\t - Creates a time stamped file name backup of the Mezzmo Trailer Checker database')
        print('update\t\t - Force update check for yt-dlp.exe.  Otherwise check is once a day.') 
        print('\n=====================================================================================================')
        print('\n ')


def getMezzmoTrailers(sysarg1= ''):                                     #  Query Mezzmo trailers  
    
    global tr_config
      
    mgenlog = "The Mezzmo DB file is: " + tr_config['dbfile']
    genLog(mgenlog)

    try:
        if not sysarg1.lower() in ['trailer', 'sync']:
            return
        else:
            genLog("Getting Mezzmo trailer data.")                          
            trdb = openTrailerDB()
            db = openMezDB()
            dbcurr = db.execute('Select MGOFile.File, MGOFileExtras.ID, MGOFileExtras.FileID,        \
            MGOFileExtras.TypeUID, MGOFileExtras.File, MGOFile.Lock, MGOFile.Title, MGOFile.IMDB_ID, \
            MGOFile.TheMovieDB_ID, MGOFile.TheTVDB_ID from MGOFileExtras INNER JOIN  MGOFile on      \
            MGOFile.ID = MGOFileExtras.FileID order by MGOFileExtras.FileID',)
            dbtuples = dbcurr.fetchall()     
            del dbcurr
            for a in range(len(dbtuples)):
                curp = trdb.execute('SELECT extras_ID, extras_FileID FROM mTrailers WHERE extras_File=?',     \
                (dbtuples[a][4],))                                     #  Check Trailers
                currTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')                
                trailertuple = curp.fetchone()
                if not trailertuple:                                   #  Add to trailer database
                    trdb.execute('INSERT into mTrailers (dateAdded, mgofile_file, extras_ID, extras_FileID,   \
                    extras_TypeUID, extras_File, mgofile_lock, mgofile_title, IMDB_ID, TheMovieDB_ID,         \
                    TheTVDB_ID) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',  (currTime, dbtuples[a][0],        \
                    dbtuples[a][1], dbtuples[a][2], dbtuples[a][3], dbtuples[a][4], dbtuples[a][5],           \
                    dbtuples[a][6], dbtuples[a][7], dbtuples[a][8], dbtuples[a][9],))
                else:                                                  #  Update trailer database
                    trdb.execute('UPDATE mTrailers SET extras_File=?, mgofile_lock=?, mgofile_title=?,        \
                    extras_ID=?, extras_FileID=?, IMDB_ID=?, TheMovieDB_ID=?, TheTVDB_ID=?                    \
                    WHERE extras_File=?', (dbtuples[a][4], dbtuples[a][5], dbtuples[a][6], dbtuples[a][1],    \
                    dbtuples[a][2], dbtuples[a][7], dbtuples[a][8], dbtuples[a][9], dbtuples[a][4],))
            trdb.commit()

            if sysarg1.lower() in ['sync'] and sysarg2.lower() in ['clean']:
                dbcurr = db.execute('SELECT * FROM MGOFileExtras')    # Get Mezzmo trailers
                dbtuples = dbcurr.fetchall()     
                del dbcurr
                trdb.execute('DELETE FROM mTemp')
                trdb.commit()

                for a in range(len(dbtuples)):                        # Insert into Temp table
                    trdb.execute('INSERT into mTemp (extras_ID, extras_FileID, extras_TypeUID, extras_File)  \
                    values (?, ?, ?, ?)',  (dbtuples[a][0], dbtuples[a][1], dbtuples[a][2], dbtuples[a][3],))
                trdb.commit()               

            trdb.close()
            db.close()
            mgenlog = "Finished getting Mezzmo Trailer records." 
            genLog(mgenlog)  
            print(mgenlog)

    except Exception as e:
        #print (e)
        mgenlog = 'There was an error getting Mezzmo trailer information ' + str(e)
        print(mgenlog)
        genLog(mgenlog)           


def genLog(mgenlog):                                        #  Write to logfile

        global tr_config
        logoutfile = tr_config['logoutfile']
        fileh = open(logoutfile, "a")                       #  open logf file
        currTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
        data = fileh.write(currTime + ' - ' + mgenlog + '\n')
        fileh.close()


def checkLogfile():                                        # Checks / trims the size of the logfile

    try:
        global tr_config
        logoutfile = tr_config['logoutfile']
        fileh = open(logoutfile, "r+")                     #  open log file
        flines = fileh.readlines()
        fcount = len(flines)
        if fcount > 11000:
            fileh.seek(0)
            fileh.truncate()
            fileh.writelines(flines[fcount - 10000:])
        fileh.close()
        mgenlog = 'The number of lines in the logfile is: ' + str(len(flines))
        genLog(mgenlog)
    except:
        print('\nThere was a problem trimming the logfile length')  


def checkDatabase():

    try:
        global trailerdb

        db = openTrailerDB()

        db.execute('CREATE table IF NOT EXISTS mTrailers (dateAdded TEXT, mgofile_title TEXT,         \
        mgofile_file INTEGER, extras_ID  INTEGER, extras_FileID INTEGER, extras_TypeUID TEXT,         \
        extras_File TEXT, mgofile_lock INTEGER, lastchecked TEXT, tr_resol INTEGER, tr_size INTEGER,  \
        trStatus TEXT, trDuration INTEGER, var1 TEXT, var2 TEXT, var3 TEXT, var4 TEXT)')
        db.execute('DROP INDEX IF EXISTS trailer_1')    # Remove old unique index
        db.execute('CREATE INDEX IF NOT EXISTS trailer_5 ON mTrailers (extras_ID, extras_FileID)')
        db.execute('CREATE INDEX IF NOT EXISTS trailer_2 ON mTrailers (mgofile_file)')
        db.execute('CREATE INDEX IF NOT EXISTS trailer_3 ON mTrailers (dateAdded)')
        db.execute('CREATE INDEX IF NOT EXISTS trailer_4 ON mTrailers (trStatus)')

        db.execute('CREATE table IF NOT EXISTS mHistory (dateAdded TEXT, mgofile_title TEXT,          \
        mgofile_file INTEGER, extras_ID  INTEGER, extras_FileID INTEGER, extras_TypeUID TEXT,         \
        extras_File TEXT, mgofile_lock INTEGER,  tr_res TEXT, tr_size INTEGER, newfile TEXT,          \
        lastchecked TEXT, trStatus TEXT, trDuration INTEGER, var1 TEXT, var2 TEXT, var3 TEXT, var4 TEXT)')

        db.execute('CREATE table IF NOT EXISTS mTemp (mgofile_title TEXT, mgofile_file INTEGER,      \
        extras_ID  INTEGER, extras_FileID INTEGER, extras_TypeUID TEXT, extras_File TEXT,            \
        extras_FileNew TEXT, mgofile_lock INTEGER, tr_size INTEGER, tr_resol INTEGER,                \
        trDuration INTEGER, trMatch TEXT, var1 TEXT, var2 TEXT, var3 TEXT, var4 TEXT)')
        db.execute('CREATE INDEX IF NOT EXISTS trailer_11 ON mTemp (extras_FileID)')
        db.execute('CREATE INDEX IF NOT EXISTS trailer_12 ON mTrailers (extras_File)')
        db.execute('DELETE FROM mTemp')                                    # Clear temp table on startup

        db.execute('CREATE table IF NOT EXISTS mChecked (last_checked TEXT, var1 TEXT, var2 TEXT)')

        try:
            db.execute('ALTER TABLE mTrailers ADD COLUMN IMDB_ID TEXT')
            db.execute('ALTER TABLE mTrailers ADD COLUMN TheTVDB_ID TEXT')
            db.execute('ALTER TABLE mTrailers ADD COLUMN TheMovieDB_ID TEXT')
            db.execute('CREATE INDEX IF NOT EXISTS trailer_6 ON mTrailers (IMDB_ID)')
            db.execute('CREATE INDEX IF NOT EXISTS trailer_7 ON mTrailers (TheTVDB_ID)')
            db.execute('CREATE INDEX IF NOT EXISTS trailer_8 ON mTrailers (TheMovieDB_ID)')
            db.execute('ALTER TABLE mTemp ADD COLUMN IMDB_ID TEXT')
            db.execute('ALTER TABLE mTemp ADD COLUMN TheTVDB_ID TEXT')
            db.execute('ALTER TABLE mTemp ADD COLUMN TheMovieDB_ID TEXT')
            db.execute('CREATE INDEX IF NOT EXISTS trailer_13 ON mTemp (IMDB_ID)')
            db.execute('CREATE INDEX IF NOT EXISTS trailer_14 ON mTemp (TheTVDB_ID)')
            db.execute('CREATE INDEX IF NOT EXISTS trailer_15 ON mTemp (TheMovieDB_ID)')
            db.execute('ALTER TABLE mHistory ADD COLUMN IMDB_ID TEXT')
            db.execute('ALTER TABLE mHistory ADD COLUMN TheTVDB_ID TEXT')
            db.execute('ALTER TABLE mHistory ADD COLUMN TheMovieDB_ID TEXT')
            db.execute('CREATE INDEX IF NOT EXISTS history_1 ON mHistory (IMDB_ID)')
            db.execute('CREATE INDEX IF NOT EXISTS history_2 ON mHistory (TheTVDB_ID)')
            db.execute('CREATE INDEX IF NOT EXISTS history_3 ON mHistory (TheMovieDB_ID)')
        except:
            pass

        db.commit()
        db.close()
 
        mgenlog = "Mezzmo check trailer database completed."
        print (mgenlog)
        genLog(mgenlog)

    except Exception as e:
        print (e)
        mgenlog = "There was a problem verifying the trailer database file: " + trailerdb
        print(mgenlog)
        sys.exit()   


def getMovieList(sysarg1= '', sysarg2= '', sysarg3= ''):                  # Get list of movies to check

    try:
        if sysarg1.lower() not in ['trailer']:                            # Must be a valid command
            return
        global tr_config
        global totcount, bdcount, gdcount, mvcount, skipcount, trlcount, longcount, nontrcount
        imdb_found = 0
        trinfo = []               

        movielimit =  tr_config['mcount']
        trlimit = tr_config['trcount']
        mpref = tr_config['mperf']
        youlimit = tr_config['youlimit']
        maxdur = int(tr_config['maxdur'])
        imdbky = tr_config['imdbky']
        tronly = tr_config['tronly'].lower()
        localmatch = '%' + tr_config['mtrailerloc'] + '%'
        #ymatch =  'https://www.youtube%'
        ymatch = '%://www.youtube%'

        daystats = getTotals()                                            # Get current stats
        #print('Daily stats: ' + str(daystats[0]))
        if daystats[0] >= int(youlimit):
            mgenlog = "You Tube trailer download limit reached for today: " + str(daystats[0]) + " trailer check exiting."
            print(mgenlog)
            genLog(mgenlog) 
            return 

        db = openTrailerDB()

        if 'new' in sysarg2.lower():                                      # Get trailers for newest movies
            dbcurr = db.execute('SELECT extras_FileID, mgofile_title, extras_ID, extras_File, lastchecked      \
            from mTrailers WHERE extras_File not like ? and trStatus IS NULL group by extras_FileID order by   \
            extras_FileID DESC LIMIT ? ', (localmatch, movielimit, ))     # Get movie list to check trailers 
        elif 'name' in sysarg2.lower() and len(sysarg3) > 0:              # Get trailers by movie name
            target = '%' + sysarg3 + '%'
            dbcurr = db.execute('SELECT extras_FileID, mgofile_title, extras_ID, extras_File, lastchecked      \
            from mTrailers WHERE mgofile_title LIKE ? GROUP BY mgofile_title', (target,))
        elif 'number' in sysarg2.lower() and len(sysarg3) > 0:            # Get trailers by movie number
            dbcurr = db.execute('SELECT extras_FileID, mgofile_title, extras_ID, extras_File, lastchecked      \
            from mTrailers WHERE extras_FileID=? GROUP BY extras_FileID', (sysarg3,))
        else:
            dbcurr = db.execute('SELECT extras_FileID, mgofile_title, extras_ID, extras_File, lastchecked      \
            from mTrailers WHERE extras_File not like ? and trStatus IS NULL group by extras_FileID order by   \
            lastchecked, extras_FileID, extras_ID LIMIT ?', (localmatch, movielimit, ))   # Get movie list to check trailers 
        trailertuple = dbcurr.fetchall()
        del dbcurr

        if len(trailertuple) > 0:
            mgenlog = "Mezzmo Trailer Checker found " + str(len(trailertuple)) + " movies to check trailers."
            print(mgenlog)
            genLog(mgenlog) 

            for trailer in trailertuple:                                  # Check for local trailers
                trcurr = db.execute('select count (extras_ID) from mTrailers WHERE extras_File like ?   \
                and extras_FileID = ?', (localmatch, trailer[0],))        # Get count of local trailers
                counttuple = trcurr.fetchone()
                mgenlog = 'Local trailer count: ' + str(counttuple[0]) + ' for - ' + trailer[1]
                genLog(mgenlog)
                totcount += 1
                if int(counttuple[0]) > 0:                                # Update lastchecked and status
                    currTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    db.execute('UPDATE mTrailers SET lastchecked=?, trStatus=? WHERE extras_FileID=? AND \
                    trStatus IS NULL', (currTime, 'Yes', trailer[0],))
                    db.commit()
                    mgenlog = "Skipping movie, local trailers found: " + trailer[1]
                    genLog(mgenlog)
                    print(mgenlog)
                    skipcount += 1
                else:                                                     # Get list of Youtube trailers
                    chcurr = db.execute('SELECT extras_FileID, mgofile_title, extras_ID, extras_File,    \
                    IMDB_ID, TheMovieDB_ID from mTrailers WHERE extras_File like ? AND extras_FileID=?   \
                    AND trStatus IS NULL Limit ? ', (ymatch, trailer[0], trlimit,))       # Get trailer list to check
                    chktuple = chcurr.fetchall()
                    mgenlog = 'Found ' + str(len(chktuple)) + ' YouTube trailers: ' + trailer[1]
                    print(mgenlog)
                    genLog(mgenlog)
                    mvcount += 1
                    db.execute('DELETE FROM mTemp')                       # Clear temp table before writing
                    db.commit()

                    if tronly == 'yes' and len(chktuple) > 0:             # Check for valid TMDB trailers
                        tmdblist = getTMDBtrailers(chktuple[0][5])        # Get trailer only list from TMDB
                        mgenlog = 'Found ' + str(len(tmdblist)) + ' TMDB trailers: ' + trailer[1]
                        print(mgenlog)
                        genLog(mgenlog)
                        #print(str(tmdblist))
                        #print(str(chktuple))
                    else:
                        tmdblist = []

                    if 'none' not in imdbky:                              # Check IMDB trailer URL
                        imdbrtrlt, imdbtitle  = checkiTrailer(chktuple[0][4], chktuple[0][1])
                        if 'none' not in imdbrtrlt:                       # IMDB trailer found
                            imdbtitle = 'imdb_' + imdbtitle.lower().replace(' ' , '_')
                            #print('IMDB trailer found: ' + imdbrtrlt + ' ' + imdbtitle)
                            trinfo = getTrailer(imdbrtrlt, imdbtitle)
                            #print('trinfo is: ' + str(trinfo))
                            if trinfo[0] == 0 and int(trinfo[4]) <= maxdur:   # Trailer fetched and not too long
                                mgenlog = 'Trailer file fetched: ' + trinfo[3] + ' - ' + trinfo[2] + ' - ' + trinfo[1] 
                                genLog(mgenlog)
                                print(mgenlog)
                                updateHistory(trinfo, chktuple[0][3], db)     # Save trailer info to history
                                updateTemp(trinfo, chktuple[0][3], db)        # Write to temp
                                gdcount += 1                                  # Increment good trailer count
                            elif trinfo[0] == 0 and int(trinfo[4]) > maxdur:  # Trailer fetched and too long
                                updateError(chktuple[0][3], db, 'Long')
                                updateHistory(trinfo, chktuple[0][3], db)     # Save trailer info to history
                                longcount += 1                                # Increment long trailer counter
                            elif 'error' in str(trinfo).lower():
                                updateError(chktuple[0][3], db, 'Bad')
                                mgenlog = 'There was an error fetching the local trailer for: ' + imdbrtrlt
                                genLog(mgenlog)
                                print(mgenlog)
                                bdcount += 1   
                            else:                                             # Error fetching You Tube trailer
                                updateError(chktuple[0][3], db, 'Bad')
                                mgenlog = 'There was an error fetching the local trailer for: ' + imdbrtrlt
                                genLog(mgenlog)
                                print(mgenlog)
                                bdcount += 1                                  # Increment bad counter
                    
                    for ytube in chktuple:                                # Get You Tube local trailers
                        #print('trinfo is: ' + str(trinfo))
                        skip = 0
                        
                        if tronly == 'yes' and len(tmdblist) > 0 and ytube[3] not in tmdblist:
                            skip = 1
                        else:
                            trinfo = getTrailer(ytube[3]) 

                        if  skip == 0 and trinfo[0] == 0 and int(trinfo[4]) <= maxdur: # Trailer fetched and not too long
                            mgenlog = 'Trailer file fetched: ' + trinfo[3] + ' - ' + trinfo[2] + ' - ' + trinfo[1] 
                            genLog(mgenlog)
                            print(mgenlog)
                            updateHistory(trinfo, ytube[3], db)           # Save trailer info to history
                            updateTemp(trinfo, ytube[3], db)              # Write to temp
                            gdcount += 1                                  # Increment good trailer count
                        elif skip == 0 and trinfo[0] == 0 and int(trinfo[4]) > maxdur:  # Trailer fetched and too long
                            updateError(ytube[3], db, 'Long')
                            updateHistory(trinfo, ytube[3], db)           # Save trailer info to history
                            longcount += 1                                # Increment long trailer counter
                        elif skip == 0 and 'error' in str(trinfo).lower():
                            updateError(ytube[3], db, 'Bad')
                            mgenlog = 'There was an error fetching the local trailer for: ' + ytube[3]
                            genLog(mgenlog)
                            print(mgenlog)
                            bdcount += 1
                        elif skip == 1:
                            updateError(ytube[3], db, 'Skip')
                            mgenlog = 'Skipping nontrailer YouTube file: ' + ytube[3]
                            genLog(mgenlog)                               # Not Youtube trailer file 
                            print(mgenlog)
                            nontrcount += 1                               # Increment no trailer count   
                        else:                                             # Error fetching You Tube trailer
                            updateError(ytube[3], db, 'Bad')
                            mgenlog = 'There was an error fetching the local trailer for: ' + ytube[3]
                            genLog(mgenlog)
                            print(mgenlog)
                            bdcount += 1                                  # Increment bad counter
                    result = updateMezzmo(ytube[0], db)                   # Update mezzmo for MGOFile_ID
                    #print('Number of trailers is ' + str(result))
                    if result > 0:                                        # Successfully featched movie trailers
                       trlcount = trlcount + result                       # Update trailer count
                       moveTrailers()                                     # Move trailers to trailer folder
                       checkFormats(db, sysarg1, sysarg2)                 # Check / modify output formats   
 
        db.close()

    except Exception as e:
        #print (e)
        mgenlog = "There was a problem getting the movie list. " + str(e)
        print(mgenlog)
        genLog(mgenlog) 


def updateError(trurl, db, status):                                        # Update status download error

    try: 
        currTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.execute('UPDATE mTrailers SET lastchecked=?, trStatus=?, tr_resol=?, tr_size=?, trDuration=?      \
        WHERE extras_File=?',  (currTime, status, 1,1,1,trurl,))
        db.commit()

    except Exception as e:
        print (e)
        mgenlog = "There was a problem updating trailer errors in the database file: " + trurl
        print(mgenlog)
        genLog(mgenlog) 


def updateMezzmo(fileID, db):                                             # Update Mezzmo from Temp table     

    try:
        global tr_config
        mperf = tr_config['mperf'].lower()
        obsize = tr_config['obsize'].lower()
        onlylt = tr_config['onlylt'].lower()
        trcount = tr_config['trcount']
        ofperf = tr_config['ofperf'].lower()
        tformat = tr_config['tformat'].lower()
        mezzdb = openMezDB()
        trcurr = db.execute('SELECT * FROM mTrailers WHERE extras_FileID=? AND (trStatus LIKE ? OR trStatus \
        IS NULL) LIMIT ?',  (fileID, 'Yes', trcount,))
        trtuple = trcurr.fetchall()                                       # Get current trailer records
        print('The # of old trailers for: ' + str(fileID) + ' is: ' + str(len(trtuple)))
        #print(str(trtuple))

        tempcurr = db.execute('SELECT * FROM mTemp WHERE extras_fileNew LIKE ? ORDER BY tr_size DESC',  \
        ('%imdb%',))
        temptuple2 = tempcurr.fetchall() 
        if 'yes' in ofperf and 'yes' in obsize:                           # If prefer official and by size
            tempcurr = db.execute('SELECT * FROM mTemp WHERE extras_fileNew LIKE ? AND extras_fileNew NOT   \
            LIKE ? ORDER BY tr_size DESC', ('%official%', '%imdb%',))
            temptuple0 = tempcurr.fetchall() 
            tempcurr = db.execute('SELECT * FROM mTemp WHERE extras_fileNew NOT LIKE ? AND extras_fileNew   \
            NOT LIKE ? ORDER BY tr_size DESC', ('%official%', '%imdb%',))
            temptuple1 = tempcurr.fetchall()
            temptuple = temptuple2 + temptuple0 + temptuple1
        elif 'yes' in ofperf and 'no' in obsize:                          # If prefer official and by resolution
            tempcurr = db.execute('SELECT * FROM mTemp WHERE extras_fileNew LIKE ? AND extras_fileNew NOT   \
            LIKE ? ORDER BY tr_resol DESC', ('%official%', '%imdb%',))
            temptuple0 = tempcurr.fetchall()  
            tempcurr = db.execute('SELECT * FROM mTemp WHERE extras_fileNew NOT LIKE ? AND extras_fileNew   \
            NOT LIKE ? ORDER BY tr_resol DESC', ('%official%', '%imdb%',)) 
            temptuple1 = tempcurr.fetchall()
            temptuple = temptuple2 + temptuple0 + temptuple1                              
        elif 'no' in ofperf and 'yes' in obsize:                          # If prefer by size
            tempcurr = db.execute('SELECT * FROM mTemp WHERE extras_fileNew NOT LIKE ? ORDER BY tr_size     \
            DESC', ('%imdb%',)) 
            temptuple1 = tempcurr.fetchall()
            temptuple = temptuple2 + temptuple1
        else:                                                             # If prefer by resolution               
            tempcurr = db.execute('SELECT * FROM mTemp WHERE extras_fileNew NOT LIKE ?ORDER BY tr_resol     \
            DESC', ('%imdb%',)) 
            temptuple1 = tempcurr.fetchall()
            temptuple = temptuple2 + temptuple1 
        #print('Sorted tuples are: ' + str(temptuple))
        print('The # of new trailers for: ' + str(fileID) + ' is: ' + str(len(temptuple)))
        if len(temptuple) == 0:                                          # No new trailers found
            mezzdb.commit()
            mezzdb.close()
            mgenlog = 'Mezzmo trailers updated - 0' 
            genLog(mgenlog)
            print(mgenlog)
            return 0

        mezzcur = mezzdb.cursor()
        mezzcur.execute('DELETE from MGOFIleExtras WHERE FileID=?', (fileID,))            
        if 'yes' in mperf:                                               # Add prefer local trailers
            count = 1
            for temp in temptuple: 
                mezzcur.execute('INSERT into MGOFIleExtras (ID, FileID, TypeUID, File) values  \
                (?, ?, ?, ?)', (count, temp[3], temp[4], temp[6],))
                count += 1
            if 'yes' not in onlylt:                                      # Check if only local trailers
                for trlr in trtuple:
                    mezzcur.execute('INSERT into MGOFIleExtras (ID, FileID, TypeUID, File) values  \
                    (?, ?, ?, ?)', (count, trlr[4], trlr[5], trlr[6],))
                    count += 1               
        else:
            count = 1
            if 'yes' not in onlylt:                                      # Check if only local trailers
                for trlr in trtuple:
                    mezzcur.execute('INSERT into MGOFIleExtras (ID, FileID, TypeUID, File) values  \
                    (?, ?, ?, ?)', (count, trlr[4], trlr[5], trlr[6],))
                    count += 1     
            for temp in temptuple:                                       # Insert local trailers from temp table 
                mezzcur.execute('INSERT into MGOFIleExtras (ID, FileID, TypeUID, File) values  \
                (?, ?, ?, ?)', (count, temp[3], temp[4], temp[6],))
                count += 1
        mezzcur.execute('UPDATE MGOFile SET Lock=? WHERE ID=?', (temp[7], fileID,))
        db.commit()        
        mezzdb.commit()
        del mezzcur         
        mezzdb.close()

        mgenlog = 'Mezzmo trailers updated - ' + str(count - 1)
        genLog(mgenlog)
        print(mgenlog)

        return (count - 1)

    except Exception as e:
        #print (e)
        mgenlog = 'There was a problem updating Mezzmo DB for trailer info. ' + str(e)
        genLog(mgenlog)
        print(mgenlog)
        return 0 


def updateHistory(histinfo, trurl, hidb):                                 # Update history table

    try:          
        hicurr = hidb.execute('SELECT * FROM mtrailers WHERE extras_File=?', (trurl,)) 
        hituple = hicurr.fetchone()                                       # Get current trailer info
        #print(str(hituple))
        #print(str(histinfo) + ' ' + trurl)
        currTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')     # Update with local trailer info
        hidb.execute('INSERT into mHistory (dateAdded, mgofile_file, extras_ID, extras_FileID,     \
        extras_TypeUID, extras_File, mgofile_lock, mgofile_title, tr_res, tr_size, lastchecked,    \
        newfile, trDuration, trStatus, IMDB_ID, TheTVDB_ID, TheMovieDB_ID) values (?, ?, ?, ?, ?,  \
        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (hituple[0], hituple[2], hituple[3], hituple[4],     \
        hituple[5], hituple[6], hituple[7], hituple[1], histinfo[3], histinfo[2], currTime,        \
        histinfo[1], histinfo[4], hituple[11], hituple[17], hituple[18], hituple[19], )) 
        del hicurr
        hidb.commit()

    except Exception as e:
        print (e)
        mgenlog = "There was a problem updating the history table: " + trurl
        print(mgenlog)
        genLog(mgenlog) 


def updateTemp(tempinfo, trurl, tedb):                                    # Update temp table

    try:
        global tr_config
        mtrailerloc = tr_config['mtrailerloc']                            # Get config information
        mlock = tr_config['mlock'].lower()
        newtrailer =  mtrailerloc + tempinfo[1]                           # Full path to new trailer
        resolution =  int(tempinfo[3].strip('p'))                         # Resolution as number 
        tecurr = tedb.execute('SELECT * FROM mtrailers WHERE extras_File=?', (trurl,)) 
        tetuple = tecurr.fetchone()                                       # Get current trailer info      
        if 'yes' in mlock:                                                # Set lock if enabled
            newlock = 1
        else:
            newlock = tetuple[7]
        #print(str(tetuple))
        tedb.execute('INSERT into mTemp(mgofile_file, extras_ID, extras_FileID, extras_TypeUID,       \
        mgofile_lock, mgofile_title, extras_FileNew, tr_size, extras_file, tr_resol, trDuration)      \
        values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (tetuple[2], tetuple[3], tetuple[4], tetuple[5],   \
        newlock, tetuple[1], newtrailer, tempinfo[2], tetuple[6], resolution, tempinfo[4]))  # Update tr info
        del tecurr
        tedb.commit()

    except Exception as e:
        print (e)
        mgenlog = "There was a problem updating the temp table: " + tedb
        print(mgenlog)
        genLog(mgenlog)  


def checkFormats(db, sysarg1, sysarg2 = ''):                             # Check / modify output formats

    try:

        if sysarg1.lower() not in ['trailer', 'adjust']:                 # Check formats for trailer action
            return

        global tr_config
        trcount = tr_config['trcount']
        tformat = tr_config['tformat']
        ltrailerloc = tr_config['ltrailerloc']
        convert_count = 0

        mezzdb = openMezDB()

        if 'mp4' in tformat:
            target1 = '.mkv'
            target = '%' + target1
        else:
            target1 = '.mp4'
            target = '%' + target1

        tempcurr = db.execute('SELECT extras_fileNew FROM mTemp WHERE extras_fileNew LIKE ? ',  \
        (target,))
        temptuple = tempcurr.fetchall() 
        
        if len(temptuple) == 0:
            mgenlog = "No trailers found needing output format adjustments. "
            print(mgenlog)
            genLog(mgenlog)
        else:
            mgenlog = "Found " + str(len(temptuple)) + " trailers needing output format adjustments. "
            print(mgenlog)
            genLog(mgenlog)

            #print(str(temptuple))  

        for x in range(len(temptuple)):
            rpos = temptuple[x][0].rfind('\\')
            curr_trailer_name = temptuple[x][0][rpos+1:]                         # Current trailer file name
            curr_trailer = ltrailerloc + curr_trailer_name                       # Current trailer path and file name
            new_trailer = curr_trailer[:len(curr_trailer) - 3] +  tformat        # Converted trailer path and file name
            trailer_name = temptuple[x][0]                                       # Current trailer file name  
            convert_name = trailer_name[:len(trailer_name) - 3] +  tformat       # Converted trailer file name
            mgenlog = "Format conversion to " + tformat + ' beginning for trailer ' + curr_trailer
            print(mgenlog)
            genLog(mgenlog)
            #print('Format file names: ' + trailer_name + '  ' + convert_name)
            frcommand = 'ffmpeg.exe -i ' +  curr_trailer + ' -vcodec copy -acodec copy -y ' + new_trailer + ' >nul 2>nul'
            os.system(frcommand)
            #print('Trailer file names: ' + curr_trailer + '  ' + new_trailer)
            delcommand = "del " + '"' + curr_trailer + '"'                       # Remove old trailer from disk    
            os.system(delcommand)
            db.execute('UPDATE mTrailers SET extras_File=? WHERE extras_File = ? ', (convert_name, trailer_name,))
            mezzdb.execute('UPDATE MGOFIleExtras SET File = ? WHERE File = ? ', (convert_name, trailer_name,))
            mgenlog = "Format conversion successful to " + new_trailer
            print(mgenlog)
            genLog(mgenlog)
            convert_count += 1

        db.commit()
        mezzdb.commit()
        mezzdb.close()

        if convert_count > 0:
            mgenlog = "Total trailer format converions completed:  " + str(convert_count)
            print(mgenlog)
            genLog(mgenlog)

    except Exception as e:
        #print (e)
        mgenlog = "There was a problem adjusting the output formats. " + str(e)
        print(mgenlog)
        genLog(mgenlog)  
        db.close()


def noTrailer():                                         # Update Temp table for no trailer analysis

    try:
        mezzdb = openMezDB()
        mvcurr = mezzdb.execute('select MGOFile.ID, MGOFile.Title, MGOFile.File FROM MGOFile INNER     \
        JOIN MGOFileCategoryRelationship on MGOFile.ID=MGOFileCategoryRelationship.FileID INNER JOIN   \
        MGOFileCategory on MGOFileCategoryRelationship.ID=MGOFileCategory.ID WHERE Data=?',  ('Movie',))
        mvtuples = mvcurr.fetchall()     
        mezzdb.close()

        if len(mvtuples) > 0:
            db = openTrailerDB()
            db.execute('DELETE FROM mTemp')              # Clear temp table before writing
            db.commit()
            for m in range(len(mvtuples)):               # Insert Mezzmo movie list into temp table
                db.execute('INSERT into mTemp(extras_FileID, mgofile_title, mgofile_file) values      \
                (?, ?, ?)', (mvtuples[m][0], mvtuples[m][1], mvtuples[m][2],))
        db.commit()
        db.close()

    except Exception as e:
        #print (e)
        mgenlog = "There was a problem updating the temp table for finding no trailers " + str(e)
        print(mgenlog)
        genLog(mgenlog)  


def openTrailerDB():

    global trailerdb
    
    try:
        from sqlite3 import dbapi2 as sqlite
    except:
        from pysqlite2 import dbapi2 as sqlite
                       
    db = sqlite.connect(trailerdb)

    return db


def openMezDB():

    global tr_config

    dbfile = tr_config['dbfile']
   
    try:
        from sqlite3 import dbapi2 as sqlite
    except:
        from pysqlite2 import dbapi2 as sqlite
                       
    db = sqlite.connect(dbfile)
    db.execute('PRAGMA journal_mode = WAL;')
    db.execute('PRAGMA synchronous = NORMAL;')
    db.execute('PRAGMA cache_size = -10000;')

    return db


def checkiTrailer(imdb_id, meztitle):                      # Find IMDB trailer URL

    try:
        global tr_config
        imdbky = tr_config['imdbky']                       # Get IMDB Key

        if imdbky.lower() in 'manual':
            print('\nEnter the IMDB trailer URL for:  ' +  meztitle)
            print('Hit Enter to skip entering IMDB trailer URL')
            choice = input('i.e. https://www.imdb.com/video/vi2101135129/?ref_=tt_vi_i_1  ?\n')
            if len(choice) < 10:                           # Skip IMDB entry
                print('Manual IMDB trailer URL entry skipped\n')
                return ('none', 'none')                
            elif 'https://www.imdb.com/video' not in choice.lower():
                print('Invalid IMDB trailer URL entered\n')
                return ('none', 'none')
            else:
                mgenlog = ("IMDB trailer manually entered for  - " + imdb_id)
                print("\n" + mgenlog)
                genLog(mgenlog)
                return (choice.strip(), meztitle)                     

        baseurl = 'https://tv-api.com/en/API/Trailer/'

        conn = http.client.HTTPSConnection("tv-api.com", 443)
        headers = {'User-Agent': 'Mezzmo Trailer Checker 0.0.28'}
        req = '/en/API/Trailer/' + imdbky + '/' + imdb_id
        reqnew = urllib.parse.quote(req)
        encoded = urllib.parse.urlencode(headers)
        #print(req)
        conn.request("GET", reqnew, encoded)        
        res = conn.getresponse()
        data = res.read()
        #print(data.decode('utf-8'))

        jdata = json.loads(data)
        error = jdata['errorMessage']                     #  Check for IMDB errors
        if len(error) > 0 and 'Invalid API Key' in error:
            mgenlog = ("Invalid IMDB API key")
            print(mgenlog)
            genLog(mgenlog)
            return (-1, 'none', 'none') 
        elif len(error) > 0 and 'Server busy' in error:
            mgenlog = ("IMDB server busy")
            print(mgenlog)
            genLog(mgenlog)
            return ('none', 'none') 
        elif len(error) > 0 and 'TvEpisode' in error:
            mgenlog = ("No IMDB trailer for TV movie")
            print(mgenlog)
            genLog(mgenlog)
            return ('none', 'none') 
        elif len(error) > 0:
            mgenlog = ("No available IMDB trailer information ")
            print(mgenlog)
            genLog(mgenlog)
            return ('none', 'none')

        imdbtrailer = jdata['link']
        imdbtitle = jdata['title']
        #print(imdbtitle + ' ' + imdbtrailer)

        if 'https://www.imdb.com/video/' in imdbtrailer:  # Found trailer
            if imdbtrailer.count('https://') == 2:        # Fix issue with duplicate https:// from Tv API
                lpos = imdbtrailer.find('video/')
                imdbtrailer = (imdbtrailer[lpos+6:])
            mgenlog = ("IMDB trailer found for  - " + imdb_id)
            print(mgenlog)
            genLog(mgenlog)
            return (imdbtrailer, imdbtitle)            
        else:
           return ("none", "none") 

    except Exception as e:
        #print (e)
        mgenlog = "There was a problem getting the IMDB trailer information "  + str(e)
        print(mgenlog)
        genLog(mgenlog) 
        return ("none", "none")

 
def getTrailer(trailer, imdbtitle = ''):                   # Download You Tube \ IMDB trailers

    try:
        global tr_config
        maxres = int(tr_config['maxres'])                  # Get max resolution
        tr_cmd = fmt = ''
        formats = str(getFormats(trailer, imdbtitle))     # Get available trailer formats
        mgenlog = 'Trailer formats result is: ' + str(formats)
        genLog(mgenlog)
        #print('Trailer info: ' + imdbtitle + ' ' + str(maxres)) 
        if 'Error' in formats:                             # You Tube / IMDB error getting formats file
            return 'Error'
        elif 'imdb' in imdbtitle and '1080p' in formats and maxres >= 1080:         # 1080 available for IMDB   
            tr_cmd = "yt-dlp.exe -f 1080p -q --check-formats --windows-filenames " + trailer
            fmt = '1080p' 
        elif 'imdb' in imdbtitle and '720p' in formats and maxres >= 720:           # 720 available for IMDB   
            tr_cmd = "yt-dlp.exe -f 720p -q --check-formats --windows-filenames " + trailer
            fmt = '720p' 
        elif 'imdb' in imdbtitle and '480p' in formats and maxres >= 480:           # 480 available for IMDB   
            tr_cmd = "yt-dlp.exe -f 480p -q --check-formats --windows-filenames " + trailer
            fmt = '480p' 
        elif 'imdb' in imdbtitle and 'SD' in formats:                               # SD available for IMDB   
            tr_cmd = "yt-dlp.exe -f SD -q --check-formats --windows-filenames " + trailer
            fmt = '360p'        
        elif '137 mp4' in formats and '140 m4a' in formats and maxres >= 1080:      # 1080P available
            tr_cmd = "yt-dlp.exe -f 137+140 -q --check-formats --restrict-filenames " + trailer
            fmt = '1080p'
        elif '137     mp4' in formats and '140     m4a' in formats and maxres >= 1080:      # 1080P available
            tr_cmd = "yt-dlp.exe -f 137+140 -q --check-formats --restrict-filenames " + trailer
            fmt = '1080p'  
        elif '137 mp4' in formats and '139 m4a' in formats  and maxres >= 1080:     # 1080P available
            tr_cmd = "yt-dlp.exe -f 137+139 -q --check-formats --restrict-filenames " + trailer
            fmt = '1080p'
        elif '137     mp4' in formats and '139     m4a' in formats  and maxres >= 1080:     # 1080P available
            tr_cmd = "yt-dlp.exe -f 137+139 -q --check-formats --restrict-filenames " + trailer
            fmt = '1080p'  
        elif '22  mp4' in formats and maxres >= 720:                                # 720P available
            tr_cmd = "yt-dlp.exe -f 22 -q --restrict-filenames " + trailer
            fmt = '720p'
        elif '22      mp4' in formats and maxres >= 720:                            # 720P available
            tr_cmd = "yt-dlp.exe -f 22 -q --restrict-filenames " + trailer
            fmt = '720p'  
        elif  '135 mp4' in formats and '140 m4a' in formats and maxres >= 480:      # 480P available
            tr_cmd = "yt-dlp.exe -f 135+140 -q --check-formats --restrict-filenames " + trailer
            fmt = '480p'
        elif  '135     mp4' in formats and '140     m4a' in formats and maxres >= 480:      # 480P available
            tr_cmd = "yt-dlp.exe -f 135+140 -q --check-formats --restrict-filenames " + trailer
            fmt = '480p'  
        elif  '135 mp4' in formats and '139 m4a' in formats and maxres >= 480:      # 480P available
            tr_cmd = "yt-dlp.exe -f 135+139 -q --check-formats --restrict-filenames " + trailer
            fmt = '480p'
        elif  '135     mp4' in formats and '139     m4a' in formats and maxres >= 480:      # 480P available
            tr_cmd = "yt-dlp.exe -f 135+139 -q --check-formats --restrict-filenames " + trailer
            fmt = '480p'  
        elif '18  mp4' in formats:                                                  # 360P available
            tr_cmd = "yt-dlp.exe -f 18 -q --restrict-filenames " + trailer
            fmt = '360p'
        elif '18      mp4' in formats:                                              # 360P available
            tr_cmd = "yt-dlp.exe -f 18 -q --restrict-filenames " + trailer
            fmt = '360p'
        else:
            return 'Error'                                 # No acceptable format available 
        
        #print (tr_cmd)
        mgenlog = 'Trailer fetch command: ' + tr_cmd
        genLog(mgenlog)

        if 'imdb' in imdbtitle:
            tsource = 'IMDB'
        else:
            tsource = 'You Tube'
        mgenlog = 'Attempting fetch ' + tsource + ' trailer at: ' + fmt + ' - ' + trailer
        genLog(mgenlog)
        print(mgenlog)

        fetch_result = subprocess.call(tr_cmd, shell=True)
        if fetch_result == 0:
            mgenlog = 'Fetched ' + tsource + ' trailer at: ' + fmt + ' - ' + trailer
            genLog(mgenlog)
            print(mgenlog)
            trfile = renameFiles(imdbtitle)                  # Cleanup trailer name and move to temp folder
            return [fetch_result, trfile[0], trfile[1], fmt, trfile[2]]
                                                             # Return trailer file info and status
                                                             # trfile[0] = new trailer file name
                                                             # trfile[1] = new trailer file size
                                                             # 2 = dur
        elif fetch_result == 1:
            mgenlog = "A Youtube / IMDB fetching error occured for: " + trailer
            print(mgenlog)
            genLog(mgenlog)
            return [fetch_result, '0', '0', '0', '0']
    
    except Exception as e:
        #print (e)
        mgenlog = 'There was a problem getting the formats information ' + str(e)
        genLog(mgenlog)
        print(mgenlog)


def getFormats(trailer,imdbtitle = ''):             # Get available You Tube Trailer formats

    try:
        global tr_config

        #maxres = int(tr_config['maxres'])          # Get max resolution
        formats = []
        tr_cmd = "yt-dlp.exe -F " + trailer + " > output.txt"
        fetch_result = subprocess.call(tr_cmd, shell=True)

        if fetch_result == 0:
            fileh = open("output.txt")             # open formats file
            data = fileh.readlines()            
            for x in range(6, len(data)):
                if 'imdb' in imdbtitle:
                    formats.append(data[x][:5].strip())    # List of available formats
                elif data[x][13:14] == ' ' :               # New format
                    formats.append(data[x][:14].strip())   # List of available formats
                else:                                      # Old format
                    formats.append(data[x][:7].strip())    # List of available formats
            fileh.close()  
            return formats
        else:
            return 'Error'

    except Exception as e:
        print (e)
        mgenlog = "There was a problem getting the trailer formats: " + trailer
        print(mgenlog)
        genLog(mgenlog) 


def getDuration(trailerfile, checktr=''):         # Get trailer duration from ffmpeg

    try:

        global tr_config
        maxdur = int(tr_config['maxdur'])         # Get maximum duration to keep

        if '&' in trailerfile:                    # Invalid name for ffpmeg processing
            mgenlog = 'Trailer file name bad name: ' + trailerfile
            genLog(mgenlog)
            print(mgenlog)
            return (1,1,1)
        dur_cmd = "ffmpeg -i " + trailerfile + " > output1.txt 2>&1"
        fetch_result = subprocess.call(dur_cmd, shell=True)
        #print('Fetch result is: ' + str(fetch_result) + ' - ' + trailerfile)
        fileh = open("output1.txt", encoding='utf-8', errors='ignore') # open ffmpeg output file
        data = fileh.readlines()                   # Read file into data
        fileh.close()      
        found = 0
        trfps_text = '0'
        for x in range(len(data)): 
            fpos = data[x].find('Duration')
            rpos = data[x].find('Video')
            if fpos > 0 and found == 0:            # Found duration
                dur_text = data[x][fpos+10:fpos+19] + '00'
                #print(str(dur_text))
                found += 1
                duration = getSeconds(dur_text)    # Convert to seconds
            if rpos > 0 and found == 1:                
                dataa = data[x].split('x')
                if '.mp4' in trailerfile:
                    vres_text = dataa[2][:4].strip(',').strip()
                    hres_text = dataa[1][len(dataa[1])-4:len(dataa[1])].strip()
                elif '.mkv' in trailerfile:
                    vres_text = dataa[1][:4].strip(',').strip()
                    hres_text = dataa[0][len(dataa[0])-4:len(dataa[0])].strip()
                found += 1       
                #print(hres_text + ' ' + vres_text + ' ' + trailerfile)
                fpspos = data[x].rfind('fps')      # Find fps
                if fpspos > 0:
                    trfps_text = data[x][fpspos-6:fpspos-1].strip()
                    if 's' in trfps_text:         # Whole number frame rate
                       tempfps = trfps_text.split(' ')[1].strip()
                       trfps_text = tempfps
                    if trfps_text == '23.98':     # Adjust for You Tube format rounding
                        trfps_text = '23.976'
                    #print('The frame rate is: ' + trfps_text)
                if int(vres_text) > 720 or int(hres_text) > 1280:
                    vres_text = 1080
                elif  int(vres_text) > 480 or int(hres_text) > 720:
                    vres_text = 720
                elif  int(vres_text) > 360 or int(hres_text) > 480:
                    vres_text = 480
                else:
                    vres_text = 360
            #print('Length of file is: ' + str(len(data)) + ' ' + str(x) + ' ' + str(rpos) + ' ' + str(fpos) + ' ' + trailerfile)
        if trfps_text != '0' and maxdur > duration:    # Check for frame rate and audio adjustments
            trfps_text = convertTrailer(trailerfile, trfps_text, checktr)             

        if found == 0: 
            duration = 0
            hres_text = '0'
            vres_text = '0'
            trfps_text = '0'
        elif found == 1:
            hres_text = '0'
            vres_text = '0'
            trfps_text = '0'        
        return (int(hres_text), int(vres_text), duration, trfps_text)
        #print(str(duration))

    except Exception as e:
        print (e)
        mgenlog = 'There was a problem calculating the duration for: ' + trailerfile
        genLog(mgenlog)
        print(mgenlog)
        return (0,0,0)


def convertTrailer(trailerfile, trfps, checktr=''):  # Adjust frame rate and audio level, if needed

    try:
        if 'check' in checktr.lower() or not os.path.isfile(trailerfile): # Check or trailer deleted
            return trfps           
        global tr_config
        trfrate = tr_config['trfrate']
        trback = tr_config['trback']
        ltrailerloc = tr_config['ltrailerloc']
        audiolvl = tr_config['audiolvl']        
        hwenc = tr_config['hwenc']

        if trfrate == '0' and audiolvl == '100':                            # Frame rate and audio changes disabled
            return trfps
        elif (trfrate == trfps) and audiolvl == '100':                      # No changes needed
            mgenlog = "No adjustments needed for: " + trailerfile
            genLog(mgenlog)
            print(mgenlog)
            return trfps       
        elif (trfrate != '0' and trfrate != trfps) or audiolvl == '100':    # Adjust frame rate only
            #print('Frame rate mismatch for: ' + trfrate + ' ' + trfps + ' ' + trailerfile)
            if 'yes' in trback.lower():
                backuploc = os.path.join(ltrailerloc, "backup")
                command = "copy " + trailerfile + " " + backuploc + " >nul 2>nul"
                os.system(command)                  # Rename trailer file to trimmed newname                
                mgenlog = 'Backup trailer successful: ' + trailerfile
                genLog(mgenlog)
                print(mgenlog)

            if hwenc.lower() in ['nevc']:                                   # nVidia HW encoding
                frcommand = "ffmpeg -i " + trailerfile + " -c:v h264_nvenc -filter:v fps=" + trfrate + " -y converted.mp4 >nul 2>nul"
                genLog(frcommand)
                os.system(frcommand)
                filestat = os.stat('./converted.mp4')
                fsize = filestat.st_size            # Get trailer size in bytes
                #print('File size is: ' + str(fsize))
                if fsize == 0:                      # Check for successful conversion
                    mgenlog = "A problem occurred using HW acceleration.  Attempting software only: " + trailerfile
                    genLog(mgenlog)
                    print(mgenlog) 
                    #command = 'del converted.mp4 /q >nul 2>nul'            #  Remove old converted files
                    #os.system(command)                                     #  Clear converted files 
                    frcommand = "ffmpeg -i " + trailerfile + " -filter:v fps=" + trfrate + " -y converted.mp4 >nul 2>nul"
                    genLog(frcommand)
                    os.system(frcommand)                   
            else:
                frcommand = "ffmpeg -i " + trailerfile + " -filter:v fps=" + trfrate + " -y converted.mp4 >nul 2>nul"
                genLog(frcommand)
                os.system(frcommand)        
            #print(frcommand)
            if not os.path.isfile('./converted.mp4'):                      # Check for successful conversion
                mgenlog = "A problem occurred converting trailer file: " + trailerfile
            else:  
                mgenlog = "Ajusted frame rate to " + trfrate + " for: " + trailerfile

        elif trfrate != '0' and trfrate != trfps and audiolvl != '100':    # Adjust frame rate and audio
            if 'yes' in trback.lower():
                backuploc = os.path.join(ltrailerloc, "backup")
                command = "copy " + trailerfile + " " + backuploc + " >nul 2>nul"
                os.system(command)                  # Rename trailer file to trimmed newname                
                mgenlog = 'Backup trailer successful: ' + trailerfile
                genLog(mgenlog)
                print(mgenlog)
            volvl = str(float(audiolvl)/100)
            if hwenc.lower() in ['nevc']:                                   # nVidia HW encoding
                frcommand = "ffmpeg -i " + trailerfile + " -c:v h264_nvenc -filter:v fps=" + trfrate +    \
                "-filter:a volume=" + volvl + " -y converted.mp4 >nul 2>nul"
                genLog(frcommand)
                os.system(frcommand)         
                filestat = os.stat('./converted.mp4')
                fsize = filestat.st_size            # Get trailer size in bytes
                #print('File size is: ' + str(fsize))
                if fsize == 0:                      # Check for successful conversion
                    mgenlog = "A problem occurred using HW acceleration.  Attempting software only: " + trailerfile
                    genLog(mgenlog)
                    print(mgenlog)  
                    frcommand = "ffmpeg -i " + trailerfile + " -filter:v fps=" + trfrate + "-filter:a volume=" + volvl \
                    + " -y converted.mp4 >nul 2>nul"
                    genLog(frcommand)
                    os.system(frcommand)        
            else:
                frcommand = "ffmpeg -i " + trailerfile + " -filter:v fps=" + trfrate + "-filter:a volume=" + volvl \
                + " -y converted.mp4 >nul 2>nul"
                genLog(frcommand)
                os.system(frcommand)        
            #print(frcommand)
            if not os.path.isfile('./converted.mp4'):                      # Check for successful conversion
                mgenlog = "A problem occurred converting trailer file: " + trailerfile
            else:  
                mgenlog = "Ajusted frame rate and audio to " + trfrate + ":" + audiolvl + " for: " + trailerfile

        elif (trfrate == '0' or trfrate == trfps) and audiolvl != '100':    # Adjust audio only
            if 'yes' in trback.lower():
                backuploc = os.path.join(ltrailerloc, "backup")
                command = "copy " + trailerfile + " " + backuploc + " >nul 2>nul"
                os.system(command)                  # Rename trailer file to trimmed newname                
                mgenlog = 'Backup trailer successful: ' + trailerfile
                genLog(mgenlog)
                print(mgenlog)
            volvl = str(float(audiolvl)/100)
            if hwenc.lower() in ['nevc']:                                   # nVidia HW encoding
                frcommand = "ffmpeg -i " + trailerfile +  " -c:v h264_nvenc -filter:a volume=" \
                + volvl + " -y converted.mp4 >nul 2>nul"
                genLog(frcommand)
                os.system(frcommand)        
                filestat = os.stat('./converted.mp4')
                fsize = filestat.st_size            # Get trailer size in bytes
                #print('File size is: ' + str(fsize))
                if fsize == 0:                      # Check for successful conversion
                    mgenlog = "A problem occurred using HW acceleration.  Attempting software only: " + trailerfile
                    genLog(mgenlog)
                    print(mgenlog)  
                    frcommand = "ffmpeg -i " + trailerfile +  " -filter:a volume=" + volvl \
                    + " -y converted.mp4 >nul 2>nul"
                    genLog(frcommand)
                    os.system(frcommand)        
            else:
                frcommand = "ffmpeg -i " + trailerfile +  " -filter:a volume=" + volvl \
                + " -y converted.mp4 >nul 2>nul"
                genLog(frcommand)
                os.system(frcommand)        
            #print(frcommand)
            if not os.path.isfile('./converted.mp4'):                      # Check for successful conversion
                mgenlog = "A problem occurred converting trailer file: " + trailerfile
            else:
                filestat = os.stat('./converted.mp4')
                fsize = filestat.st_size                                   # Get trailer size in bytes
                if fsize > 0:  
                    mgenlog = "Ajusted audio volume to " + audiolvl + " for: " + trailerfile
                else:
                    mgenlog = "A problem occurred converting trailer file: " + trailerfile
        genLog(mgenlog)
        print(mgenlog)
        #genLog(frcommand)
        #os.system(frcommand)
        if ltrailerloc not in trailerfile:
            copytrailer = os.path.join(ltrailerloc, trailerfile)
        else:
            copytrailer = trailerfile
        mvcommand =  "copy converted.mp4 " + copytrailer + " /y >nul 2>nul"  
        genLog(mvcommand)
        os.system(mvcommand)

        command = 'del *.mp4 /q >nul 2>nul'          #  Remove old converted files
        os.system(command)                           #  Clear converted files
        return trfrate

    except Exception as e:
        print (e)
        mgenlog = "There was a problem converting the trailer: " + trailerurl
        print(mgenlog)
        genLog(mgenlog) 


def adjustTrailer(sysarg1 = '', sysarg2 = '', sysarg3 = '', sysarg4 = ''):   # User adjusting of trailers

    try:
        if sysarg1.lower() not in 'adjust':
            return
        if len(sysarg2.lower()) > 0 and sysarg2.lower() not in ['number', 'frame', 'format']:
            print('\nThe valid trailer adjust options are:  number, frame and format\n')
            return

        global tr_config
        trfrate = tr_config['trfrate']
        trback = tr_config['trback']
        ltrailerloc = tr_config['ltrailerloc']
        mtrailerloc = tr_config['mtrailerloc']
        tformat = tr_config['tformat']

        if sysarg2.lower() == 'frame' and len(sysarg3) > 0:        
            db = openTrailerDB()
            frmatch = sysarg3.strip() 
            dbcurr = db.execute('SELECT * from mTrailers WHERE var1 = ? LIMIT 200', (frmatch,))   # Get movie list to check trailers
            dbtuples = dbcurr.fetchall()
            print('Number of trailers found: ' + str(len(dbtuples)))
            db.close()

            if len(dbtuples) == 0:
                mgenlog = 'There were no trailers with the frame rate of ' + sysarg3 + ' to adjust'
                genLog(mgenlog)  
                print(mgenlog)
            else:
                mgenlog = 'Found ' + str(len(dbtuples)) + ' trailers with the frame rate of ' + sysarg3 + ' to adjust'
                genLog(mgenlog)
                print(mgenlog)
 
        if sysarg2.lower() == 'number' and len(sysarg3) > 0:  
            stamatch = sysarg3.strip()
            fmatch = '%' + mtrailerloc + '%'
            db = openTrailerDB()
            if len(sysarg3) > 0 and len(sysarg4) == 0:  # Query is for single movie
                dbcurr = db.execute('SELECT * from mTrailers WHERE extras_FileID = ? AND extras_File LIKE ? \
                ORDER BY extras_FileID LIMIT 50', (stamatch, fmatch,))     # Get movie trailer list to adjust
            elif len(sysarg3) > 0 and len(sysarg4) > 0:
                stomatch = sysarg4.strip()
                dbcurr = db.execute('SELECT * from mTrailers WHERE extras_FileID >= ? and extras_FileID <= ? \
                AND extras_File LIKE ? ORDER BY extras_FileID LIMIT 50', (stamatch, stomatch, fmatch,))   # Get movie list
            dbtuples = dbcurr.fetchall()
            print('Number of trailers found: ' + str(len(dbtuples)))
            db.close()       

            if len(dbtuples) == 0:
                mgenlog = 'There were no trailers with movie number(s) ' + sysarg3 + ' to adjust'
                genLog(mgenlog)  
                print(mgenlog)
            else:
                mgenlog = 'Found ' + str(len(dbtuples)) + ' trailers with requested movie(s) numbers to adjust'
                genLog(mgenlog)
                print(mgenlog)

        if sysarg2.lower() in ['frame', 'number']:
            for x in range(len(dbtuples)):
                #print('Trailerfile is: ' +  dbtuples[x][6])
                curr_tr = dbtuples[x][6]
                rpos = curr_tr.rfind('\\')
                new_tr = ltrailerloc + curr_tr[rpos+1:]
                frame_upd = getDuration(new_tr, 'adjust')
                db = openTrailerDB()                
                db.execute('UPDATE mTrailers SET var1=? WHERE extras_File=?', (frame_upd[3], curr_tr,))
                db.commit()
                db.close()
            return   

        if sysarg2.lower() == 'format' and len(sysarg3) > 0:                # Bulk output format adjustments
            if sysarg3.isdigit() and (int(sysarg3) <= 200 or sysarg4.lower() in ['number']):
                adjcount = int(sysarg3)
            elif sysarg3.isdigit() and int(sysarg3) > 200:
                adjcount = 200
            else:
                adjcount = 1
        elif sysarg2.lower() == 'format':                                   # No number given.  Default to 1
            adjcount = 1

        if 'mp4' in tformat:
            target1 = '.mkv'
            target = '%' + target1
        else:
            target1 = '.mp4'
            target = '%' + target1          

        db = openTrailerDB()

        if sysarg4.lower() in ['number']:                                   # Adjust format for specific movie
            tempcurr = db.execute('SELECT extras_File FROM mTrailers WHERE extras_File LIKE ? and     \
            extras_FileID = ? ORDER BY extras_File ASC', (target, sysarg3,))
            temptuple = tempcurr.fetchall()
        else:                                                               # Or bulk adjust
            tempcurr = db.execute('SELECT extras_File FROM mTrailers WHERE extras_File LIKE ? ORDER BY \
            dateAdded DESC LIMIT ?', (target, adjcount))
            temptuple = tempcurr.fetchall()
        #print(str(temptuple)) 
        
        if len(temptuple) == 0:
            mgenlog = "No trailers found needing output format adjustments. "
            print(mgenlog)
            genLog(mgenlog)
            return

        for a in range(len(temptuple)):          # Insert trailers to convert into temp table
            db.execute('INSERT into mTemp(extras_fileNew) values (?)', (temptuple[a][0],))  
        
        db.commit()

        checkFormats(db, sysarg1, sysarg2)
        db.close()    


    except Exception as e:
        print (e)
        mgenlog = "There was a problem adjusting the trailer: " + sysarg2 + ' ' + sysarg3
        print(mgenlog)
        genLog(mgenlog)


def getTMDBtrailers(tmdb_id):                      # Get list of TMDB trailers

    try:
        print('Getting TMDB trailer list.')
        b64key = 'YTY4OTg3OTI5OTUwNDI4OTYyNTY1ODUwODJkYjA4NDI='
        details_url = movie_url.format(tmdb_id)

        hencoded = urllib.parse.urlencode(headers)
        tmdb_key = base64.b64decode(b64key)

        parms = {'api_key': tmdb_key,              #  TMDB URL Parms
                'language': 'en-US',
                'accept': 'application/json',
                'adult': False,                    
                'append_to_response': 'trailers',
                }  

        queryInfo = urllib.parse.urlencode(parms)
        reqnew = urllib.parse.quote(details_url, safe=':/?')
        request = reqnew + queryInfo

        #print(request)

        req = urllib.request.Request(request, headers=headers)
        jresponse = urllib.request.urlopen(req)

        mdata = json.load(jresponse)
        trailerlist = []

        if 'trailers' in mdata.keys():
            videos = mdata.get('trailers')
            trailers = videos.get('youtube')

            for trailer in trailers:
                if trailer['type'] == 'Trailer':
                    trailerlist.append('https://www.youtube.com/watch?v=' + trailer['source'])
                    #print('https://www.youtube.com/watch?v=' + trailer['source'])
        #print(str(trailerlist))
        return trailerlist

    except Exception as e:
        print (e)
        mgenlog = "There was a getting the TMDB trailer list: " + tmdb_id 
        print(mgenlog)
        genLog(mgenlog) 
        return trailerlist         


def getSeconds(dur_text):                          # Convert time string to secs

    try:
        x = time.strptime(dur_text.split(',')[0],'%H:%M:%S.00')
        td = timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec)
        seconds = int((td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6)
        if seconds == None:
            seconds = 0
        return seconds

    except Exception as e:
        print (e)
        mgenlog = "There was a problem calculating seconds: " + str(dur_text)
        print(mgenlog)
        genLog(mgenlog) 


def checkFolders():                                # Check folders and files

    try:
        global tr_config
        trailerloc = tr_config['ltrailerloc']
        mdbfile = tr_config['dbfile']
        trback = tr_config['trback']
        if not os.path.exists('temp'):             #  Check temp files location
            os.makedirs('temp')
        command = 'del temp\*.mp4 >nul 2>nul'      #  Delete temp files if exist 
        os.system(command)                         #  Clear temp files
        if not os.path.exists('backups'):          #  Check backup files location
            os.makedirs('backups')
        command = 'del *.mp4 >nul 2>nul'           #  Remove old converted files
        os.system(command)                         #  Clear converted files
        if not os.path.exists(trailerloc):         #  Check trailer files location
            mgenlog = 'Local trailer file location does not exist.  Mezzmo Trailer Checker exiting.'  
            genLog(mgenlog)
            print(mgenlog)            
            sys.exit()
        if 'yes' in trback.lower():                
            backuploc = os.path.join(trailerloc, "backup")
            if not os.path.exists(backuploc):      #  Check trailer backup files location
                os.makedirs(backuploc)
                mgenlog = 'Trailer backup file location did not exist.  Backup folder created.'  
                genLog(mgenlog)
                print(mgenlog) 
        if not os.path.isfile(mdbfile):
            mgenlog = 'Mezzmo DB file not found: ' + mdbfile + '.  Please check the config.txt file. '
            genLog(mgenlog)
            print(mgenlog)            
            mgenlog = 'Mezzmo Trailer Checker exiting.'
            genLog(mgenlog)
            print(mgenlog)  
            sys.exit()
        if not os.path.isfile('./ffmpeg.exe'):
            mgenlog = 'ffmpeg.exe not found in Mezzmo Trailer Checker folder.  Mezzmo Trailer Checker exiting.'
            genLog(mgenlog)
            print(mgenlog)            
            sys.exit()
        if not os.path.isfile('./yt-dlp.exe'):
            mgenlog = 'ytp-dl.exe not found in Mezzmo Trailer Checker folder.  Mezzmo Trailer Checker exiting.'
            genLog(mgenlog)
            print(mgenlog)            
            sys.exit()
  

    except Exception as e:
        #print (e)
        mgenlog = 'There was a problem checking folders ' + str(e)
        genLog(mgenlog)
        print(mgenlog)    


def checkFiles(sysarg1 = '', sysarg2 = '', ccount = 0): # Check size, resolution and duration for trailers

    try:
        if sysarg1.lower() not in 'check':
            return
        elif len(sysarg2.lower()) > 0 and sysarg2.lower() not in ['new']:
            print('\nThe valid media check option is:  new\n')
            return

        global tr_config
        trailerloc = tr_config['ltrailerloc']         # Get locatal path to trailer lcoation
        maxcheck = tr_config['maxcheck']              # Number of movies to check
        if ccount > 0:
            maxcheck = ccount
   
        db = openTrailerDB()

        if 'new' in sysarg2.lower():
            dbcurr = db.execute('SELECT extras_File from mTrailers WHERE extras_File NOT LIKE ?    \
            ORDER BY lastchecked ASC LIMIT ?', ('%www.youtube%', maxcheck,))
        else: 
            dbcurr = db.execute('SELECT extras_File from mTrailers WHERE extras_File NOT LIKE ?    \
            AND (trDuration=? or trDuration is NULL or tr_resol is NULL or tr_size=? OR tr_size is \
            NULL) ORDER BY extras_FileID, extras_File LIMIT ?', ('%www.youtube%', 0, 0, maxcheck,))      
        dbtuple = dbcurr.fetchall()                   # Get entries with missing info

        if len(dbtuple) == 0:                         # All files updated
            mgenlog = 'There were no trailers found which need checking.'
            genLog(mgenlog)
            print(mgenlog)
            db.close 
            return

        #print('Length of tuples is: ' + str(len(dbtuple)) + ' ' + str(maxcheck)) 
        #print(str(dbtuple)) 

        checkcount = 0
        if ccount == 0:                              # Display start message if not called by checkFinish
            mgenlog = 'Checking trailer files beginning.'
            genLog(mgenlog)
            print(mgenlog)
        for fname in range(len(dbtuple)):
            lpos = dbtuple[fname][0].rfind('\\')     # Slice file name 
            fpart = dbtuple[fname][0][lpos+1:]       # Get file name portion
            newname = trailerloc + fpart             # Local path to trailer file
            currTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            target = '%' + fpart                     # Find trailer by like name 
            if os.path.isfile(newname ):             # Verify trailerfile exists
                # print('File name is: ' +  newname)
                fdur = getDuration(newname, 'check')
                filestat = os.stat(newname)
                fsize = filestat.st_size             # Get trailer size in bytes
                #print(str(fdur[1]) + ' ' + str(fdur[2]) + ' ' + str(fsize) + ' ' + newname)
                if fdur[0] == 1 and fdur[1] == 1 and fdur[2] == 1:
                    db.execute('UPDATE mTrailers SET lastchecked=?, tr_resol=?, tr_size=?, trStatus=?,     \
                    trDuration=? WHERE extras_File LIKE ?', (currTime, fdur[1], fsize, 'Invalid', fdur[2], \
                    target,))
                else:
                    db.execute('UPDATE mTrailers SET lastchecked=?, tr_resol=?, tr_size=?, trStatus=?, \
                    trDuration=?, var1=? WHERE extras_File LIKE ?', (currTime, fdur[1], fsize, 'Yes',  \
                    fdur[2], fdur[3], target,))
            else:
                db.execute('UPDATE mTrailers SET lastchecked=?, tr_resol=?, tr_size=?, trStatus=?,     \
                trDuration=? WHERE extras_File LIKE ?', (currTime, 2, 2, 'Missing', 2, target,))
                mgenlog = 'Trailer file not found for duration checking: ' + newname
                genLog(mgenlog)
            checkcount += 1
            if checkcount % 100 == 0:
                print('Files checked: ' + str(checkcount))
            if checkcount % 500 == 0:
                db.commit()             
        db.commit()
        db.close()
        if ccount == 0:                               # Display ending message if not called by checkFinish
            mgenlog = 'Checking trailer files completed. ' + str(checkcount) + ' files checked'  
            genLog(mgenlog)
            print(mgenlog)

        return

    except Exception as e:
        #print (e)
        mgenlog = "There was a problem checking files: " + str(e)
        print(mgenlog)
        genLog(mgenlog) 


def renameFiles(imdbtitle = ''):                    # Rename trailer file names / move to temp folder

        global tr_config
        maxdur = int(tr_config['maxdur'])           # Get maximum duration to keep
        ytube = tr_config['ytube']                  # Get You Tube prepend option
        listOfFiles = os.listdir('.')
        pattern = "*.mp4"
        for x in listOfFiles:
            if fnmatch.fnmatch(x, pattern):
                #print (x)
                filestat = os.stat(x)
                fsize = filestat.st_size            # Get trailer size in bytes
                rpos = x.find('[')
                newname = x[:rpos - 1]
                # Remove file name characters which cannot be reencoded
                newname = newname.replace(' ' ,'_')
                imdbtitle = imdbtitle.replace(' ' ,'_').replace(',' ,'_')
                newname = re.sub(r'[^\x61-\x7a,\x5f,^\x41-\x5a,^\x30-\x39]',r'', newname) 
                imdbtitle = re.sub(r'[^\x61-\x7a,\x5f,^\x41-\x5a,^\x30-\x39]',r'', imdbtitle)  
                if rpos > 1 and len(imdbtitle) > 0 and 'imdb' in imdbtitle:     # Trim extra characters
                    #tempname = ''.join(random.choices(string.ascii_letters, k=6))
                    if ytube.lower() in 'yes':                                  # Prepend ytube_ to trailer
                        newname = imdbtitle[:40] + "_" + newname[:rpos - 1]  + ".mp4"
                    else:
                        newname = imdbtitle + "_" + newname[:rpos - 1] + "_" + tempname + ".mp4"
                elif rpos >= 10:                    # Trim extra characters
                    if ytube.lower() in 'yes':                                  # Prepend ytube_ to trailer
                        newname = "ytube_" + newname[:rpos - 1]  + ".mp4"
                    else:
                        newname = newname[:rpos - 1]  + ".mp4"
                elif len(newname) < 10:
                    tempname = ''.join(random.choices(string.ascii_letters, k=12))
                    if ytube.lower() in 'yes':                                  # Prepend ytube_ to trailer
                        newname = "ytube_trailer_" + tempname + ".mp4"
                    else:
                        newname = "trailer_" + tempname + ".mp4"
                else:
                    newname = "ytube_" + newname  + ".mp4"
                checkname = 'temp\\' + newname
                dupe = checkDupe(newname)           # Check dupe in db
                if os.path.isfile(checkname) or dupe > 0: # Ensure local trailer name is not a dupe
                    dupename = newname[:len(newname)-4]
                    appname = ''.join(random.choices(string.ascii_letters, k=3))
                    newname = dupename + '_' + appname + '.mp4'
                    mgenlog = 'Duplicate trailer name found. Trailer name appended: ' + newname
                    genLog(mgenlog)
                    print(mgenlog) 
                command = "rename " + '"' + x + '" "' + newname + '"'
                os.system(command)                  # Rename trailer file to trimmed newname
                hres, vres, duration, trfpos = getDuration(newname)
                if duration > maxdur:               # Do not keep trailer if too long
                    command = "del " + '"' + newname + '"'
                    mgenlog = 'Trailer not kept - Too long: ' + str(duration) + 's - ' + newname
                    genLog(mgenlog)
                    print(mgenlog) 
                else:
                    command = "move " + '"' + newname + '" temp >nul 2>nul'
                os.system(command)                  # Move to temp folder till done fetching all
                return [newname, str(fsize), duration]   # Return new trailer name and info


def checkDupe(newname):                             # Check duplicate name already in trauiler database

    try:
        db = openTrailerDB()
        target = '%' + newname
        curd = db.execute('SELECT count (*) FROM mTrailers WHERE extras_File LIKE ?', (target,))        
        curtuple = curd.fetchone()
        trcount = int(curtuple[0])
        curd = db.execute('SELECT count (*) FROM mTemp WHERE extras_FileNew LIKE ?', (target,))        
        curtuple = curd.fetchone()
        tmcount = int(curtuple[0])
        totcount = trcount + tmcount
        db.close()
        return totcount

    except Exception as e:
        print (e)
        mgenlog = "There was a problem checking for duplicate trailers : " + newname
        print(mgenlog)
        genLog(mgenlog) 


def moveTrailers():                                 # Move trailers to trailer location

    try:
        global tr_config
        trailerloc = tr_config['ltrailerloc']       # Get locatal path to trailer lcoation

        command = "move temp\*.mp4 " + trailerloc + " >nul 2>nul"
        #print(command)
        os.system(command)
    except Exception as e:
        #print (e)
        mgenlog = 'There was a problem moving trailers to the trailer folder. ' + str(e)
        genLog(mgenlog)
        print(mgenlog)


def checkUpdate(sysarg1):                          # Check for yt-dlp.exe update

    try:
        if len(sysarg1) > 1 and sysarg1.lower() not in ['trailer', 'update']:
            return

        currDate = datetime.now().strftime('%Y-%m-%d')

        db = openTrailerDB()
        curd = db.execute('SELECT count (*) FROM mChecked WHERE last_checked = ?', (currDate,))        
        curtuple = curd.fetchone()
        
        if curtuple[0] == 0 or sysarg1.lower() == 'update':  
            command = "yt-dlp.exe -U >nul 2>nul"
            #print(command)
            os.system(command)
            if curtuple[0] == 0:
                mgenlog = 'Daily check for yt-dlp.exe update completed.'
            else:
                mgenlog = 'Forced check for yt-dlp.exe update completed.'
            genLog(mgenlog)
            print(mgenlog)
            db.execute('DELETE FROM mCHecked')
            db.commit()
            db.execute('INSERT into mChecked(last_checked) values (?)', (currDate,))
            db.commit()
        else:
            mgenlog = 'Daily check for yt-dlp.exe already completed today.'
            genLog(mgenlog)
            print(mgenlog)
        db.close()


    except Exception as e:
        #print (e)
        mgenlog = 'There was a problem checking for a yt-dlp.exe update. ' + str(e)
        genLog(mgenlog)
        print(mgenlog)
        sys.exit()


def checkCsv(sysarg1 = '', sysarg2 = ''):           # Generate CSV files

        if len(sysarg1) == 0 or sysarg1.lower() not in 'csv':
            return
        elif sysarg2.lower() not in ['trailer', 'history', 'notrail']:
            print('\nThe valid csv options are:  trailer, history or notrail\n')
            return

        if sys.version_info[0] < 3:
            print('The CSV export utility requires Python version 3 or higher')
            exit()    
        mgenlog = 'CSV file export beginning for - ' + sysarg1
        genLog(mgenlog)
            
        db = openTrailerDB()
        fpart = datetime.now().strftime('%H%M%S')
        if sysarg2.lower() == 'trailer':
            curm = db.execute('SELECT * FROM mTrailers ORDER BY extras_FileID')
            filename = 'meztrailers_' + fpart + '.csv'
        elif sysarg2.lower() == 'history':
            curm = db.execute('SELECT * FROM mHistory')
            filename = 'mezhistory_' + fpart + '.csv'
        elif sysarg2.lower() == 'notrail':
            print('Beginning no trailer report generation')
            noTrailer()                                # Update Temp table for no trailer analysis
            curm = db.execute('select extras_FileID, mgofile_title, mgofile_file FROM \
            mTemp WHERE extras_FileID NOT IN (SELECT extras_FileID FROM mTrailers)    \
            ORDER BY extras_FileID')
            filename = 'meznotrail_' + fpart + '.csv'            

        headers = [i[0] for i in curm.description]      
        recs = curm.fetchall()
        writeCSV(filename, headers, recs)
        del curm
        db.close()
        mgenlog = 'CSV file export completed to - ' + filename
        genLog(mgenlog)
        print(mgenlog)


def writeCSV(filename, headers, recs):

    try:
        csvFile = csv.writer(open(filename, 'w', encoding = 'utf-8'),
                         delimiter=',', lineterminator='\n',
                         quoting=csv.QUOTE_ALL)
        csvFile.writerow(headers)     # Add the headers and data to the CSV file.
        for row in recs:
            recsencode = []
            for item in range(len(row)):
                if isinstance(row[item], int) or isinstance(row[item], float):  # Convert to strings
                    recitem = str(row[item])
                else:
                    recitem = row[item]
                recsencode.append(recitem) 
            csvFile.writerow(recsencode)               

    except Exception as e:
        #print (e)
        mgenlog = 'An error occurred creating the CSV file. ' + str(e)
        genLog(mgenlog)
        pring(mgenlog)


def checkFinish(sysarg1, sysarg2):                           # Successfully finished

    if sysarg1.lower() in ['trailer']:                       # Sync trailer db to Mezzmo
        getMezzmoTrailers('sync')
        checkFiles('check', '', gdcount)
        cleanSkip()                                          # Clean skipped trailers
    checkLogfile()                                           # Trim logfile to 10k lines       
    mgenlog = 'Mezzmo Trailer Checker completed successfully.'
    print(mgenlog)
    genLog(mgenlog)
    if sysarg1.lower() in ['trailer', 'stats']:   
        displayStats(sysarg1, sysarg2)


def cleanSkip():                                             # Clean skipped non-trailer files

        global tr_config

        if tr_config['cleanskp'].lower()  != 'yes':
            return

        mgenlog = 'Checking for skipped non-trailer files enabled.'
        print(mgenlog)
        genLog(mgenlog)

        db = openTrailerDB()
        dbcurr = db.execute('SELECT count (*) from mTrailers WHERE trStatus LIKE ? ', ('%Skip%',))
        showtuples = dbcurr.fetchone()

        if showtuples[0] > 0:
            mgenlog = 'Non-trailer files found in trailer DB: ' + str(showtuples[0])
            print(mgenlog)
            genLog(mgenlog)
            db.execute('DELETE from mTrailers WHERE trStatus LIKE ?', ('%Skip%',))
            db.commit()
            mgenlog = 'Non-trailer file database cleaning completed.'
            print(mgenlog)
            genLog(mgenlog)
        else:
            mgenlog = 'No Non-trailer files found in trailer DB.  Skipping cleaning.'
            print(mgenlog)
            genLog(mgenlog)
        db.close()


def getTotals():                                             # Gets checked download totals

    try:
        db = openTrailerDB()
        currDate = datetime.now().strftime('%Y-%m-%d')
        dateMatch = currDate + '%'
        dqcurr = db.execute('SELECT count (*) from mHistory WHERE lastchecked LIKE ?', (dateMatch,))
        daytuple = dqcurr.fetchone()
        dqcurr = db.execute('SELECT count (*) from mHistory')
        htottuple = dqcurr.fetchone()
        db.close()
        return [daytuple[0], htottuple[0]]

    except Exception as e:
        #print (e)
        mgenlog = 'An error occurred generating totals. ' + str(e)
        genLog(mgenlog)
        print(mgenlog)


def showErrors(sysarg1= '', sysarg2= ''):                     # Show movies with bad statuses

    try:
        if sysarg1.lower() not in ['show']:                   # Must be a valid command
            return

        if len(sysarg2) > 0:                                  # return for files
            return

        db = openTrailerDB()
        dbcurr = db.execute('SELECT * from mTrailers WHERE trStatus NOT LIKE ? AND trStatus IS \
        NOT NULL ORDER BY extras_FileID, extras_ID', ('%Yes%',))
        showtuples = dbcurr.fetchall()

        if len(showtuples) > 0:
            print('\n\n Movie # \tTrailer # \tStatus \t\t\t    Movie Title \n')
            for show in showtuples:
                print(str(show[4]) + '\t\t' + str(show[3]) + '\t\t' + show[11] + '\t\t' + show[1])
            print('\n\n\n')
            mgenlog = 'There were ' + str(len(showtuples)) + ' displayed with errors'
            genLog(mgenlog)
        else:
            mgenlog = 'There were no movies found with errors'
            genLog(mgenlog)
            print(mgenlog)
        db.close()       


    except Exception as e:
        #print (e)
        mgenlog = 'An error occurred showing bad movies. ' + str(e)
        genLog(mgenlog)
        print(mgenlog)


def makeBackups():                                   # Make database backups

    try:
        from sqlite3 import dbapi2 as sqlite
    except:
        from pysqlite2 import dbapi2 as sqlite
    
    try:
        if len(sysarg1) == 0 or sysarg1.lower() not in 'backup':
            return
        DB = 'backups/mezzmo_trailers_' + datetime.now().strftime('%m%d%Y-%H%M%S') + '_.db'
        dbout = sqlite.connect(DB)
        dbin = openTrailerDB()

        with dbout:
            dbin.backup(dbout, pages=100)
        dbout.close()
        dbin.close()
        mgenlog = 'Mezzmo Trailer Checker backup successful: ' + str(DB)
        genLog(mgenlog)
        print(mgenlog) 

    except Exception as e:
        #print (e)
        mgenlog = 'An error occurred creating a Mezzmo Trailer Checker backup. ' + str(e)
        genLog(mgenlog)
        print(mgenlog)      

                                  
def cleanTrailers(sysarg1 = '', sysarg2 = '', sysarg3 = ''): # Clean show movie trailers from DB


        if sysarg1.lower() not in ['show', 'clean'] or  sysarg2.lower() not in         \
        ['name', 'number', 'files', 'bad', 'long', 'skip', 'missing']: 
            return
        elif sysarg2.lower() in ['name', 'number'] and len(sysarg3) == 0:
           print('A movie name or movie number is required.')

        global tr_config
        ltrailerloc = tr_config['ltrailerloc']       # Get local path to trailer lcoation
        mtrailerloc = tr_config['mtrailerloc']       # Get Mezzmo path to trailer lcoation

        if sysarg2.lower() in 'number':
            db = openTrailerDB()
            dbcurr = db.execute('SELECT * from mTrailers WHERE extras_FileID=? ORDER BY \
            extras_FileID, extras_ID', (sysarg3,))
            dbtuples = dbcurr.fetchall() 
            if len(dbtuples) == 0:
                mgenlog = 'No trailers found with movie number: ' + str(sysarg3)
                genLog(mgenlog)
                print(mgenlog)
                db.close()
                return

        elif sysarg2.lower() in 'name':
            db = openTrailerDB()
            dbcurr = db.execute('SELECT * from mTrailers WHERE mgofile_title=?    \
            ORDER BY mgofile_title, extras_ID', (sysarg3,))
            dbtuples = dbcurr.fetchall()
            if len(dbtuples) == 0:
                mgenlog = 'No trailers found with movie name: ' + str(sysarg3)
                genLog(mgenlog)
                print(mgenlog)
                db.close()
                return

        elif sysarg2.lower() in 'files':
            db = openTrailerDB()
            db.execute('DELETE FROM mTemp')              # Clear temp table before writing
            db.commit()
            listOfFiles = os.listdir(ltrailerloc)
            pattern = "*.mp4"
            for x in listOfFiles:
                if fnmatch.fnmatch(x, pattern):
                    #print(x)
                    insertfile = ltrailerloc + x
                    matchfile = mtrailerloc + x
                    db.execute('INSERT into mTemp(extras_File, mgofile_file) values (?, ?)',  \
                    (insertfile, matchfile,))               
            db.commit()
            listOfFiles = os.listdir(ltrailerloc)
            pattern = "*.mkv"
            for x in listOfFiles:
                if fnmatch.fnmatch(x, pattern):
                    #print(x)
                    insertfile = ltrailerloc + x
                    matchfile = mtrailerloc + x
                    db.execute('INSERT into mTemp(extras_File, mgofile_file) values (?, ?)',  \
                    (insertfile, matchfile,))               
            db.commit()
            dbcurr = db.execute('SELECT extras_file FROM mTemp WHERE mTemp.mgofile_file NOT IN \
            (SELECT extras_file FROM mTrailers)')  
            dbtuples = dbcurr.fetchall()
            if len(dbtuples) == 0:             
                mgenlog = 'No trailer files found without a Mezzmo trailer entry'
                genLog(mgenlog)
                print(mgenlog)
                db.close()
                return

        elif sysarg2.lower() in 'bad':
            db = openTrailerDB()
            dbcurr = db.execute('SELECT * from mTrailers WHERE trStatus=?    \
            ORDER BY mgofile_title, extras_ID', ('Bad',))
            dbtuples = dbcurr.fetchall() 
            if len(dbtuples) == 0:
                mgenlog = 'No trailers found with Bad status'
                genLog(mgenlog)
                print(mgenlog)
                db.close()
                return

        elif sysarg2.lower() in 'long':
            db = openTrailerDB()
            dbcurr = db.execute('SELECT * from mTrailers WHERE trStatus=?    \
            ORDER BY mgofile_title, extras_ID', ('Long',))
            dbtuples = dbcurr.fetchall() 
            if len(dbtuples) == 0:
                mgenlog = 'No trailers found with Long status'
                genLog(mgenlog)
                print(mgenlog)
                db.close()
                return

        elif sysarg2.lower() in 'skip':
            db = openTrailerDB()
            dbcurr = db.execute('SELECT * from mTrailers WHERE trStatus=?    \
            ORDER BY mgofile_title, extras_ID', ('Skip',))
            dbtuples = dbcurr.fetchall() 
            if len(dbtuples) == 0:
                mgenlog = 'No trailers found with Skip status'
                genLog(mgenlog)
                print(mgenlog)
                db.close()
                return

        elif sysarg2.lower() in 'missing':
            db = openTrailerDB()
            dbcurr = db.execute('SELECT * from mTrailers WHERE trStatus=?    \
            ORDER BY mgofile_title, extras_ID', ('Missing',))
            dbtuples = dbcurr.fetchall() 
            if len(dbtuples) == 0:
                mgenlog = 'No trailers found with Missing trailer file status'
                genLog(mgenlog)
                print(mgenlog)
                db.close()
                return

        print('The number of trailers found: ' + str(len(dbtuples)))

        if sysarg2.lower() in ['name', 'number', 'bad', 'long', 'skip', 'missing']:
            print('\n\n Movie #   Trailer # \tStatus\t\tMovie Title    \t\t\t Trailer File\n')
            for trailer in dbtuples:
                status = '   '
                if trailer[11] != None:
                    status = trailer[11]
                print(str(trailer[4]) + '\t\t' + str(trailer[3]) + '\t' + status + '\t' \
                + trailer[1][:36] + '\t' + trailer[6])

        if sysarg2.lower() in ['files']:
            print('\n\n Movie Trailer File\n')
            for trailer in dbtuples:
                print(str(trailer[0]))
            print('\nTotal orphaned trailers found: ' +str(len(dbtuples)))  
        print('\n\n\n')

        if 'clean' in sysarg1.lower() and sysarg2.lower() in ['name', 'number']:  # Do you want to delete ?
            choice = input('Do you want to delete these trailers (Y/N) ?  They will be rebuilt from Mezzmo\n')
            if 'n' in choice.lower():
                mgenlog = 'Trailers will not be cleaned for: ' + str(sysarg3)
                genLog(mgenlog)
                print(mgenlog)                
                db.close()
                return 
        elif 'clean' in sysarg1.lower() and sysarg2.lower() in ['bad', 'long', 'skip', 'missing']:  # Do you want to delete ?
            choice = input('Do you want to delete these trailers (Y/N) ?  They will be removed from the Trailer Checker database\n')
            if 'n' in choice.lower():
                mgenlog = 'Trailers will not be cleaned with status: ' + str(sysarg2)
                genLog(mgenlog)
                print(mgenlog)                
                db.close()
                return 
        elif 'clean' in sysarg1.lower() and sysarg2.lower() in ['files']:  # Do you want to delete ?
            mgenlog = str(len(dbtuples)) + ' - orphaned trailer files found for cleaning'
            genLog(mgenlog)
            choice = input('Do you want to delete these orphaned trailer files from your trailer folder (Y/N) ?  \n')
            if 'n' in choice.lower():
                mgenlog = 'Trailer files will not be deleted'
                genLog(mgenlog)
                print(mgenlog)                
                db.close()
                return 

        if sysarg2.lower() in 'number' and sysarg1.lower() in "clean": 
            db.execute('DELETE from mTrailers WHERE extras_FileID=?', (sysarg3,))
            db.commit()
        elif sysarg2.lower() in 'name' and sysarg1.lower() in "clean":
            dbcurr = db.execute('DELETE from mTrailers WHERE mgofile_title=?', (sysarg3,))
            db.commit()
        elif sysarg2.lower() in 'bad' and sysarg1.lower() in "clean":
            dbcurr = db.execute('DELETE from mTrailers WHERE trStatus=?', ('Bad',))
            db.commit()
        elif sysarg2.lower() in 'long' and sysarg1.lower() in "clean":
            dbcurr = db.execute('DELETE from mTrailers WHERE trStatus=?', ('Long',))
            db.commit()
        elif sysarg2.lower() in 'skip' and sysarg1.lower() in "clean":
            dbcurr = db.execute('DELETE from mTrailers WHERE trStatus=?', ('Skip',))
            db.commit()
        elif sysarg2.lower() in 'missing' and sysarg1.lower() in "clean":
            dbcurr = db.execute('DELETE from mTrailers WHERE trStatus=?', ('Missing',))
            db.commit()
        elif sysarg2.lower() in 'files' and sysarg1.lower() in "clean":
            gcount = bcount = 0

            for a in range(len(dbtuples)):            
                if os.path.isfile(dbtuples[a][0]):
                    os.remove(dbtuples[a][0])
                    gcount += 1
                    mgenlog = 'Orphaned trailer file successfully deleted: ' + dbtuples[a][0]
                    genLog(mgenlog)

            mgenlog = str(gcount) + ' - total orphaned trailer files successfully deleted'
            genLog(mgenlog)
            print('\n\n' + mgenlog + '\n\n')                                
  
        if sysarg1.lower() in "clean" and sysarg2.lower() in ['name', 'number']:        
            mgenlog = 'Trailers successfully cleaned for movie: ' + str(sysarg3)
            genLog(mgenlog)
            print(mgenlog)
        if sysarg1.lower() in "clean" and sysarg2.lower() in ['bad', 'long', 'skip', 'missing']:        
            mgenlog = 'Trailers successfully cleaned with status: ' + str(sysarg2)
            genLog(mgenlog)
            print(mgenlog)
        db.close()        


def displayStats(sysarg1, ssyarg2 = ''):              # Display statistics    

    try:
        global totcount, bdcount, gdcount, mvcount, skipcount, trlcount, longcount, nontrcount
        global tr_config
        trailerloc = tr_config['ltrailerloc']
        mtrailerloc = tr_config['mtrailerloc']
        tronly = tr_config['tronly'].lower()

        print ('\n\n\t ************  Mezzmo Trailer Checker Stats  *************\n')

        daytotal, grandtotal =  getTotals()

        if sysarg1.lower() in ['trailer']:
            print ("Mezzmo movies checked: \t\t\t" + str(totcount))
            print ("Mezzmo movies skipped: \t\t\t" + str(skipcount))
            print ("Mezzmo trailers fetched: \t\t" + str(trlcount))
            print ("Mezzmo trailers bad trailer: \t\t" + str(bdcount))
            print ("Mezzmo trailers too long: \t\t" + str(longcount))
            print ("Mezzmo trailers downloaded: \t\t" + str(gdcount))
            print ("YouTube videos skipped: \t\t" + str(nontrcount))
            print ("\nTrailers fetched today: \t\t" + str(daytotal))
            if tronly == 'yes':
                print ("Trailers fetched total: \t\t" + str(grandtotal))

        elif sysarg1.lower() in ['stats'] and not sysarg2.lower() in ['frame']:
            db = openTrailerDB()
            dqcurr = db.execute('SELECT count (*) from mTrailers')
            totaltuple = dqcurr.fetchone()
            dqcurr = db.execute('SELECT count (*) from mTrailers WHERE extras_File NOT LIKE ?', ('%www.youtube%',))
            localtuple = dqcurr.fetchone()
            target = "%" + mtrailerloc + "imdb%"
            dqcurr = db.execute('SELECT count (*) from mTrailers WHERE extras_File LIKE ?', (target,))
            imdbtuple = dqcurr.fetchone()
            dqcurr = db.execute('SELECT count (*) from mTrailers WHERE extras_File LIKE ?', ('%www.youtube%',))
            youtuple = dqcurr.fetchone()
            dqcurr = db.execute('SELECT count (*) from mTrailers WHERE trstatus LIKE ?', ('%Bad%',))
            badtuple = dqcurr.fetchone()
            dqcurr = db.execute('SELECT count (*) from mTrailers WHERE trstatus LIKE ?', ('%Long%',))
            longtuple = dqcurr.fetchone()
            dqcurr = db.execute('SELECT count (*) from mTrailers WHERE trstatus LIKE ?', ('%Yes%',))
            chktuple = dqcurr.fetchone()
            dqcurr = db.execute('SELECT count (*) from mTrailers WHERE trstatus LIKE ?', ('%Skip%',))
            skptuple = dqcurr.fetchone()
            dqcurr = db.execute('SELECT count (*) from mTrailers WHERE trstatus LIKE ?', ('%Invalid%',))
            invtuple = dqcurr.fetchone()
            dqcurr = db.execute('SELECT count (*) from mTrailers WHERE trstatus LIKE ?', ('%Missing%',))
            mistuple = dqcurr.fetchone()
            dqcurr = db.execute('SELECT count (*) from mTrailers WHERE trstatus IS NULL')
            nulltuple = dqcurr.fetchone()
            dqcurr = db.execute('SELECT count (DISTINCT extras_FileID) from mTrailers')
            movtuple = dqcurr.fetchone()
            dqcurr = db.execute('SELECT count (DISTINCT extras_FileID) from mTrailers WHERE trStatus IS NULL')
            nullmvtuple = dqcurr.fetchone()
            dqcurr = db.execute('SELECT COUNT (DISTINCT extras_FileID) from mTrailers WHERE extras_File LIKE ?',
            (mtrailerloc + "%",))
            localmovie = dqcurr.fetchone()
            dqcurr = db.execute('SELECT count (*) from mTrailers WHERE extras_File LIKE ?', ('%.mp4',))
            mp4format = dqcurr.fetchone()
            dqcurr = db.execute('SELECT count (*) from mTrailers WHERE extras_File LIKE ?', ('%.mkv',))
            mkvformat = dqcurr.fetchone()
            noTrailer()                                # Update Temp table for no trailer analysis
            dqcurr = db.execute('select count(extras_FileID) FROM mTemp WHERE extras_FileID NOT IN     \
            (SELECT extras_FileID FROM mTrailers) ORDER BY extras_FileID')
            notrailer = dqcurr.fetchone()

            db.close()
            foldersize = filecount = bfoldersize = bstoragegb = 0
            for element in os.scandir(trailerloc):
                foldersize+=os.stat(element).st_size
                filecount += 1
            storagegb = round((float(foldersize) / 1073741824),2)
            trbackfolder = os.path.join(trailerloc, 'backup')
            if os.path.exists(trbackfolder):
                for belement in os.scandir(trbackfolder):
                    bfoldersize+=os.stat(belement).st_size            
                bstoragegb = round((float(bfoldersize) / 1073741824),2)
            avgsize = round((float(foldersize) / 1048576 / filecount),2) 
            print ("\nTrailers fetched today: \t\t" + str(daytotal))
            print ("Trailers fetched total: \t\t" + str(grandtotal))
            print ("\nTotal Movies with trailers: \t\t" + str(movtuple[0]))
            print ("Movies with local trailers: \t\t" + str(localmovie[0]))
            print ("Mezzmo movies with no trailers: \t" + str(notrailer[0]))  
            print ("Movies not yet fetched: \t\t" + str(nullmvtuple[0]))
            print ("Movies total trailers: \t\t\t" + str(totaltuple[0]))
            print ("Mezzmo local trailers:  \t\t" + str(localtuple[0]))
            print ("Mezzmo YouTube trailers: \t\t" + str(youtuple[0]))
            print ("Mezzmo IMDB trailers: \t\t\t" + str(imdbtuple[0]))
            print ("Mezzmo bad trailers: \t\t\t" + str(badtuple[0]))
            print ("Mezzmo long trailers: \t\t\t" + str(longtuple[0]))
            print ("YouTube skipped trailers: \t\t" + str(skptuple[0]))
            print ("Mezzmo invalid name trailers: \t\t" + str(invtuple[0]))
            print ("Mezzmo trailer file missing: \t\t" + str(mistuple[0]))
            print ("\nMezzmo local trailers mp4 format: \t" + str(mp4format[0]))
            print ("Mezzmo local trailers mkv format: \t" + str(mkvformat[0]))
            print ("\nLocal trailer files in folder: \t\t" + str(filecount))
            print ("Total size of local trailers: \t\t" + str(storagegb) + 'GB')
            print ("Average trailer file size: \t\t" + str(avgsize) + 'MB')
            if bstoragegb > 0:
                print ("Total size of backup trailers: \t\t" + str(bstoragegb) + 'GB')
            print ("\nMezzmo trailers fetched: \t\t" + str(chktuple[0]))
            print ("Mezzmo trailers not fetched: \t\t" + str(nulltuple[0]))
            print ("\n\n")

        elif sysarg1.lower() in ['stats'] and sysarg2.lower() in ['frame']:
            db = openTrailerDB()
            dqcurr = db.execute('SELECT var1, COUNT(*) counter FROM mTrailers WHERE NOT var1 \
            is NULL GROUP BY var1')
            frametuples = dqcurr.fetchall()
            db.close()

            if len(frametuples) == 0:
                print('There was a problem getting the frame rate statistics')
                return
            else:
                #print('The number of rows is: ' + str(len(frametuples)))
                print('\tFrame')
                print('\tRate\t\tCount\n')        
                for a in range(len(frametuples)):
                    print('\t' + str(frametuples[a][0]) + '\t\t' + str(frametuples[a][1]))


    except Exception as e:
        #print (e)
        mgenlog = "There was a problem displaying statistics  " + str(e)
        print(mgenlog)
        genLog(mgenlog) 


checkCommands(sysarg1, sysarg2)                              # Check for valid commands
getConfig()                                                  # Process config file
checkDatabase()                                              # Check trailer database 
checkUpdate(sysarg1)                                         # Check for new vesion of yt-dlp.exe
checkFolders()                                               # Check trailer and temp folder locations
getMezzmoTrailers(sysarg1)                                   # Load Mezzmo trailers into trailer checker DB
getMovieList(sysarg1, sysarg2, sysarg3)                      # Get list of movies to check and get trailers
checkCsv(sysarg1, sysarg2)
checkFiles(sysarg1, sysarg2)
cleanTrailers(sysarg1, sysarg2, sysarg3)
adjustTrailer(sysarg1, sysarg2, sysarg3, sysarg4)
makeBackups()
checkFinish(sysarg1, sysarg2)
showErrors(sysarg1, sysarg2)
