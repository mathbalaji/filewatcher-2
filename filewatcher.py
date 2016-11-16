#!/usr/bin/env python

import time
import sys
import os
import subprocess
import daemon

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

PIDFILE = '/var/run/filewatcher.pid' 
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
		
		event.event_type
			'modified' | 'created' | 'moved' | 'deleted'
		event.is_directory
			True | False
		event.src_path
			path/to/file
		
		self.do_handleChanges(event)
	
	def on_modified(self, event):
		self.process(event)
	
	def on_create(self, event):
		self.process(event)

class Filewatcher(Daemon):
	def run(self):
		args = sys.argv[1:]
		
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
		
		# Logging errors and exceptions
		try:
			pass
		except Exception, e:
			logging.exception('Human friendly error message, the exception will be captured and added to the log file automaticaly')
		while True:
			time.sleep(60)
			

if __name__ == '__main__':
	fw = FileWatcher(PIDFILE)
	
	if len(sys.argv) == 2:

	if 'start' == sys.argv[1]:
		try:
			daemon.start()
		except:
			pass

	elif 'stop' == sys.argv[1]:
		print "Stopping ..."
		daemon.stop()

	elif 'restart' == sys.argv[1]:
		print "Restaring ..."
		daemon.restart()

	elif 'status' == sys.argv[1]:
		try:
			pf = file(PIDFILE,'r')
			pid = int(pf.read().strip())
			pf.close()
		except IOError:
			pid = None
		except SystemExit:
			pid = None

		if pid:
			print 'YourDaemon is running as pid %s' % pid
		else:
			print 'YourDaemon is not running.'

	else:
		print "Unknown command"
		sys.exit(2)
		sys.exit(0)
else:
	print "usage: %s start|stop|restart|status" % sys.argv[0]
	sys.exit(2)

