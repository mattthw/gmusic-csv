#!/usr/bin/env pyhton
from csv import DictWriter
from gmusicapi import Mobileclient
from operator import itemgetter
import getpass, os.path
from gmusicapi.exceptions import NotLoggedIn
import sys
""""(CallFailure, ParseException, ValidationException,
    AlreadyLoggedIn, NotLoggedIn)"""

class verifyUser(object):
    def login(self, *args):
        print 'attempting to login.'
<<<<<<< HEAD
        api.login(raw_input('username\n: '), getpass.getpass('\nNOTICE: if you use secondary authentication use an app specific password!\npassword (hidden)\n: '))

=======
        logged_in = api.login(raw_input('username\n: '), getpass.getpass('\nNOTICE: if you use secondary authentication use an app specific password!\npassword (hidden)\n: '))
            # IMPORTANT: If you use secondary authentication for gogle music
            # you need to generate an app specific password!
        return logged_in
>>>>>>> 31d4bafe68de80cb2275a9c0712dee23d685b85c

class RetrieveSongs(object):
    def songList(self):
        try:
            print 'attempting to retrieve song info.'
            tempList = api.get_all_songs()
            for x in range(len(tempList)):
                gatherList = {
                    "album":    tempList[x].get('album').encode('utf-8'),
                    "artist":    tempList[x].get('artist').encode('utf-8'),
                    "name":    tempList[x].get('title').encode('utf-8'),
                    "trackNumber":    tempList[x].get('trackNumber'),
                    "playCount":    tempList[x].get('playCount')
                    }
                content.append(gatherList)
        except NotLoggedIn:
            sys.exit("<Error> Not logged in. Check account info or network status.")

        return content

    # def playLists(self):
        # print 'attempting to retrieve playlist song info.'
        # playListTemp = api.get_all_user_playlist_contents()
        # tempdictionary = {}
        # for x in range(len(playListTemp)):
        #     tempdictionary = dict(playListTemp[x])
        #     for key, value in tempdictionary.items():
        #         if isinstance(value,list):
        #             print 'first dict loop'
        #             tempdictionary = {'track':value[0]}
        #             for k2, v2 in tempdictionary.items():
        #                 RetrieveSongs().runThrough(v2)
        #                 tempdictionary = dict(v2)
        #                 print 'second dict loop'
        #                 for k3, v3 in tempdictionary.items():
        #                     if isinstance(v3, dict):
        #                         print 'third dict loop'
        #                         RetrieveSongs().runThrough(v3)

    # def runThrough(self, *args):
        # print '\n'
        # for key, value in args[0].items():
        #     if isinstance(value, dict):
        #         RetrieveSongs().runThrough(value)
        #     else:
        #         print
        #         gatherList = {
        #         "album":    args[0].get('album').encode('utf-8'),
        #         "artist":    tempList[x].get('artist').encode('utf-8'),
        #         "name":    tempList[x].get('title').encode('utf-8'),
        #         "trackNumber":    tempList[x].get('trackNumber')
        #         }



        #     tempdict2 = dict(tempdictionary['tracks'])
        #     print tempdict2.keys()



        #     for y in range(len(tempdictionary.keys())):
        #         print tempdictionary['tracks']
        # print range(len(playListTemp))
        # newPlaylistDict = {}
        # for x in range(len(playListTemp)):
        #     tempstr = str('playlist')+str(x)
        #     tempdictionary = {tempstr:dict(playListTemp[x])}
        #     newPlaylistDict.update(tempdictionary)

        # print newPlaylistDict.items()
        # print newPlaylistDict['playlist'].values()

        # for x in range(len(newPlaylistDict)):
        #     plname = newPlaylistDict['playlist']['name']
        #     for y in range(len(newPlaylistDict['playlist']['tracks']['track'])):
        #         gatherList = {
        #             "album": 0,
        #             "artist": 0,
        #             "name": 0,
        #             "trackNumber": 0,
        #             "playlist": 0
        #         }
        #     content.append(gatherList)
        # return content

class WriteOut(object):
    def writeToFile(self):
        temp = sorted(content, key=itemgetter('trackNumber'))
        temp = sorted(temp, key=itemgetter('album'))
        temp = sorted(temp, key=itemgetter('artist'))

        filename = raw_input('save file as (do not include .csv or any extension!)\n: ')
        if os.path.exists(str(filename)+'.csv'):
            print filename, ' exists already. Choose another file name.'
            filename = raw_input(': ')
        try:
            with open(filename+'.csv','w') as outfile:
                writer = DictWriter(outfile, ('artist','album','trackNumber','name','playCount'))
                writer.writeheader()
                writer.writerows(temp)
                print('wrote song info to '+str(filename)+str('.csv'))
        except IOError:
            sys.exit("<Error> Invalid filename!")

#GLOBAL VARS
api = Mobileclient()
content = []

def main():
    verifyUser().login()
    RetrieveSongs().songList()
    WriteOut().writeToFile()

if __name__ == '__main__':
    main()
