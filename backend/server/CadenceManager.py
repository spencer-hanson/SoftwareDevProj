import time
import sys
import threading
from multiprocessing import Process
from RecommendServer import *
from CommandTerminal import *
from RecommendThread import *

class CadenceManager(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self);
		self.stopped = False;
		self.threads = {};
	def run(self):
		RecommendServer.cadenceManager = self;
		self.webserver = CadenceWebserverThread();
		self.webserver.start();
	def end(self):
		self.stopped = True;
		self.webserver.shutdown();
		for key, val in self.threads.iteritems():
			if not val.getStopped():
				print "Stopping Thread \'{}\'".format(val.thread_name);
				val.end();
				val.join();

	def pruneThreads(self):
		toremove = [];
		for key, val in self.threads.iteritems():
			if val.getStopped():
				print "Pruning Thread \'{}\'".format(val.thread_name);
				val.join();
				toremove.append(key);
		for key in toremove:
			del self.threads[key];	
	def doProcessing(self, sp_token, username): #Make a playlist for a user, return in the form [status, data], where status is none, working, started, or done, and data is the playlist uri
		result = ["none", "none"];
		if username in self.threads:
			if self.threads[username].getStopped():
				print "Finishing processing for: {}!".format(username);
				result = ["done", self.threads[username].getData()];
				self.pruneThreads();
			else:
				print "Already processing for: {}!".format(username);
				result = ["working","none"];
		else:
			new_thread = RecommendThread(username, sp_token);
			new_thread.start();
			self.threads[username] = new_thread;
			print "Started processing for {}!".format(username);
			result = ["started","none"];
		return result;


class CadenceWebserverThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self);
		self.recommendServer = RecommendServer();
	def run(self):
		print "Starting webserver!";
		self.recommendServer.start();
	def shutdown(self):
		print "Stopping webserver!";
		self.recommendServer.end();
