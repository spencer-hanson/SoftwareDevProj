import sys
sys.path.append("util")
from Crawler import *
from flask import Flask, request, jsonify, Response
from flask.views import View


class CrawlServer(View):
	methods = ['GET'];
	def __init__(self):
		self.app = Flask(__name__)
		self.app.add_url_rule("/", view_func=self.as_view('/'));
		self.app.add_url_rule("/killserver", view_func=ShutdownView.as_view('killserver'));
		self.app.debug = False;
	def start(self):
		self.app.run(port='8675')
	def end(self):
		requests.get('http://localhost:8675/killserver');
	def validArgs(self, all_args):
		if not "artist" in all_args or not "depth" in all_args:
			return False;
		artist = all_args["artist"];
		depth = all_args["depth"];
		if (artist == "undefined" or depth == "undefined"):
			return False;
		try:
			depth = int(depth)
		except:
			return False
		return True;
	def dispatch_request(self):
		all_args = request.args.to_dict();
		if not self.validArgs(all_args):
			resp = Response(self.get_graph_data("Error", 1))
		else:
			#graph_data = "{} {}".format(all_args["artist"], all_args["depth"])
			artist = all_args["artist"]
			depth = int(all_args["depth"])
			graph_data = self.get_graph_data(artist, depth)
			resp = Response(graph_data)
		resp.headers["Access-Control-Allow-Origin"] = "*"
		return resp;


	@staticmethod
	def _make_graph_node(name, group, data):
		data.append("\"name\":\"{}\",".format(name))
		data.append("\"group\":{}".format(group))

	@staticmethod
	def _make_graph_link(source, target, data):
		data.append("\"source\":{},".format(source))
		data.append("\"target\":{}".format(target))

	def get_graph_data(self, artist, depth):
		crawler = Crawler(artist, depth)
		crawler.startCrawl()
		allnodes = crawler.seen_artists


		data = [];
		data.append("{")
		#Nodes
		data.append("\"nodes\":[")
		for i in range(0, len(allnodes)): 
			data.append("{")
			CrawlServer._make_graph_node(allnodes[i], crawler.groups[allnodes[i]], data)
			data.append("},")

		data[-1] = data[-1][:-1] #Remove the ',' from the last json entry

		data.append("],")
		#Links
		data.append("\"links\":[")
		for i in range(0, len(allnodes)):
			if allnodes[i] in crawler.database: #There are more connections
				for sim_artist in crawler.database[allnodes[i]]:
					data.append("{")
					CrawlServer._make_graph_link(crawler.artist_id[allnodes[i]], 
						crawler.artist_id[sim_artist], data)
					data.append("},")
			else: #It's an end node
				pass
		data[-1] = data[-1][:-1]	

		data.append("]")
		data.append("}")

		str_data = "";
		for item in data:
			str_data = str_data+item
		return str_data	

class ShutdownView(View):
        def dispatch_request(self):
                func = request.environ.get('werkzeug.server.shutdown')
                if func is None:
                        raise RuntimeError("Not Running WerkZeug Server!");
                func()
                return "Server is killed";
                                              

if __name__ == "__main__":
	CrawlServer().start()
