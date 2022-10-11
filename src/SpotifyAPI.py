import spotipy
from spotipy.oauth2 import SpotifyOAuth
from tqdm import tqdm
import numpy as np


class SpotifyApi:
    def __init__(self) -> None:
        self.CLIENT_ID = ""
        self.CLIENT_SECRET = ""
        self.REDIRECT_URL = "http://localhost:8888/callback/"
        self.SCOPE = 'playlist-modify-public'
        self.api = None

    def connection(self) -> None:
        self.api = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=self.CLIENT_ID,
                client_secret=self.CLIENT_SECRET,
                redirect_uri=self.REDIRECT_URL,
                scope=self.SCOPE))

    def search(self, textfilename, musicnamelist) -> str:
        print("Searching for songs and retriveng song URI...")
        urilist = []
        songsnotfound = []
        for musicname in tqdm(musicnamelist):
            try:
                result = self.api.search(musicname, type="track", limit=1)
                if result:
                    result = result['tracks']['items']
                    for item in result:
                        uri = item['uri']
                        urilist.append(uri)
            except:
                songsnotfound.append(musicname)

        with open(textfilename, "w") as output:
            output.write(str(songsnotfound))

        return urilist

    def addtoplaylist(self, playlistname, trackidlist):
        self.api.playlist_add_items(playlistname, trackidlist)

    def getplaylist_uri(self, playlistname):
        results = self.api.current_user_playlists()
        for i, item in enumerate(results['items']):
            if playlistname in item['name']:
                return item['uri']

    def createPlaylist(self, playlistname):
        playlistexist = self.getplaylist_uri(playlistname)
        if not playlistexist:
            user_id = self.api.me()['id']
            self.api.user_playlist_create(user_id, playlistname)
            print("SUCCESS: Playlist created.")
        else:
            print("ERROR: Playlist already exist!")

    def musicfoundlist(self, musicnamelist):
        musicfound = []
        musicnotfound = []
        for name in tqdm(musicnamelist):
            found_temp = []
            notfound_temp = []
            res = self.search(name)
            if res:
                found_temp.append(res)
            else:
                notfound_temp.append(res)

            musicfound.append(found_temp)
            musicnotfound.append(notfound_temp)

        return musicfound

    def processplaylist(self, playlistname, urilist):
        print("Adding to playlist...")
        # Check if playlist already exist
        playlistURI = self.getplaylist_uri(playlistname)
        if not playlistURI:
            self.createPlaylist(playlistname)
            playlistURI = self.getplaylist_uri(playlistname)

        while urilist:
            self.addtoplaylist(playlistURI, urilist[:100])
            urilist = urilist[100:]
