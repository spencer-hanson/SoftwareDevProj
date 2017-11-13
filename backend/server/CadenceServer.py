from blessings import Terminal
import time
import sys
import threading
import subprocess as sp
from CommandTerminal import *
from CadenceCommand import *
from CadenceManager import *


cadenceManager = 0;
commandTerminal = 0;
def testRunCommand(data):
	pass;
def testShutdown():
	cadenceManager.end();
	commandTerminal.printer.getOrigOut().flush();
	commandTerminal.printer.stopManaging();
def testWrite(stxt):
	pass;
def shutdown():
	cadenceManager.end();
	commandTerminal.end();
class CadenceServer(object):
	@staticmethod
	def getCadenceManager():
		return cadenceManage;
#How to start the terminal
if __name__ == "__main__":
	terminal = Terminal();
	if len(sys.argv) > 1:
		if sys.argv[1] == "-test":
			cadenceCommands = CadenceCommand(testShutdown);
			cadenceManager = CadenceManager();
			cadenceManager.start();
			commandTerminal = CommandTerminal(terminal, testRunCommand);
			commandTerminal.printer.startManaging();
			commandTerminal.printer.write = testWrite;		
		else:
			print "Unknown parameter: {}, exiting".format(sys.argv[1]);
	else:
	        tmp = sp.call('clear', shell=True);
		terminal.clear();
		terminal.fullscreen();
		cadenceCommands = CadenceCommand(shutdown);
		cadenceManager = CadenceManager();
	
		cadenceManager.start();
		commandTerminal = CommandTerminal(terminal, cadenceCommands.runCommand);
		commandTerminal.start();
