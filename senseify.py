import threading
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from sense_hat import SenseHat
from pprint import pprint
import time
import json
from PIL import Image
import urllib.request
import sys

sense = SenseHat()

with open('config.json') as f:
    data = json.load(f)
##EDIT VALUES IN CONFIG.JSON##
SP_CLIENT_ID = data['SP_CLIENT_ID']
SP_CLIENT_SECRET = data['SP_CLIENT_SECRET']
SP_REDIRECT_URI = data['SP_REDIRECT_URI']
SHOW_COVER = data['SHOW_COVER']

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SP_CLIENT_ID,
                                                           client_secret=SP_CLIENT_SECRET,
                                                           redirect_uri=SP_REDIRECT_URI,
                                                           scope="user-read-currently-playing,user-read-playback-state,user-modify-playback-state,streaming,app-remote-control"))

def sense_loop():
	while True:
		try:
			track = sp.current_user_playing_track()
			tname = track['item']['name']
			tartist = track['item']['artists'][0]['name']
			fullinfo = tname + " - " + tartist

			if SHOW_COVER:
				try:
					tcover = track['item']['album']['images'][0]['url']
					urllib.request.urlretrieve(tcover, 'cover.png')
					image = Image.open('cover.png')
					new_image = image.resize((8, 8))
					new_image.save('cover_8.png')
					an_image = Image.open("cover_8.png")
					sequence_of_pixels = an_image.getdata()
					list_of_pixels = list(sequence_of_pixels)
					coverAvail = 1
				except IndexError as e:
					print("ERROR!")
					print(e)
					print("Do not panic, this is normal is you are playing from local files.")
					coverAvail = 0

			sense.show_message(fullinfo)
			if SHOW_COVER:
				if coverAvail == 1:
					sense.set_pixels(list_of_pixels)
				if coverAvail == 0:
					print("Did not show cover since cover not available")
			time.sleep(5)
		except KeyboardInterrupt:
			sense.clear()
			raise
		except:
			print("Unexpected error", sys.exc_info()[0])
			pass

def control_loop():
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
			sense.clear()
			raise
		except OSError:
			pass
		except:
			print("Unexpected error", sys.exc_info()[0])
			pass

thread1 = threading.Thread(target=control_loop)
thread1.start()
thread2 = threading.Thread(target=sense_loop)
thread2.start()
