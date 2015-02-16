gmusic-csv
=============
_previously named gmaGetLibrary_

A simple python script for saving your music library in CSV format
___

######Depends on:
- Python 2.7.x (python 3 compatability untested)
- [gmusicapi](https://github.com/simon-weber/Unofficial-Google-Music-API)

___

#####INPUT:
You will need the following:

1. the google account used for Google Play Music
2. password for acocunt OR [application specific password](https://security.google.com/settings/security/apppasswords) if you use 2 factor authentication

#####OUTPUT
the output will be a .csv file containing:

_album, artist, title, track number, playcount_

![output file opened in LibreOffice](http://i.imgur.com/GzeEB2D.png)

I used LibreOffice Calc to open, format, and sort the data based on my needs.

#####USAGE:
```
usage: gmusic-csv [option]
options:
    -o <filename>    :    preemptively name CSV file
    -h               :    display this menu
example:
    gmusic-csv -o my_library
```
___

#### Check out these projects as well:
- [gmusic-migrate](https://github.com/brettcoburn/gmusic-migrate)
- [gmusicapi-scripts](https://github.com/thebigmunch/gmusicapi-scripts)
