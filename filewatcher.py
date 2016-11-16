#!/usr/bin/env python

import time
import sys
import os
import subprocess
import daemon

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

class EventHandler(PatternMatchingEventHandler):
	patterns = ["*"]

	def do_handleChanges(self, event):
		print "Handle changes"

		commands = sys.argv[1:]
		
		print "Have CMDS: {0}".format(commands)
		
	def process(self, event):
		print event
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
