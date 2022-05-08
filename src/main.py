import glob

from FileHandle import FileHandle
from SpotifyAPI import SpotifyApi

if __name__ == "__main__":
    api = SpotifyApi()
    api.connection()

    filenamelist = glob.glob("files/*")
    fileobj = FileHandle(filenamelist)
    getmusiclist = fileobj.getmusiclist()
    musicurilist = api.search(getmusiclist)
    api.processplaylist("newplaylist", musicurilist)
