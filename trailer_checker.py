# -*- coding: utf-8 -*-
# #!/usr/bin/python
import os, fnmatch, sys, csv, json, glob
from datetime import datetime
import urllib.request, urllib.parse, urllib.error
import http.client
import mimetypes
import subprocess
from urllib.request import Request, urlopen

trailerdb = 'mezzmo_trailers.db'
tr_config = {}

version = 'version 0.0.1'

sysarg1 = ''
sysarg2 = ''
if len(sys.argv) == 2:
    sysarg1 = sys.argv[1]
if len(sys.argv) == 3:
    sysarg1 = sys.argv[1]   
    sysarg2 = sys.argv[2]


def getConfig():

    try: 

        global tr_config, version      
        fileh = open("config.txt")                                     # open the config file
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
        if int(mfetchcount) > 20:
            mfetchcount = 20                                           # Max trailer per movie is 20

        data = fileh.readline()                                        # Get number of trailers per movie
        datad = data.split('#')                                        # Remove comments
        trfetchcount = datad[0].strip().rstrip("\n")                   # cleanup unwanted characters
        if int(trfetchcount) > 20:
            trfetchcount = 20                                          # Max trailer per movie is 20

        data = fileh.readline()                                        # Get trailer max resolution
        datae = data.split('#')                                        # Remove comments
        maxres = datae[0].strip().rstrip("\n")                         # cleanup unwanted characters
        if maxres not in ['1080', '720', '480'] :
            maxres = '720'                                             # Default to 720P

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

        data = fileh.readline()                                        # Get Order by size
        if data != '':
            datah = data.split('#')                                    # Remove comments
            obsize = datah[0].strip().rstrip("\n")                     # cleanup unwanted characters
        else:
            obsize = 'Yes'                                             # Default to Yes

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

        fileh.close()                                                  # close the file
        
        tr_config = {
                     'dbfile': mezzmodbfile,
                     'ltrailerloc': ltrailerloc,
                     'mtrailerloc': mtrailerloc,
                     'mcount':  mfetchcount,
                     'trcount':  trfetchcount,
                     'maxres':  maxres,
                     'mlock':  mlock,
                     'mperf':  mperf,
                     'obsize':  obsize,
                     'onlylt': onlylt,
                     'logoutfile': logoutfile,
                    }

        mgenlog = ("Mezzmo Trailer Checker started - v" + version)
        print(mgenlog)
        genLog(mgenlog)        
        mgenlog = "Finished reading config file."
        genLog(mgenlog)       
        return 
 
    except Exception as e:
        print (e)
        mgenlog = 'There was a problem parsing the config file.'
        genLog(mgenlog)
        print(mgenlog)


def checkCommands(sysarg1, sysarg2):                                   # Check for valid commands
   
    if len(sysarg1) > 1 and sysarg1.lower() not in ['trailer', 'csv', 'sync', 'help']:
        displayHelp()
        exit()
    if 'help' in sysarg1.lower():
        displayHelp()
        exit()


def displayHelp():                                 #  Command line help menu display

        print('\n=========================================================================================')
        print('\nThe only valid commands are -  trailer, sync, csv and help  \n\nExample:  trailer_checker.py trailer')      
        print('\ntrailer\t\t - Runs the trailer checker normally starting with the first movie in the Mezzmo database.')
        print('\ntrailer new\t - Runs the trailer checker normally starting with the newest movie in the Mezzmo database.')
        print('\nsync\t\t - Syncs the Mezzmo Trailer Checker to the Mezzmo database without fetching any trailers.')
        print('\ncsv trailer\t - Creates a CSV file with the trailer information in the Mezzmo Trailer Checker')
        print('\ncsv thistory\t - Creates a CSV file with the history information in the Mezzmo Trailer Checker')
        print('\n ')
        print('\n ')
        print('\n=========================================================================================')


def getMezzmoTrailers(sysarg1= ''):                                     #  Query Mezzmo trailers  
    
    global tr_config
      
    mgenlog = "The Mezzmo DB file is: " + tr_config['dbfile']
    genLog(mgenlog)

    try:
        if sysarg1.lower() in ['trailer', 'sync']:
            genLog("Getting Mezzmo trailer data.")                          
            trdb = openTrailerDB()
            db = openMezDB()
            dbcurr = db.execute('Select MGOFile.File, MGOFileExtras.ID, MGOFileExtras.FileID,   \
            MGOFileExtras.TypeUID, MGOFileExtras.File, MGOFile.Lock, MGOFile.Title from         \
            MGOFileExtras INNER JOIN  MGOFile on MGOFile.ID = MGOFileExtras.FileID order by     \
            MGOFileExtras.FileID',)
            dbtuples = dbcurr.fetchall()     
            del dbcurr
            for a in range(len(dbtuples)):
                curp = trdb.execute('SELECT extras_ID, extras_FileID FROM mTrailers WHERE extras_ID=? AND    \
                extras_FileID=?', (dbtuples[a][1], dbtuples[a][2],))   #  Check Trailers
                currTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')                
                trailertuple = curp.fetchone()
                if not trailertuple:                                   #  Add to trailer database
                    trdb.execute('INSERT or REPLACE into mTrailers (dateAdded, mgofile_file, extras_ID,       \
                    extras_FileID, extras_TypeUID, extras_File, mgofile_lock, mgofile_title) values           \
                    (?, ?, ?, ?, ?, ?, ?, ?)',  (currTime, dbtuples[a][0], dbtuples[a][1], dbtuples[a][2],    \
                    dbtuples[a][3], dbtuples[a][4], dbtuples[a][5], dbtuples[a][6],))
                else:                                                  #  Update trailer database
                    trdb.execute('UPDATE mTrailers SET extras_File=?, mgofile_lock=?, mgofile_title =? WHERE  \
                    extras_ID=? AND extras_FileID=?', (dbtuples[a][4], dbtuples[a][5], dbtuples[a][6],        \
                    dbtuples[a][1], dbtuples[a][2],))
            trdb.commit()
            trdb.close()
            db.close()
            mgenlog = "Finished getting Mezzmo Trailer records." 
            genLog(mgenlog)  
            print(mgenlog)

    except Exception as e:
        print (e)
        mgenlog = 'There was an error getting Mezzmo trailer information'
        print(mgenlog)
        genLog(mgenlog)           


def genLog(mgenlog):                                        #  Write to logfile

        global tr_config
        logoutfile = tr_config['logoutfile']
        fileh = open(logoutfile, "a")                       #  open logf file
        currTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
        data = fileh.write(currTime + ' - ' + mgenlog + '\n')
        fileh.close()


def checkDatabase():

    try:
        global trailerdb

        db = openTrailerDB()

        db.execute('CREATE table IF NOT EXISTS mTrailers (dateAdded TEXT, mgofile_title TEXT,         \
        mgofile_file INTEGER, extras_ID  INTEGER, extras_FileID INTEGER, extras_TypeUID TEXT,         \
        extras_File TEXT, mgofile_lock INTEGER, lastchecked TEXT, tr_resol INTEGER, tr_size INTEGER,  \
        trStatus TEXT, var1 TEXT, var2 TEXT, var3 TEXT, var4 TEXT)')
        db.execute('CREATE UNIQUE INDEX IF NOT EXISTS trailer_1 ON mTrailers (extras_ID, extras_FileID)')
        db.execute('CREATE INDEX IF NOT EXISTS trailer_2 ON mTrailers (mgofile_file)')
        db.execute('CREATE INDEX IF NOT EXISTS trailer_3 ON mTrailers (dateAdded)')
        db.execute('CREATE INDEX IF NOT EXISTS trailer_4 ON mTrailers (trStatus)')

        db.execute('CREATE table IF NOT EXISTS mHistory (dateAdded TEXT, mgofile_title TEXT,          \
        mgofile_file INTEGER, extras_ID  INTEGER, extras_FileID INTEGER, extras_TypeUID TEXT,         \
        extras_File TEXT, mgofile_lock INTEGER,  tr_res TEXT, tr_size INTEGER, newfile TEXT,          \
        lastchecked TEXT, trStatus TEXT, var1 TEXT, var2 TEXT, var3 TEXT, var4 TEXT)')

        db.execute('CREATE table IF NOT EXISTS mTemp (mgofile_title TEXT, mgofile_file INTEGER,      \
        extras_ID  INTEGER, extras_FileID INTEGER, extras_TypeUID TEXT, extras_File TEXT,            \
        extras_FileNew TEXT, mgofile_lock INTEGER, tr_size INTEGER, tr_resol INTEGER)')
        db.execute('CREATE INDEX IF NOT EXISTS trailer_11 ON mTemp (extras_FileID)')
        db.execute('DELETE FROM mTemp')              # Clear temp table on startup

        db.commit()
        db.close()
 
        mgenlog = "Mezzmo check database completed."
        print (mgenlog)
        genLog(mgenlog)

    except Exception as e:
        print (e)
        mgenlog = "There was a problem verifying the database file: " + trailerdb
        print(mgenlog)
        genLog(mgenlog) 
        exit()   


def getMovieList(sysarg1= '', sysarg2= ''):                               # Get list of movies to check

    try:
        if sysarg1.lower() not in ['trailer']:                            # Must be a valid command
            return
        global tr_config
        trinfo = []

        movielimit =  tr_config['mcount']
        trlimit = tr_config['trcount']
        mpref = tr_config['mperf']
        localmatch = '%' + tr_config['mtrailerloc'] + '%'
        ymatch =  'https://www.youtube%'

        db = openTrailerDB()

        if 'new' in sysarg2.lower():                                      # Get trailers for enwest movies
            dbcurr = db.execute('SELECT extras_FileID, mgofile_title, extras_ID, extras_File, lastchecked      \
            from mTrailers WHERE extras_File not like ? and trStatus IS NULL group by extras_FileID order by   \
            extras_FileID DESC LIMIT ? ', (localmatch, movielimit, ))     # Get movie list to check trailers 
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
                if int(counttuple[0]) > 0:                                # Update lastchecked and status
                    currTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    db.execute('UPDATE mTrailers SET lastchecked=?, trStatus=? WHERE extras_FileID=?',  \
                    (currTime, 'Yes', trailer[0],))
                    db.commit()
                    mgenlog = "Skipping movie, local trailers found: " + trailer[1]
                    genLog(mgenlog)
                    print(mgenlog)
                else:                                                     # Get list of Youtube trailers
                    chcurr = db.execute('SELECT extras_FileID, mgofile_title, extras_ID, extras_File from  \
                    mTrailers WHERE extras_File like ? AND extras_FileID=? AND (trStatus NOT LIKE ? OR     \
                    trStatus IS NULL) Limit ? ', (ymatch, trailer[0], '%Bad%', trlimit,)) # Get trailer list to check
                    chktuple = chcurr.fetchall()
                    mgenlog = 'Found ' + str(len(chktuple)) + ' Youtube trailers: ' + trailer[1]
                    print(mgenlog)
                    genLog(mgenlog)
                    for ytube in chktuple:                                # Get local trailers
                        trinfo = getTrailer(ytube[3])
                        if trinfo[0] == 0:                                # Trailer fetched
                            mgenlog = 'Trailer file fetched: ' + trinfo[3] + ' - ' + trinfo[2] + ' - ' + trinfo[1] 
                            genLog(mgenlog)
                            print(mgenlog)
                            updateHistory(trinfo, ytube[3], db)           # Save trailer info to history
                            updateTemp(trinfo, ytube[3], db)              # Write to temp 
                        else:                                             # Error fetching You Tube trailer
                            updateError(ytube[3], db)
                            mgenlog = 'There was an error fetching the local trailer for: ' + ytube[3]
                            genLog(mgenlog)
                            print(mgenlog)
                    result = updateMezzmo(ytube[0], db)                   # Update mezzmo for MGOFile_ID
                    #print('Number of trailers is ' + str(result))
                    if result > 0:                                        # Successfully featched movie trailers
                       updatemTrailers(ytube[0], db)                      # Update mTrailer info
                       moveTrailers()                                     # Move trailers to trailer folder   
 
        db.close()

    except Exception as e:
        print (e)
        mgenlog = "There was a problem getting the movie list." 
        print(mgenlog)
        genLog(mgenlog) 


def updateError(trurl, db):                                               # Update status download error
      
        currTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.execute('UPDATE mTrailers SET lastchecked=?, trStatus=? WHERE extras_File=?',  \
        (currTime, 'Bad', trurl,))
        db.commit()


def updatemTrailers(fileID, db):                                          # Update mTrailer table

        tmpcurr = db.execute('SELECT * FROM mTemp')
        temptuple = tmpcurr.fetchall()
        currTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for temp in temptuple:                                            # Update new trailer info
            db.execute('UPDATE mTrailers SET mgofile_lock=?, tr_size=?, tr_resol=?,      \
            lastchecked=?, trStatus=? WHERE extras_File=?', (temp[7], temp[8], temp[9],  \
            currTime, 'Yes', temp[5],))
        db.execute('DELETE FROM mTemp')       
        db.commit()


def test():

    db = openTrailerDB()
    currTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    db.execute('UPDATE mTrailers SET lastchecked=?, trStatus=? WHERE extras_FileID=? AND \
    NOT trStatus IS ?', (currTime, 'Yes', 2, 'Bad',))
    db.commit()
    db.close()
    exit()

def updateMezzmo(fileID, db):                                             # Update Mezzmo from Temp table     

    try:
        global tr_config
        mperf = tr_config['mperf'].lower()
        obsize = tr_config['obsize'].lower()
        onlylt = tr_config['onlylt'].lower()
        trcount = tr_config['trcount']
        mezzdb = openMezDB()
        trcurr = db.execute('SELECT * FROM mTrailers WHERE extras_FileID = ? LIMIT ?', (fileID, trcount))
        trtuple = trcurr.fetchall()                                      # Get current trailer records
        print('The # of old trailers for: ' + str(fileID) + ' is: ' + str(len(trtuple))) 
        if 'yes' in obsize:                                              # Default order by resolution
            tempcurr = db.execute('SELECT * FROM mTemp ORDER BY tr_size desc ')            
        else:                                                            # Order by size                
            tempcurr = db.execute('SELECT * FROM mTemp ORDER BY tr_resol desc ')
        temptuple = tempcurr.fetchall()                                  # Get new local trailer records
        print('The # of new trailers for: ' + str(fileID) + ' is: ' + str(len(temptuple)))
        if len(temptuple) == 0:                                          # No new trailers found
            mezzdb.commit()
            mezzdb.close()
            mgenlog = 'Mezzmo trailers updated - 0' 
            genLog(mgenlog)
            print(mgenlog)
            return 0

        mezzdb.execute('DELETE from MGOFIleExtras WHERE FileID=?', (fileID,))            
        if 'yes' in mperf:                                               # Add prefer local trailers
            count = 1
            for temp in temptuple: 
                mezzdb.execute('INSERT into MGOFIleExtras (ID, FileID, TypeUID, File) values  \
                (?, ?, ?, ?)', (count, temp[3], temp[4], temp[6],))
                count += 1
            if 'yes' not in onlylt:                                      # Check if only local trailers
                for trlr in trtuple:
                    mezzdb.execute('INSERT into MGOFIleExtras (ID, FileID, TypeUID, File) values  \
                    (?, ?, ?, ?)', (count, trlr[4], trlr[5], trlr[6],))
                    count += 1               
        else:
            count = 1
            if 'yes' not in onlylt:                                      # Check if only local trailers
                for trlr in trtuple:
                    mezzdb.execute('INSERT into MGOFIleExtras (ID, FileID, TypeUID, File) values  \
                    (?, ?, ?, ?)', (count, trlr[4], trlr[5], trlr[6],))
                    count += 1     
            for temp in temptuple: 
                mezzdb.execute('INSERT into MGOFIleExtras (ID, FileID, TypeUID, File) values  \
                (?, ?, ?, ?)', (count, temp[3], temp[4], temp[6],))
                count += 1  
        mezzdb.execute('UPDATE MGOFile SET Lock=? WHERE ID=?', (temp[7], fileID,))
        #db.execute('DELETE FROM mTemp')
        db.commit()        
        mezzdb.commit()         
        mezzdb.close()

        mgenlog = 'Mezzmo trailers updated - ' + str(count - 1)
        genLog(mgenlog)
        print(mgenlog)

        return (count - 1)

    except Exception as e:
        print (e)
        mgenlog = 'There was a problem updating Mezzmo DB for trailer info.'
        genLog(mgenlog)
        print(mgenlog)
        return 0 


def updateHistory(histinfo, trurl, hidb):                                 # Update history table

    try:          
        #hidb = openTrailerDB()
        hicurr = hidb.execute('SELECT * FROM mtrailers WHERE extras_File=?', (trurl,)) 
        hituple = hicurr.fetchone()                                       # Get current trailer info
        #print(str(hituple))
        currTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
        hidb.execute('INSERT into mHistory (dateAdded, mgofile_file, extras_ID, extras_FileID,     \
        extras_TypeUID, extras_File, mgofile_lock, mgofile_title, tr_res, tr_size, lastchecked,    \
        trStatus) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',  (hituple[0], hituple[2],          \
        hituple[3], hituple[4], hituple[5], hituple[6], hituple[7], hituple[1], histinfo[3],       \
        histinfo[2], currTime, histinfo[1],))                             # Update with local trailer info
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
        mgofile_lock, mgofile_title, extras_FileNew, tr_size, extras_file, tr_resol) values           \
        (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (tetuple[2], tetuple[3], tetuple[4], tetuple[5], newlock,    \
        tetuple[1], newtrailer, tempinfo[2], tetuple[6], resolution,))    # Update temp trailer info
        del tecurr
        tedb.commit()

    except Exception as e:
        print (e)
        mgenlog = "There was a problem updating the temp table: " + tedb
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

    return db


def getTrailer(trailer):                                   # Download You Tube trailers

    try:
        global tr_config
        maxres = int(tr_config['maxres'])                  # Get max resolution
        tr_cmd = fmt = ''
        formats = getFormats(trailer)                      # Get available trailer formats
        #print('Formats result is: ' + str(formats))
        if 'Error' in formats:                             # You Tube error getting formats file
            return formats        
        if '137 ' in formats and '140 ' in formats and maxres >= 1080:      # 1080P available
            tr_cmd = "yt-dlp.exe -f 137+140 -q --check-formats --restrict-filenames " + trailer + "-sQ"
            fmt = '1080p' 
        elif '137 ' in formats and '139 ' in formats  and maxres >= 1080:   # 1080P available
            tr_cmd = "yt-dlp.exe -f 137+139 -q --check-formats --restrict-filenames " + trailer + "-sQ"
            fmt = '1080p' 
        elif '22  ' in formats and maxres >= 720:                           # 720P available
            tr_cmd = "yt-dlp.exe -f 22 -q --restrict-filenames " + trailer
            fmt = '720p' 
        elif  '135 ' in formats and '140 ' in formats and maxres >= 480:    # 480P available
            tr_cmd = "yt-dlp.exe -f 135+140 -q --check-formats --restrict-filenames " + trailer + "-sQ"
            fmt = '480p' 
        elif  '135 ' in formats and '139 ' in formats and maxres >= 480:    # 480P available
            tr_cmd = "yt-dlp.exe -f 135+139 -q --check-formats --restrict-filenames " + trailer + "-sQ"
            fmt = '480p' 
        elif '18  ' in formats:                            # 360P available
            tr_cmd = "yt-dlp.exe -f 18 -q --restrict-filenames " + trailer
            fmt = '360p' 
        
        #print (tr_cmd)
        fetch_result = subprocess.call(tr_cmd, shell=True)

        if fetch_result == 0:
            mgenlog = 'Fetched Youtube trailer at: ' + fmt + ' - ' + trailer
            genLog(mgenlog)
            print(mgenlog)
            trfile = renameFiles()                           # Cleanup trailer name and move to temp folder  
            return [fetch_result, trfile[0], trfile[1], fmt] # Return trailer file info and status
                                                             # trfile[0] = new trailer file name
                                                             # trfile[1] = new trailer file size
        elif fetch_result == 1:
            mgenlog = "A Youtube fetching error occured for: " + trailer
            print(mgenlog)
            genLog(mgenlog)
            return fetch_result
    
    except Exception as e:
        print (e)
        mgenlog = 'There was a problem getting the You Tube formats information'
        genLog(mgenlog)
        print(mgenlog)


def getFormats(trailer):                           # Get available You Tube Trailer formats

        formats = []
        tr_cmd = "yt-dlp.exe -F " + trailer + " > output.txt"
        fetch_result = subprocess.call(tr_cmd, shell=True)

        if fetch_result == 0:
            fileh = open("output.txt")             # open formats file
            data = fileh.readlines()            
            for x in range(6, len(data)):
                formats.append(data[x][:4])        # List of available formats
            fileh.close()  
            return formats
        else:
            return 'Error'


def checkFolders():                                # Check folders

    try:
        global tr_config
        trailerloc = tr_config['ltrailerloc']
        if not os.path.exists('temp'):             #  Check temp files location
            os.makedirs('temp')
        command = 'del temp\*.mp4 >nul 2>nul'      #  Delete temp files if exist 
        os.system(command)                         #  Clear temp files
        if not os.path.exists(trailerloc):         #  Check trailer files location
            mgenlog = 'Local trailer file location does not exist.  Mezzmo Trailer Checker exiting.'  
            genLog(mgenlog)
            print(mgenlog)            
            sys.exit()

    except Exception as e:
        print (e)
        mgenlog = 'There was a problem checking folders'
        genLog(mgenlog)
        print(mgenlog)    


def renameFiles():                                  # Rename trailer file names / move to temp folder

        listOfFiles = os.listdir('.')
        pattern = "*.mp4"
        for x in listOfFiles:
            if fnmatch.fnmatch(x, pattern):
                #print (x)
                filestat = os.stat(x)
                fsize = filestat.st_size            # Get trailer size in bytes
                rpos = x.find('[')
                newname = x[:rpos - 1]
                if rpos >= 0:                       # Trim extra characters
                   newname = newname[:rpos - 1]  + ".mp4"
                else:
                   newname = newname  + ".mp4"
                command = "rename " + '"' + x + '" "' + newname + '"'
                os.system(command)                  # Rename trailer file to trimmed name
                command = "move " + '"' + newname + '" temp >nul 2>nul'
                #print(command)
                os.system(command)                  # Move to temp folder till done fetching all
                return [newname, str(fsize)]        # Return new trailer name and size


def moveTrailers():                                 # Move trailers to trailer location

    try:
        global tr_config
        trailerloc = tr_config['ltrailerloc']       # Get locatal path to trailer lcoation

        command = "move temp\*.mp4 " + trailerloc + " >nul 2>nul"
        #print(command)
        os.system(command)
    except Exception as e:
        print (e)
        mgenlog = 'There was a problem moving trailers to teh trailer folder.'
        genLog(mgenlog)
        print(mgenlog)


def checkCsv(sysarg1 = '', sysarg2 = ''):           # Generate CSV files

        if sysarg1.lower() not in 'csv':
            return
        elif sysarg2.lower() not in ['trailer', 'history']:
            print('\nThe valid csv options are:  trailer or history\n')
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
        else:
            curm = db.execute('SELECT * FROM mHistory')
            filename = 'mezhistory_' + fpart + '.csv'            

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
        print (e)
        mgenlog = 'An error occurred creating the CSV file.'
        genLog(mgenlog)
        pring(mgenlog)


def checkFinish(sysarg1):                                    # Successfully finished

    if 'trailer' in sysarg1.lower():                         # Sync trailer db to Mezzmo
        getMezzmoTrailers('sync')        
    mgenlog = 'Mezzmo Trailer Checker completed successfully.'
    print(mgenlog)
    genLog(mgenlog)


checkCommands(sysarg1, sysarg2)                              # Check for valid commands
getConfig()                                                  # Process config file
checkDatabase()                                              # Check trailer database 
checkFolders()                                               # Check trailer and temp folder locations
getMezzmoTrailers(sysarg1)                                   # Load Mezzmo trailers into trailer checker DB
getMovieList(sysarg1, sysarg2)                               # Get list of movies to check and get trailers
checkCsv(sysarg1, sysarg2)
checkFinish(sysarg1)




