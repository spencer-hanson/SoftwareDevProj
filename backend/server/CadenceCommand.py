class CadenceCommand(object):
	def __init__(self, shutdown):
		self.shutdown = shutdown;
	def runCommand(self, data):
		if data == "CTRL_C" or data == "exit":
			print "\\^prefix:[System];nosuffix$\\ Stopping...";
			self.shutdown();
		else:
			print data;
