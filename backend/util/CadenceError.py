import traceback
class CadenceError(object):
	@staticmethod
	def error(msg, exc_info):
		print "[ERROR] {}".format(msg)
		print exc_info[0]
		print exc_info[1]
		traceback.print_tb(exc_info[2])

