#!/usr/bin/env python

import sys, time, os, socket
from daemon import Daemon

class MyDaemon(Daemon):
	def run(self):

		# Bind the socket to the port
		print('starting up on %s' % self.socketf)
		# Create pointer
		sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
		sock.bind(self.socketf)

		print("Socketfile exists")
	
		# Listen for incoming connections
		sock.listen(1)
		while True:

			# Wait for a connection
			print('SERVER: waiting for a connection')
			connection, client_address = sock.accept()
			try:
				pid = os.fork()
				print >>sys.stderr, 'SERVER: connection from', client_address
#
			        # Receive the data in small chunks and retransmit it
			        while True:
			            data = connection.recv(16)
			            print >>sys.stderr, 'SERVER: received "%s"' % data
			            if data:
			                print >>sys.stderr, 'SERVER: sending data back to the client'
			                connection.sendall(data)
			            else:
			                print >>sys.stderr, 'SERVER: no more data from', client_address
			                break
            
			finally:
				print("SERVER: Lets take a rest before we close")
				time.sleep(4)
		        	# Clean up the connection
			        connection.close()

	def wiggle(self):
		try:
		   with open(self.socketf):
			print("%s does not exist" % self.socketf)
		except IOError:
		   os.remove(self.socketf)	

if __name__ == "__main__":
	daemon = MyDaemon('/var/aurza/run/aurza.pid')
	if len(sys.argv) == 2:
		if 'start' == sys.argv[1]:
			print("Starting Daemon")
			daemon.start()
		elif 'stop' == sys.argv[1]:
			print("Stoping Daemon")
			daemon.stop()
		elif 'restart' == sys.argv[1]:
			print("Restarting Daemon")
			daemon.restart()
		else:
			print "Unknown command"
			sys.exit(2)
		sys.exit(0)
	else:
		print "usage: %s start|stop|restart" % sys.argv[0]
		sys.exit(2)

