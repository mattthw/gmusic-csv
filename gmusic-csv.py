#!/usr/bin/env pyhton
from csv                  import DictWriter
from gmusicapi            import Mobileclient
from operator             import itemgetter
from gmusicapi.exceptions import NotLoggedIn
import getpass, os.path
import sys, getopt
""""(CallFailure, ParseException, ValidationException,
    AlreadyLoggedIn, NotLoggedIn)"""
#GLOBAL VARS
api = Mobileclient()
content = []
helpString = ("usage: gmusic-csv [option]\noptions:"
                +"\n    -o <filename>    :    preemptively name CSV file"
                +"\n    -p '<playlist>'  :    get songs in playlist"
                +"\n    -h               :    display this menu\nexample:"
                +"\n    gmusic-csv -o my_library"
                +"\n    gmusic-csv -p 'summer 2013'")

class Credintials(object):
    def login(self, *args):
        res = api.oauth_login(Mobileclient.FROM_MAC_ADDRESS)
        if (not res):
            print ('\n===================================================='
                + '\nPlease log in. Credentials will be saved as'
                + '\n' + Mobileclient.OAUTH_FILEPATH + '.'
                + '\n----------------------------------------------------')
            Mobileclient.perform_oauth(storage_filepath=Mobileclient.OAUTH_FILEPATH, open_browser=True)
            res = api.oauth_login(Mobileclient.FROM_MAC_ADDRESS)
        print ('----------------------------------------------------')
        if (not res):
            print 'Login failed. Try again or press ctrl+c to cancel.'
            Credintials.login(self, *args)
            return
        else:
            print 'Login successful!\nnow performing selected or default option...'
        print ('====================================================')

class Library(object):
    #get all music owned by user
    def getMusic(self):
        try:
            print('retrieving library...\n'),
            tempList = api.get_all_songs()
            for x in range(len(tempList)):
                gatherList = {
                    "album":       tempList[x].get('album').encode('utf-8', errors='ignore'),
                    "artist":      tempList[x].get('artist').encode('utf-8', errors='ignore'),
                    "name":        tempList[x].get('title').encode('utf-8', errors='ignore'),
                    "trackNumber": tempList[x].get('trackNumber'),
                    "playCount":   tempList[x].get('playCount')
                    }
                content.append(gatherList)
        except NotLoggedIn:
            sys.exit("Error processing request. Error: NotLoggedIn.")

    #get songs from specified playlist in users collection
    def getPlaylist(self, name):
        try:
            print('retrieving playlist.'),
            playlists = api.get_all_user_playlist_contents()
            allSongs = api.get_all_songs()
            allSongsDict = dict()
            for x in range(len(allSongs)):
                gatherList = {
                    "album":       allSongs[x].get('album').encode('utf-8', errors='ignore'),
                    "artist":      allSongs[x].get('artist').encode('utf-8', errors='ignore'),
                    "name":        allSongs[x].get('title').encode('utf-8', errors='ignore'),
                    "trackNumber": allSongs[x].get('trackNumber'),
                    "playCount":   allSongs[x].get('playCount')
                    }
                allSongsDict[allSongs[x].get('id')] = gatherList
            for playlist in playlists:
                if playlist['name'] == name:
                    tracks = playlist['tracks']
                    for track in tracks:
                        id = track['trackId']
                        #print(id)
                        if id in allSongsDict:
                            print(allSongsDict[id])
                            content.append(allSongsDict[id])
        except NotLoggedIn:
            sys.exit("Could not log in - verify credintials.")


class WriteOut(object):
    def writeToFile(self, filename):
        if "." in filename:
            filename = filename.split(".")[0]
        elif filename == "":
            filename = raw_input('save file as: ')
        temp = sorted(content, key = itemgetter('trackNumber'))
        temp = sorted(temp,    key = itemgetter('album'))
        temp = sorted(temp,    key = itemgetter('artist'))

        # filename = raw_input('save file as (do not include .csv or any extension!)\n: ')
        if os.path.exists(str(filename)+'.csv'):
            print (filename, ' exists already. Choose another file name.')
            WriteOut.writeToFile(self, filename)
            return
        try:
            with open(filename+'.csv','w') as outfile:
                print ("  exporting library to CSV format!"),
                writer = DictWriter(outfile, ('artist','album','trackNumber','name','playCount'))
                writer.writeheader()
                writer.writerows(temp)
                print ('\n  \''+str(filename)+str('.csv')+'\' saved in current directory!')
        except IOError:
            sys.exit("<Error> Invalid filename!")


def main(argv):
    try:
        # option = "library"
        filename = ""
        playlist = ""
        try:
            opts, args = getopt.getopt(argv, "hp:o:")
        except:
            print(helpString)
            sys.exit(2)
        for flag, argument in opts:
            if flag == "-h":
                print(helpString)
                sys.exit(2)
            elif flag == "-o":
                filename = str(argument)
                if filename == "":
                    print ("enter a <filename> when using the -o flag.")
                    sys.exit(2)
            elif flag == "-p":
                playlist = str(argument)
        Credintials().login()
        if playlist == "":
            Library().getMusic()
        else:
            Library().getPlaylist(playlist)
            if len(content) <=1:
                print ('{} does not exist as a playlist. Try again.').format(playlist)
                sys.exit(2)
        print ('====================================================')
        WriteOut().writeToFile(filename)
        print ('====================================================')
    except KeyboardInterrupt:
        print "\nShutdown requested...exiting"

if __name__ == '__main__':
    main(sys.argv[1:])