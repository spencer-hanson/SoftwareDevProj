import sys
sys.path.append('apis')
sys.path.append('server') 
sys.path.append('util')
from flask import Flask, request, jsonify, Response
from flask.views import View
from SpotifyAPI import *
from multiprocessing import Process
from ResponseProtocol import *
import time
import threading
import requests


class RecommendServer(View):
	methods = ['GET'];
	cadenceManager = -1; #Is set later to a manager instance
	def __init__(self):
		self.app = Flask(__name__)
		self.app.add_url_rule("/", view_func=self.as_view('/'));
		self.app.add_url_rule("/killserver", view_func=ShutdownView.as_view('killserver'));
		self.app.debug = False;
	def start(self):
		self.app.run();
	def end(self):
		requests.get('http://localhost:5000/killserver');
	def validArgs(self, all_args):
		if not "atoken" in all_args or not "username" in all_args:
			return False;
		username = all_args["username"];
		atoken = all_args["atoken"];
		if (atoken == "undefined" or username == "undefined"):
			return False;
		return True;
	def dispatch_request(self):
		all_args = request.args.to_dict();
		request_status = "invalid-unknown"; #Invalid until validated
		if not self.validArgs(all_args):
			request_status = "invalid-args";
			username = "none";
			sp_token = "none";
			result = ["none", "none"]; #status, data
		else:
			request_status = "valid";
			username = all_args["username"];
			sp_token = all_args["atoken"];
			result = self.cadenceManager.doProcessing(sp_token, username);
			if result[1] == "error": #If the returned data is error, make the status error as well
				result[0] = "error";
		resp = [["request",request_status], ["username",username], ["atoken",sp_token],["status",result[0]],["data",result[1]]]; 
		resp = Response(ResponseProtocol.doResponse(resp));
		resp.headers["Access-Control-Allow-Origin"] = "*";
		return resp;

class ShutdownView(View):
	def dispatch_request(self):
		func = request.environ.get('werkzeug.server.shutdown')
		if func is None:
			raise RuntimeError("Not Running WerkZeug Server!");
		func()
		return "Server is killed";
