import re
import os
import getpass

folderpath = os.getcwd() + os.sep
songlistpath = "/media/" +  getpass.getuser() + os.sep + "mypath" + os.sep


def populate_artistsongs ():
  temphold = os.listdir (songlistpath)
  wr = open(os.getcwd() + os.sep + "songs.txt", "wb")

  print "\n Songs Details to fetch: " + str(songlistpath)
  print "\n Check path exist: " + str ("yes" if (len(temphold)) else "no")

  if (len(temphold)):
    fileother = []

    temphold.sort()

    for val in temphold:
      #print val

      if val.endswith (".mp3"): 
        wr.write( val.strip() + "\n")
      else:
        fileother.append (val)

    print "\n\n non MP3 files:"
    for val in fileother:
      print val

  return

def options_display(): 

  temphold = []
  for val in  os.listdir( folderpath ):
    if val.endswith(".torrent"):
      temphold.append(val)

  for index in xrange(0, len( temphold )):
    print str( index + 1 ) + " : " + str(temphold[index])

  tempval = int( raw_input( "\n -- Select Torrent : " ) )
  if (tempval > (len(temphold) + 1)):
    print "\n ERROR : slected input is invalid"
    exit(0)

  fd = open( folderpath + temphold[ tempval -1 ], "rb" ).readlines()
  listmp3 = []

  for val in fd:
    temphold = val.split("eed6:lengthi")
    for index in xrange(0, len(temphold) - 1):
      tempval = "".join( temphold[index].split(":pathl")[1].split(":")[1:]).strip() 
      #" ".join( temphold[index].split(":pathl")[1].split(" ")[0:]).strip()
      if tempval.endswith(".mp3"):
        listmp3.append( tempval )

  #print "DEBUG : mp3 information!"
  
  if ( len(listmp3) ):
    wr = open(os.getcwd() + os.sep + "songs.txt", "wb")
    for val in listmp3:
      if listmp3.index( val) == 0:
        wr.write( val.strip() )
      else:
        wr.write("\n" + val.strip())
    wr.close()

  else:
    print "\n INFO : no contents to form the new file"

  #print "DEBUG : completed!"


def get_functional():
  currentDir = os.getcwd()
  list1 = "songs.txt"
  
  content2 = {}
  
  for val in open(currentDir + os.sep + list1, "rb" ).readlines():
    temphold = re.split(" ", val.strip(), 2)
    newcontent = temphold[-1].split ("-")
   
    if (len (newcontent) >= 2):
      print "DEBUG: - " + str(newcontent)
      content2.update( {newcontent[-2]:newcontent[-1]} )
    else:
      print "ERROR: unexpected: " + str(newcontent)
      exit(-1)
      
  print "DEBUG : contents of new torrent \n" + str(content2)
      
  for val in os.listdir(songlistpath):
    if( val.endswith( ".mp3" ) ):
      if (val.strip() in content2.keys()):
        content2.pop( val.strip() )
		    
  print "\n download contents are:- \n"
		    
  temphold = []
  for key, val in content2.iteritems():
    temphold.append( str(val) + " " + str(key) )

  temphold.sort()
  for val in temphold:
    print val

def footer_display():
  pass

def header_display():
  print "\n\n" 
  print "==========================================================="
  print "| Working:-                                                |"
  print "|                                                          |"
  print "| 1. Takes torrent files from configurable Download folder |"
  print "| 2. Works only for Music torrents                         |"
  print "==========================================================="
  print "\n\n"


if __name__ == '__main__':

  #print "INFO : inside the first block!"

  header_display()

  print " 1) get songs to current directory - songs.txt"
  print " 2) Check whether the compare folder is avialable - " + str(songlistpath)
  print " 3) get new songs"
  print " 4) Populate Artist-Songs"
  print " 5) Exit"

  tempval = 0
  while (tempval <=0) or (tempval > 5):
    tempval = int( raw_input( "\n -- Enter Selection : " ) )

  if (tempval == 5):
    exit(0)
  elif (tempval == 4):
    populate_artistsongs ()
  elif (tempval == 2):
    try:
      os.listdir (songlistpath) 
      print "\n songs list path: " + str(songlistpath)

    except OSError:
      print "\n Folder does not exist: " + str(songlistpath)
     
  elif (tempval == 1):
    options_display()
  else:
    try:
      os.listdir (songlistpath) 
      options_display()
      get_functional()
    except OSError:
      print "\n Folder does not exist: " + str(songlistpath)

  footer_display()
