import spotipy
from spotipy.oauth2 import SpotifyOAuth
from sense_hat import SenseHat
from pprint import pprint
import time
import json
import sys

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
	try:
		cp = sp.current_playback()
		vol = cp['device']['volume_percent']
		devid = cp['device']['id']
		for event in sense.stick.get_events():
			if event.action == "pressed":
				if event.direction == "up":
					sp.volume(vol+10,device_id=devid)
					print("Raised volume")
				elif event.direction == "down":
					sp.volume(vol-10,device_id=devid)
					print("Lowered volume")
				elif event.direction == "left":
					sp.previous_track(device_id=cp['device']['id'])
					print("Rewinded to last track")
				elif event.direction == "right":
					sp.next_track(device_id=cp['device']['id'])
					print("Skipped track")
				elif event.direction == "middle":
					sp.pause_playback(device_id=cp['device']['id'])
					print("Paused")
	except KeyboardInterrupt:
		raise
	except:
		print("Unexpected error", sys.exc_info()[0])
		pass
