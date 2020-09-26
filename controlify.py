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
                                                           scope="user-read-playback-state,user-modify-playback-state,streaming,app-remote-control"))
while True:
    cp = sp.current_playback()
    vol = cp['device']['volume_percent']
    devid = cp['device']['id']
    for event in sense.stick.get_events():
        if event.action == "pressed":
      
            if event.direction == "up":
                sp.volume(vol+10,device_id=devid)
            elif event.direction == "down":
                sp.volume(vol-10,device_id=devid)     
            elif event.direction == "left":
                sp.previous_track(device_id=cp['device']['id'])
            elif event.direction == "right":
                sp.next_track(device_id=cp['device']['id'])
            elif event.direction == "middle":
                sp.pause_playback(device_id=cp['device']['id'])
                print("Paused")
        time.sleep(0.5)