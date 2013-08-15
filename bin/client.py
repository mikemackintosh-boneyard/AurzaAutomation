#!/usr/bin/env python

import sys, time, os, socket
from daemon import Daemon


# Create a UDS socket
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = '/var/aurza/run/aurza.sock'

print >>sys.stderr, 'CLIENT: connecting to %s' % server_address
try:
    sock.connect(server_address)
except socket.error, msg:
    print >>sys.stderr, msg
    sys.exit(1)

try:
    
    # Send data
    message = 'This is the message.  It will be repeated.'
    print >>sys.stderr, 'CLIENT: sending "%s"' % message
    sock.sendall(message)

    amount_received = 0
    amount_expected = len(message)
    
    while amount_received < amount_expected:
        data = sock.recv(16)
        amount_received += len(data)
        print >>sys.stderr, 'CLIENT: received "%s"' % data
except socket.error, msg:
    print >>sys.stderr, msg
    sys.exit(1)
finally:
    print >>sys.stderr, 'CLIENT: closing socket'
    sock.close()
