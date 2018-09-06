
from utilities.IOFunctions import *
import os

# Extract the xml from the library file, parse it and return a list of artists.
def Import():
    file = os.getcwd() + "\\Library.xml"
    raw = LoadFileContents(file)
    list = GatherList(raw)
    return list

# Actually combs the xml, looking for artists from each song.
def GatherList(raw:str):
    artists = []
    rawList = raw.splitlines()
    for line in rawList:
        if "<key>Album Artist</key><string>" in line:
            artist = line.replace('<key>Album Artist</key><string>','').replace('</string>','').replace('\t','')
            if artist not in artists:
                artists.append(artist)
    return artists
