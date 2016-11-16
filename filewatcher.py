#!/usr/bin/env python

import time
import sys
import os
import subprocess
import daemon
from optparse import OptionParser

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

parser = OptionParser()
parser.add_option('-w', '--watchdir', dest='watchdir', default='.', help="Watching this directory instead of \'.\'")
parser.add_option('-l', '--log', dest='log', default=sys.stdout, help="Destination for printing logs.")
opts = parser.parse_args()


class EventHandler(PatternMatchingEventHandler):
	patterns = ["*"]

	def do_handleChanges(self, event):
		print "Handle changes"

		print opts
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
	eventHandler = EventHandler()

	observer = Observer()
	observer.schedule(eventHandler, path='.')
	observer.start()
	
	print >> open(opts.log, 'a'), 'Hello', 'World', 2+3
	print "filewatcher.py is watching on: {0}".format(repr(os.getcwd()))
	
	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		observer.stop()
		
	observer.join()
