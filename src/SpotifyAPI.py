import spotipy
from spotipy.oauth2 import SpotifyOAuth
from tqdm import tqdm
import numpy as np


class SpotifyApi:
    def __init__(self) -> None:
        self.CLIENT_ID = ""  # ADD client id
        self.CLIENT_SECRET = ""  # Add Client secret id
        self.REDIRECT_URL = "http://localhost:8080/callback/"
        self.SCOPE = 'playlist-modify-public'
        self.api = None

    def connection(self) -> None:
        self.api = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=self.CLIENT_ID,
                client_secret=self.CLIENT_SECRET,
                redirect_uri=self.REDIRECT_URL,
                scope=self.SCOPE))

    def search(self, musicnamelist) -> str:
        urilist = []
        for musicname in musicnamelist:
            result = self.api.search(musicname, type="track", limit=1)
            if result:
                result = result['tracks']['items']
                for item in result:
                    uri = item['uri']
                    urilist.append(uri)
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
        # Check if playlist already exist
        playlistURI = self.getplaylist_uri(playlistname)
        if not playlistURI:
            self.createPlaylist(playlistname)
            playlistURI = self.getplaylist_uri(playlistname)

        if len(urilist) > 100:
            total_minimal_chunks = int(len(urilist)/100)
            chunks = np.array_split(urilist, total_minimal_chunks)
            for chunk in chunks:
                self.addtoplaylist(playlistURI, chunk)
        else:
            self.addtoplaylist(playlistURI, urilist)
