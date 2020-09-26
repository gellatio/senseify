import spotipy
from spotipy.oauth2 import SpotifyOAuth
from sense_hat import SenseHat
from pprint import pprint
import time
import json

sense = SenseHat()

with open('config.json') as f:
    data = json.load(f)
##EDIT VALUES IN CONFIG.JSON##
SP_CLIENT_ID = data['SP_CLIENT_ID']
SP_CLIENT_SECRET = data['SP_CLIENT_SECRET']
SP_REDIRECT_URI = data['SP_REDIRECT_URI']

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SP_CLIENT_ID,
                                                           client_secret=SP_CLIENT_SECRET,
                                                           redirect_uri=SP_REDIRECT_URI,
                                                           scope="user-read-currently-playing"))
while True:
    track = sp.current_user_playing_track()
    tname = track['item']['name']
    tartist = track['item']['artists'][0]['name']
    tcover = track['item']['album']['images'][0]['url']
    fullinfo = tname + " - " + tartist
    sense.show_message(fullinfo)
    time.sleep(5)

    