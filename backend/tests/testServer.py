import sys
sys.path.append('apis')
sys.path.append('util')
import CadenceGlobals
import spotipy.util as util
import requests
from subprocess import call
import os
os.system("./clean.sh > /dev/null")

sp_token = "bogus"

if len(sys.argv) > 1:
	if sys.argv[1] == "-test":
		print "Doing a manual server test"
		sp_token = util.prompt_for_user_token(CadenceGlobals.SPOTIFY_USERNAME, client_id=CadenceGlobals.SPOTIFY_CLIENT_ID, client_secret=CadenceGlobals.SPOTIFY_CLIENT_SECRET, redirect_uri=CadenceGlobals.SPOTIFY_REDIRECT_URI)
	elif sys.argv[1] == "-token" and len(sys.argv) > 2:
		sp_token = sys.argv[2]
	else:
		print "Invalid options"
r = requests.get("http://localhost:5000/?atoken={}&username={}".format(sp_token, CadenceGlobals.SPOTIFY_USERNAME))


print r.text #Response of server
