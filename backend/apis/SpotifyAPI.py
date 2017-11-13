import sys
sys.path.append('util')
import CadenceGlobals
import spotipy
import urllib
import spotipy.util as util
import requests;
import base64
import six
from CadenceError import *

class SpotifyAPI():
	def __init__(self, token, username):
		self.username = username
		self.token = token
		
	#Gets artistName, trackName, trackURI from spotify based on input track
	def __processTrack(self, track):
		artist_name = track['artists'][0]['name']
		artist_name = urllib.quote(artist_name.encode('utf-8'))
		track_name = track['name'].encode('utf-8')
		track_name = urllib.quote(track_name)
		track_uri = urllib.quote(track['uri'].encode('utf-8'))
		return [artist_name, track_name, track_uri]

	#Gets the first result from searching the artist name's link to spotify
	def getArtistLink(self, artist):
		sp = spotipy.Spotify()
		return spotify.search(q="artist:{}".format(artist), type="artist")['artists']['items'][0]['external_urls']['spotify']

	#Iterates through the entirety of a playlist and creates a list of items which contain the song information, utilized __processTrack from above.
	def getPlaylistData(self):
		plData = 1;
		try:
			sp = spotipy.Spotify(auth=self.token)
			playlists = sp.user_playlists(self.username)
			plData = []
			while playlists:
			    for i, playlist in enumerate(playlists['items']):
				results = sp.user_playlist(self.username, playlist['id'], fields="tracks,next")
				for i, item in enumerate(results['tracks']['items']):
					track = item['track']
					plData.append(self.__processTrack(track))
			    if playlists['next']:
				playlists = sp.next(playlists)
			    else:
				playlists = False
		except:
			CadenceError.error("Error in SpotifyAPI.getPlaylistData()", sys.exc_info())
		finally:
			return plData
		
	#Prints each track in an input list
	def printTracks(self, tracks):
		for key, val in tracks.iteritems():
			print "{} - {}\n---".format(key, val)
	
	#Creates a playlist for input username using the given playlist data, returns the id of new playlist
	@staticmethod
	def createPlaylist(sp_token, username, plData):
		sp = spotipy.Spotify(auth=sp_token)
		sp.trace = False
		#Creates new playlist for the user
		r = sp.user_playlist_create(username, "CadenceTest 2.3", True)
		playlist_id = r['id']
		track_ids = []
		#Iterates over playlist data and appends the track info to list track_ids
		for item in plData:
			if item[2] == "notrackuri":
				pass
			else:
				spotify_uri = item[2]
				spotify_uri = spotify_uri.split(":")
				spotify_uri = spotify_uri[2]
				#item in pldata has form:
				#['band', 'song', 'spotify:track:<id>']
				track_ids.append(spotify_uri)
			
		#Adds all the tracks we just got to the new playlist
		results = sp.user_playlist_add_tracks(username, playlist_id, track_ids)
		return playlist_id;

	#Retrieves the Spotify URI of given artist's song
	@staticmethod
	def getTrackURI(artist, track):
		sp = spotipy.Spotify()
		results = sp.search(q=track + ' ' + artist, type='track')
		results = results['tracks']['items']
		if len(results) > 0:		
			return results[0]['uri']
		else:
			return "notrackuri"

#Testing...
def testSpotify():
	client_id = CadenceGlobals.SPOTIFY_CLIENT_ID
	client_secret = CadenceGlobals.SPOTIFY_CLIENT_SECRET
	redirect_uri = CadenceGlobals.SPOTIFY_REDIRECT_URI 
	username = CadenceGlobals.SPOTIFY_USERNAME
		
	scope = CadenceGlobals.SPOTIFY_SCOPE
	token = util.prompt_for_user_token(username, scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
	spot = SpotifyAPI(token, username)
	plData = spot.getPlaylistData()
	SpotifyAPI.createPlaylist(token, username, plData)
	spot.getTrackURI("Rush", "2112")

