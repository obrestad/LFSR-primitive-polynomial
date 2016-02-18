#!/usr/bin/python3

import sys

from polynomial import Polynomial
from ast import literal_eval

if(len(sys.argv) < 2):
	print("Usage: %s <input_file>" % sys.argv[0])
	sys.exit(1)

try:
	f = open(sys.argv[1], 'r')
except IOError as e:
	print("Could not open file")
	print(e)
	sys.exit(2)

polynomials=literal_eval(f.read())

for p in polynomials:
	print(int(p), Polynomial(int(p)))
