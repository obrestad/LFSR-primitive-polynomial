#!/usr/bin/python3

from polynomial import Polynomial

import sys

if(len(sys.argv) > 2):
	for i in range(2 ** int(sys.argv[1]), 2 ** (int(sys.argv[2]) + 1)):
		p = Polynomial(i)
		if(p.primitive()):
			print(i, str(p))
