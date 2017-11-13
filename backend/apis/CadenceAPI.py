import sys
from SpotifyAPI import *
from LastFmAPI import *
sys.path.append('util')
import CadenceGlobals
from CadenceError import *


from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

import threading
import spotipy.util as util
import urllib
import random
import traceback

client_id = CadenceGlobals.SPOTIFY_CLIENT_ID 
client_secret =  CadenceGlobals.SPOTIFY_CLIENT_SECRET
redirect_uri =  CadenceGlobals.SPOTIFY_REDIRECT_URI
playlist_size =  CadenceGlobals.CADENCE_PLAYLIST_SIZE
thread_pool_size =  CadenceGlobals.CADENCE_THREADPOOL_SIZE 


class CadenceAPI(object):
	def __init__(self, sp_token, username, printFunc, getStopped):
		try:
			self.spotify = SpotifyAPI(sp_token, username);
			self.lastfm = LastFmAPI();
			self.suggested_tracks = [];
			self.printFunc = printFunc;
			self.getStopped = getStopped;
		except:
			CadenceError.error("Error in CadenceAPI.init()", sys.exc_info())
			return 1;

	#Check if list1 contains input obj
	def __listContains(self, list1, obj):
		for el in list1:
			if el == obj:
				return True;
		return False;

	#Reduces the data size of input playlist
	def __cutPlDataSize(self, plData):
		uniqueArtists = [];
		newPlData = [];
		for artistData in plData:
			artistName = artistData[0];
			if not self.__listContains(uniqueArtists, artistName): 
				newPlData.append(artistData);
				uniqueArtists.append(artistName);
		return newPlData;
	
	#Generates a new playlist. This is used only for giving data to LastFM
	def makePlaylist(self):
		try:
			plData = self.spotify.getPlaylistData();
			##REMOVE ME, DO NOT USE IN ACTUAL PRODUCTION
			##THIS CUTS THE SONGS TO A BARE MINIMUM FOR
			##PERFORMANCE, ONLY FOR LASTFM SINCE
			##RECOMMENDATIONS ARE BASED ON ARTIST ONLY
			##__cutPlDataSize CUTS EVERY SONG EXCEPT THE UNIQUE
			##ARTISTS' SONGS
			plData = self.__cutPlDataSize(plData);
			if plData == 1:
				return 1;
			results = self.makeRecommendation(plData); #Returns in the form [ [artistdata], [artistdata] ]
			#Where [artistdata] = ['band', 'song', 'trackuri']
			new_results = [];
			for artist_result in results: #Flattening results
				for song_result in artist_result:
					new_results.append(song_result); #All results will be in new_results
			results = new_results;
			
			size = len(results);
			random.shuffle(results);
			if size > playlist_size:
				size = playlist_size;

			return results[:size];
		except:
			CadenceError.error("Error in CadenceAPI.makePlaylist()", sys.exc_info())
		return 1;

	#Produces new recommendataions based off the input playlist
	def makeRecommendation(self, plData):
		try:
			suggested_tracks = [];
			pool = ThreadPool(thread_pool_size);
			results = pool.map(self.makeRecommendationForSong, plData);
			return results;
		except:
			CadenceError.error("Error in CadenceAPI.makeRecommendation()", sys.exc_info())
		return 1
	
	#Produces new recommendation based off of input song
	#song = Artist, SongName
	def makeRecommendationForSong(self, song):
		self.printFunc("Processing " + song[0] + " " + song[1]);
		#song_tags = lastfm.getTrackTags(song[0], song[1]);
		#TODO? Could do stuff with tags here
		suggested_tracks = [];
		#Gets the top tracks for artist related to the input song
		top_tracks = self.lastfm.getTopTracks(self.lastfm.getSimilarArtist(song[0]));
		for track in top_tracks:
			artist = track[0];
			track_names = track[1];
			#TODO make this a thread pool
			for track_name in track_names:
				if self.getStopped():
					return 1;
				track_uri = SpotifyAPI.getTrackURI(artist, track_name);	
				suggested_tracks.append([artist, track_name, track_uri]);
		return suggested_tracks;

#Tests...
def testPrint(txt):
	print txt;
def testStopped():
	return False;
def testCadence():
	client_id = CadenceGlobals.SPOTIFY_CLIENT_ID	
	client_secret = CadenceGlobals.SPOTIFY_CLIENT_SECRET
	redirect_uri = CadenceGlobals.SPOTIFY_REDIRECT_URI
	username = CadenceGlobals.SPOTIFY_USERNAME
	scope = CadenceGlobals.SPOTIFY_SCOPE
	token = util.prompt_for_user_token(username, scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri);
	cadenceAPI = CadenceAPI(token, username, printFunc=testPrint, getStopped=testStopped);
	cadenceAPI.makePlaylist();		
