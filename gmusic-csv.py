#!/usr/bin/env pyhton
from csv                  import DictWriter
from gmusicapi            import Mobileclient
from operator             import itemgetter
from gmusicapi.exceptions import NotLoggedIn
import getpass, os.path
import sys, getopt
""""(CallFailure, ParseException, ValidationException,
    AlreadyLoggedIn, NotLoggedIn)"""

class verifyUser(object):
    def login(self, *args):
        print 'Please log in. Secondary authentication users need an app-specific password.\nPassword will not be stored.'
        api.login(
            raw_input('username: '),
            getpass.getpass('password: '))

class RetrieveSongs(object):
    def getLibrary(self):
        try:
            print('retrieving library.'),
            tempList = api.get_all_songs()
            for x in range(len(tempList)):
                gatherList = {
                    "album":       tempList[x].get('album').encode('utf-8'),
                    "artist":      tempList[x].get('artist').encode('utf-8'),
                    "name":        tempList[x].get('title').encode('utf-8'),
                    "trackNumber": tempList[x].get('trackNumber'),
                    "playCount":   tempList[x].get('playCount')
                    }
                content.append(gatherList)
        except NotLoggedIn:
            sys.exit("Could not log in - verify credintials.")

    def getUserPlist(self):
        print "not implemented"

    def getSharedPlist(self):
        print "not implemented"

    def main(self, option):
        if str(option) == "shared":
            self.getSharedPlist()
        elif str(option) == "user":
            self.getUserPlist()
        else:
            self.getLibrary()

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
            print filename, ' exists already. Choose another file name.'
            filename = raw_input(': ')
        try:
            with open(filename+'.csv','w') as outfile:
                print(" exporting library to CSV format."),
                writer = DictWriter(outfile, ('artist','album','trackNumber','name','playCount'))
                writer.writeheader()
                writer.writerows(temp)
                print(' saved as \''+str(filename)+str('.csv')+'\'')
        except IOError:
            sys.exit("<Error> Invalid filename!")

#GLOBAL VARS
api = Mobileclient()
content = []

def main(argv):
    option = "library"
    filename = ""
    try:
        opts, args = getopt.getopt(argv, "ht:o:")
    except:
        print("usage: gmusic-csv [option]\noptions:\n    -o <filename>    :    preemptively name CSV file\n    -h               :    display this menu\nexample:\n    gmusic-csv -o my_library")
        sys.exit(2)
    for flag, argument in opts:
        if flag == "-h":
            print("usage: gmusic-csv [option]\noptions:\n    -o <filename>    :    preemptively name CSV file\n    -h               :    display this menu\nexample:\n    gmusic-csv -o my_library")
            sys.exit(2)
        elif flag == "-o":
            filename = str(argument)
            if filename == "":
                print "enter a <filename> when using the -o flag."
                sys.exit(2)
        # elif flag == "-t":
        #     option = str(argument)
    verifyUser().login()
    RetrieveSongs().main(option)
    WriteOut().writeToFile(filename)

if __name__ == '__main__':
    main(sys.argv[1:])
