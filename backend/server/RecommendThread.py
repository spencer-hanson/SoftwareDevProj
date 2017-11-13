import threading
import Queue
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
import urllib2
import timeit
import time
from CommandTerminal import *
from CadenceAPI import *
import traceback
class RecommendThread(threading.Thread):
	def __init__(self, username, sp_token, printFunc=-1, newGetStopped=-1):
		threading.Thread.__init__(self);
		if printFunc == -1:
			printFunc = self.doPrint;
		if newGetStopped == -1:
			newGetStopped = self.getStopped;
		self.username = username;
		self.sp_token = sp_token;
		self.thread_name = "REC-{}".format(self.username);
		self.stopped = False;
		self.data = "none";
		self.doPrint = printFunc;
		self.getStopped = newGetStopped;
	def getStopped(self):
		return self.stopped;
	def end(self):
		self.stopped = True;
	def doPrint(self, txt):
		CommandTerminal.printThread(self.thread_name, txt);
	def getData(self):
		return self.data;
	def run(self):
		try:
			self.doPrint("Starting thread for {} {}".format(self.username, self.sp_token));

		#	time.sleep(5);
		#	self.stopped = True;
		#	return 0;

			cadenceAPI = CadenceAPI(self.sp_token, self.username, self.doPrint, self.getStopped);
			if cadenceAPI != 1:
				newPlData = cadenceAPI.makePlaylist();
				if newPlData != 1:	
					self.data = SpotifyAPI.createPlaylist(self.sp_token, self.username, newPlData);
				else:
					self.doPrint("[ERROR] newPlData returned 1");
					self.data = "error";
			else:
				self.doPrint("[ERROR] cadenceAPI returned 1");
				self.data = "error";
		except:
			self.doPrint("Error in processing thread");
			self.doPrint("{}".format(sys.exc_info()[0]));
			self.doPrint("{}".format(sys.exc_info()[1]));
			self.doPrint("{}".format(sys.exc_info()[2]));
			traceback.print_tb(sys.exc_info()[2]);
		finally:
			if not self.data:
				self.data = "error";
			self.stopped = True;
			self.doPrint("Finished thread for {} {}".format(self.username, self.sp_token));
		return 0;
	def doStuff(self):
		urls = [
  'http://www.python.org', 
  'http://www.python.org/about/',
  'http://www.onlamp.com/pub/a/python/2003/04/17/metaclasses.html',
  'http://www.python.org/doc/',
  'http://www.python.org/download/',
  'http://www.python.org/getit/',
  'http://www.python.org/community/',
  'https://wiki.python.org/moin/',
  'http://planet.python.org/',
  'https://wiki.python.org/moin/LocalUserGroups',
  'http://www.python.org/psf/',
  'http://docs.python.org/devguide/',
  'http://www.python.org/community/awards/'
  # etc.. 
  ]
  
		pool = ThreadPool(8) # Sets the pool size to 8

		start_time = timeit.default_timer()  
		results = pool.map(urllib2.urlopen, urls)
		time_taken = timeit.default_timer() - start_time;
		self.doPrint(time_taken);

