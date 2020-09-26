# Senseify
## Spotify controls for SenseHat

### Requirements
* Raspberry Pi
* Sense Hat
* Python3+
* Required Addons (Added using `pip/pip3 install <name>`)
  * Spotipy
  * PPrint
  * Sensehat (Added using `sudo apt-get install sense-hat`)
  
### How to setup
* Install & setup all the requirements listed above & clone the repo (obviously)
* Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/) and create a new application
![Spotify Developer Dashboard](https://i.imgur.com/Km5P230.png)
* Once you have created your app, click on "Show Client Secret and copy the Client ID & Client Secret to config.json
![Show the client secret](https://i.imgur.com/OEB4RYN.gif)
* Now click on Edit Settings on the Spotify Dashboard, and add your redirect URI as one of the whitelisted URI's. (`http://localhost:8080` is the default, the website does not have to work, it just needs a place to redirect to.)
![Whitelist the URI](https://i.imgur.com/x9Ykeyh.gif)
* Now open 2 terminal windows and cd into the directories. Then type `python3 senseify.py` in one, and `python3 controlify.py`


### Known issues
* The player will not work if no music is playing. It will just stop the program.
* Volume control does not work on any iOS devices. There is no way around this, Apple is just stupid.
* Browser windows will open randomly when the program is running, this is just the program authing itself on Spotify & getting any needed info. This program is completely safe, as you are the one running the application on Spotify!
* Non-English characters will not appear, this isn't fixable either, since this is something SenseHat needs to add.
* If you find any issues or have any critisism, feel free to leave an issue report or make a pull request! I am still fairly new to Python, I haven't done it in a few years so anything helps! :)
