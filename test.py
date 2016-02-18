#!/usr/bin/python3

from polynomial import Polynomial

import sys

if(len(sys.argv) < 2):
	print("Usage: %s <polynomial>" % sys.argv[0])
	sys.exit(1)

p = Polynomial(sys.argv[1])
if(p.primitive()):
	print("The polynomial '%s' is primitive!" % str(p))
else:
	print("The polynomial '%s' is NOT primitive!" % str(p))
