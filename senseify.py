import spotipy
from spotipy.oauth2 import SpotifyOAuth
from sense_hat import SenseHat
from pprint import pprint
import time
import json
from PIL import Image
import urllib.request

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
                                                           scope="user-read-currently-playing"))

while True:
	track = sp.current_user_playing_track()
	tname = track['item']['name']
	tartist = track['item']['artists'][0]['name']
	fullinfo = tname + " - " + tartist

	if SHOW_COVER:
		tcover = track['item']['album']['images'][0]['url']
		urllib.request.urlretrieve(tcover, 'cover.png')
		image = Image.open('cover.png')
		new_image = image.resize((8, 8))
		new_image.save('cover_8.png')
		an_image = Image.open("cover_8.png")
		sequence_of_pixels = an_image.getdata()
		list_of_pixels = list(sequence_of_pixels)

	sense.show_message(fullinfo)
	if SHOW_COVER:
		sense.set_pixels(list_of_pixels)
	time.sleep(5)
