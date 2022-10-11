import glob
import pathlib

from FileHandle import FileHandle
from SpotifyAPI import SpotifyApi

if __name__ == "__main__":
    api = SpotifyApi()
    api.connection()

    getsubfolderlist = glob.glob("D:/Music/World" + "/*")
    #playlistname = "English Hits 2011"
    #fullpath = "D:/Music/English Hits/English Hits 2011"
    for foldername in getsubfolderlist:

        playlistname = pathlib.PurePath(foldername)
        playlistname = str(playlistname.name)

        filenamelist = glob.glob(foldername + "/*")
        fileobj = FileHandle(filenamelist)

        getmusiclist = fileobj.getmusiclist()
        musicurilist = api.search(
            str("C:/Users/ia_tu/Downloads/"+playlistname+".txt"), getmusiclist)
        api.processplaylist(playlistname, musicurilist)
