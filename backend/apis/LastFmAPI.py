import sys
sys.path.append('util')
import pylast
import urllib2
import CadenceGlobals
from CadenceError import *
from bs4 import BeautifulSoup


class LastFmAPI():
	def __init__(self):
		self.API_KEY = CadenceGlobals.LASTFM_API_KEY
		self.API_SECRET =  CadenceGlobals.LASTFM_API_SECRET
		self.toptrack_limit =  CadenceGlobals.LASTFM_TOPTRACK_LIMIT
		self.simartist_limit =  CadenceGlobals.LASTFM_SIMARTIST_LIMIT
		self.api_prefix =  CadenceGlobals.LASTFM_API_PREFIX
		
	#Get the MusicBrains ID for given artist
	def getMBID(self, artist_name):
		try:
			url = self.api_prefix + "artist.search&artist={}&api_key={}".format(artist_name, self.API_KEY)	
			response = urllib2.urlopen(url).read()
			soup = BeautifulSoup(response, "lxml")
			return soup.find('artist').find('mbid').string
		except (urllib2.HTTPError, urllib2.URLError):
			CadenceError.error("Error in LastFm.getMBID()", sys.exc_info())
		return 1
	
	#Fetches all the LFM tags for the given artist's song. 
	def getTrackTags(self, artist, track):
		tags = []
		try:		
			url = self.api_prefix + "track.getinfo&artist={}&track={}&api_key={}".format(artist, track, self.API_KEY)
			response = urllib2.urlopen(url).read()
			
			soup = BeautifulSoup(response, "lxml")
			for tag in soup.find_all('tag'): #Get all tags of the track
				tags.append(tag.find('name').string.lower())
			return tags
		except (urllib2.HTTPError, urllib2.URLError):
			CadenceError.error("Error in LastFm.getTrackTags()", sys.exc_info())
		return 1

	#Will get LFM's related artists, limits the number with input
	def getSimilarArtistWithLimit(self, artist, limit):
		tmp = self.simartist_limit
		self.simartist_limit = limit
		data = self.getSimilarArtist(artist)
		self.simartist_limit = tmp
		return data

	#Gets all of LFM's related artists with no limit to number returned
	def getSimilarArtist(self, artist):
		artists = [];	
		try:		
			url = self.api_prefix + "artist.getsimilar&limit={}&artist={}&api_key={}".format(self.simartist_limit, artist, self.API_KEY)
			response = urllib2.urlopen(url).read()
			soup = BeautifulSoup(response, "lxml")
			for tag in soup.find_all('artist'):
				artists.append(tag.find('name').string.lower())
			return artists
		except (urllib2.HTTPError, urllib2.URLError):
			CadenceError.error("Error in LastFm.GetSimilarArtist()", sys.exc_info())
		return 1

	#Fetches the artist's top tracks from LFM
	def getTopTracks(self, artists):
		alltracks = []
		for artist in artists:
			try:
				url = self.api_prefix + "artist.gettoptracks&limit={}&artist={}&api_key={}".format(self.toptrack_limit, artist, self.API_KEY)		
				response = urllib2.urlopen(url).read()
				soup = BeautifulSoup(response, "lxml")
				artist_tracks = []
				for tag in soup.find_all('track'):
					artist_tracks.append(tag.find('name').string.lower())
				alltracks.append([artist, artist_tracks])
			except (urllib2.HTTPError, UnicodeEncodeError, urllib2.URLError):
				CadenceError.error("Error in getTopTracks()", sys.exc_info())
				return 1
		return alltracks

#Testing...
def testLastFM():
	artist_name = "pendulum"
	track_name = "The Island - Pt. I (Dawn)"
	test = LastFmAPI()
	test.getMBID(artist_name)
	test.getTrackTags(artist_name, track_name)
	test.getTopTracks(test.getSimilarArtist(artist_name))

