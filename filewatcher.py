#!/usr/bin/env python

import time
import sys
import os
import subprocess
import daemon

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


LOGFILE = '/var/log/filewatcher.log'

class EventHandler(PatternMatchingEventHandler):
	patterns = ["*"]

	def do_handleChanges(self, event):
		buildCmd = "swift build"
		runCmd = ".build/debug/App"
		
		print event.src_path, event.event_type
		process = subprocess.Popen(buildCmd.split(), stdout=subprocess.PIPE) 
		output, error = process.communicate()
		
		print output, error

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
	eventHandler.logfile = open(logfile, 'a')

	observer = Observer()
	observer.schedule(eventHandler, path=args[0] if args else '.')
	observer.start()

	eventHandler.logfile.write("filewatcher.py is watching on: {0}".format(repr(os.getcwd())))
	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		observer.stop()
	observer.join()
