#############################################################################
# Author   : Vipin Varghese
# Date     : 13-Jul-2011
#============================================================================
#
# Description:
# ===========
# This is generic reusable script to fetch mp3 files in folders & sort of
# redudant files 
#
# TO DO: 
# ======
# 1) in-cooperate feature of parsing sub dictionary level.
#============================================================================
#
# History:
# ----Date---- -----Who----- -----------Comments (Changes, Reason)-----------
#
# 4-Jun-2011   Vipin Varghese              Added Header
#                                          Added dynamic path resloution
# 23-Apr-2012  Vipin Varghese              Modified header
#                                          Added error & directory handling
#                                          Added moving of size zero files
#############################################################################

import sys
import os
import time
import re
import shutil

# intial list to hold the files in the folder "/media/Backup/Songs/The\ Official\ UK\ Top\ Singles\ Chart"
path = os.getcwd()
tempFolder = path + os.sep + 'tmp'

def header():
  print "\n\n"
  print "==========================================================================================="
  print "| Working:-                                                                               |"
  print "| ========                                                                               |"
  print "|                                                                                        |"
  print	"|  1. Using current directory location as input                                           |"
  print "|  2. Parses files with number in start.                                                  |"
  print "|  3. Compared w.r.t. name by ignoring the first numerical values                         |"
  print "|  4. Similar files are hold in temp folder of the given path                             |"
  print "==========================================================================================="
  print "\n\n"

def createTemp():
  global tempFolder

  try:
    os.mkdir(tempFolder)
  except OSError:
    pass


def moveFilesToTemp(finalSameList):
  global path, tempFolder
  #print "DEBUG : Move the same files to temp folder!"
  for files in finalSameList:
    shutil.move( (path + os.sep + files), (tempFolder + os.sep + files) )


def utility():
  global path
  #print "DEBUG : Searching a pre-defined location for files!"

  #print os.walk(path)
  # have to implement using walk through folders & form the digest

  musicList =  os.listdir(path)

  musicDistinct = []
  musicSame = []

  if ( len(musicList) > 0):
    #print "DEBUG : musicList ==> " + str(musicList)  + "!"
  
    for files in musicList:
      tempFileSplit = files.split(" ")
      #print "\nDEBUG : tempFileSplit ==> " + str(tempFileSplit)  + " !"

      SearchObj = re.match( '[0-9].', tempFileSplit[0])
      #print "DEBUG : boolFlag ==> " + str(boolFlag)  + " !"
      if ( SearchObj ):
        musicSame.append(files)
      else:
        musicDistinct.append(files)

  #print "\nDEBUG : Same Music files are ==> " + str(musicSame) 
  #print "\nDEBUG : Distinct Music files ==> " + str(musicDistinct) 

  #for index,value in enumerate(musicSame): 
    #print str(index) + " - " + str(value)

  #print "DEBUG : remove the extra tag in name format & check in distinct!"
  finalSameList = []

  if (len(musicSame)):

    for music in musicSame:
      if ( (" ".join(music.split()[1:])).strip() in musicDistinct ):
        finalSameList.append(music)
      else:
        musicDistinct.append(music)

#print "\n\nDEBUG : Distinct Music file are!"
#for index,value in enumerate(musicDistinct): 
  #print str(index) + " - " + str(value)

#print "\n\nDEBUG : Same Music file are!"
#for index,value in enumerate(finalSameList): 
  #print str(index) + " - " + str(value)

  createTemp()
  moveFilesToTemp(finalSameList)

  #print "DEBUG : Renaming files in tmp folder!"
  os.chdir(tempFolder)

  #print "INFO : files in temp folder are : " 
  #for files in os.listdir(tempFolder):
    #os.rename( files, (" ".join(files.split()[1:])).strip() )
    #print " DEBUG : " + str(files).strip()
    #print " DEBUG : " + str(" ".join(files.split()[1:])).strip()
    #os.rename( (path + os.sep + files), (path + os.sep + (" ".join(files.split()[1:-2])).strip()) )

#print "files inside tmp " + str(os.listdir(tempFolder))

# please make False in first run, to get the files in temp folder
# manually cut all files and copy to parrent folder
# if set True it will check in search folder for renaming files with starting number

  #if (False):
  if (True):
    os.chdir(path)
    os.rmdir(tempFolder)

    #print "DEBUG : rename files with starting !"
    filesInPath = os.listdir(path)

    #print "DEBUG : files in path ==> " + str(filesInPath)

    for files in filesInPath:
      tempFileSplit = files.split()

      SearchObj = re.match( '[0-9].', tempFileSplit[0])

      if (SearchObj):
        # check whether there is file with same name existing
        if ( os.path.isfile (path + os.sep + (" ".join( tempFileSplit[1:] )).strip())):
             print "ERROR : there is file with same name : [" + str(path + os.sep + (" ".join( tempFileSplit[1:] )).strip()) + "]"
        else:                                
            # rename file
            os.rename( (path + os.sep + files), (path + os.sep + (" ".join( tempFileSplit[1:] )).strip() ) )

  print "Files cleansed in the given folder are :"
  for index,value in enumerate( os.listdir(path) ): 
    print str(index).zfill(4) + " - " + str(value)

def checkByNameCase ():
    global path

    #print "DEBUG : check given path if exsist !"
    musicList =  os.listdir(path)
    caseDifferentMusic = []
    SplitFail  = []

    # ensure if given listdir is file or not
    for listDet in musicList:
      if( os.path.isfile(listDet)):
        if (listDet.endswith(".mp3")):
          pass
        else:
          #print "\n DEBUG : files been removed is " + str(listDet)
          musicList.remove(listDet)
      else:
        #print "\n DEBUG : non files been removed is " + str(listDet)
        musicList.remove(listDet)

    for mFile in musicList:
      try:
        tempDump = mFile.split("-")[1].strip()
        pass
      except IndexError:
        #print "\n DEBUG : mFile failed to split ==> " + str(mFile)
        SplitFail.append(mFile)
        continue

    # if there are files which failed to get split; move them to temp folder 
    if ( len(SplitFail) ):
      print "\n INFO : Split fail files are ==> " + str(SplitFail)
      createTemp()
      moveFilesToTemp(SplitFail)

    #print "DEBUG : get files in the folder!"
    if ( len(musicList) ):
      # convert the file names to upper case & get song name by using the deleimeter "-"
      musicUpper = map(lambda x:x.upper().split("-")[1].strip(), musicList)
      #musicUpper.sort()
      #print "\n DEBUG : musicUpper ==> " + str(musicUpper)
   
      # if any matched move specific file to temp folder!
      for index in xrange(0, (len(musicList) - 2)): # we only have to check for (n - 1) files
        for files in musicList[(index+1):]:
         
          if (musicUpper[index] == files.split("-")[1].upper().strip()):
            if (files.split("-")[1].upper().strip() not in map(lambda x:x.upper().split("-")[1].strip(), caseDifferentMusic)):
              caseDifferentMusic.append(files)

      createTemp()
      moveFilesToTemp(caseDifferentMusic)

    else:
      #print "DEBUG : no files found in given location !"
      pass
 
    if (len( caseDifferentMusic )):
      print "INFO : caseDifferentMusic ==> " + str(caseDifferentMusic)

def movefilesizezero ():
    global path, tempFolder
    #print "DEBUG : fetching the list of files in the location!"

    #print "DEBUG : moving files of size 0 to temp folder!"
    createTemp()

    for metadata in os.walk( path ):
      # get the file only
      for files in metadata[2]:
        #print "DEBUG : file name : " + str(files)
        #check size of the file is zero
        if ( os.stat(path + os.sep + files).st_size == 0):
	  print "\n DEBUG : zero size movig file : " + str(path + os.sep + files) + "; to : " + str(tempFolder)
          shutil.move( (path + os.sep + files), (tempFolder + os.sep + files) )


if (__name__ == "__main__"):
  print "INFO : START!"

  header()
  utility()
  checkByNameCase()
  movefilesizezero()

  print "INFO : END!"
