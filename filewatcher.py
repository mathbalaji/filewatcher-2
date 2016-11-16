#!/usr/bin/env python

import time
import sys
import os
import subprocess
import daemon
from optparse import OptionParser

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

def getOptions:
	parser = OptionParser()
	parser.add_option("-f", "--file", dest="filename", help="write report to FILE", metavar="FILE")
	parser.add_option("-q", "--quiet", action="store_false", dest="verbose", default=True, help="don't print status messages to stdout")

(options, args) = parser.parse_args()

class EventHandler(PatternMatchingEventHandler):
	patterns = ["*"]

	def do_handleChanges(self, event):
		print "Handle changes"

		commands = sys.argv[1:]
		for cmd in commands:
			print "Executing \"{0}\" ...".format(cmd)
			returnCode = subprocess.call(cmd, shell=True)
			print "Done \"{0}\"".format(cmd)
			print "Return: {0}".format(returnCode)

		
	def process(self, event):
		"""
		event.event_type
			'modified' | 'created' | 'moved' | 'deleted'
		event.is_directory
			True | False
		event.src_path
			path/to/file
		"""
		self.do_handleChanges(event)
	
	def on_modified(self, event):
		self.process(event)
	
	def on_create(self, event):
		self.process(event)

if __name__ == '__main__':
	args = sys.argv[1:]
	logfile = "./filewatcher.log"
	eventHandler = EventHandler()

	observer = Observer()
	observer.schedule(eventHandler, path='.')
	observer.start()
	
	print "filewatcher.py is watching on: {0}".format(repr(os.getcwd()))
	
	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		observer.stop()
	observer.join()
